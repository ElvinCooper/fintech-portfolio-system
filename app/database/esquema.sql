-- vista para reportes
CREATE OR REPLACE VIEW VW_RESUMEN_CARTERA AS
SELECT
    c.id,
    c.nombre AS nombre_cliente,
    COUNT(p.id) AS total_carteras,
    SUM(p.saldo_pendiente) AS saldo_total,
    MAX(p.fecha_inicio) AS ultima_operacion
FROM CLIENTES c
LEFT JOIN CARTERA p ON c.id = p.cliente_id
GROUP BY c.id, c.nombre;
/

------ Trigger para auditoria cartera
create or replace NONEDITIONABLE TRIGGER TRG_AUDIT_CARTERA
after insert or update or delete on CARTERA
FOR EACH ROW
DECLARE
    v_tipo_op VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_tipo_op := 'INSERT';
    ELSIF UPDATING THEN
        v_tipo_op := 'UPDATE';
    ELSE
        v_tipo_op := 'DELETE';
    END IF;

    INSERT INTO AUD_CARTERA (ID_CARTERA ,
                             TIPO_OPERACION,
                             VALOR_ANTERIOR,
                             VALOR_NUEVO,
                             USUARIO_BD,
                             FECHA_HORA)
                      VALUES (:OLD.ID,
                              v_tipo_op,
                              CASE WHEN v_tipo_op != 'INSERT' THEN TO_CHAR(:OLD.SALDO_PENDIENTE) ELSE NULL END,
                              CASE WHEN v_tipo_op != 'DELETE' THEN TO_CHAR(:NEW.SALDO_PENDIENTE) ELSE NULL END,
                              USER,
                              SYSTIMESTAMP);
END;
/

---------------------- PROCEDIMIENTO PARA TRANSFERIR SALDO ---------------
CREATE OR REPLACE PROCEDURE SP_TRANSFERIR_SALDO (
    p_id_origen      IN  NUMBER,
    p_id_destino     IN  NUMBER,
    p_monto          IN  NUMBER,
    p_codigo_res     OUT NUMBER,
    p_mensaje_res    OUT VARCHAR2
) AS
    v_saldo_origen NUMBER;
BEGIN
    SELECT saldo_pendiente INTO v_saldo_origen
    FROM CARTERA WHERE id = p_id_origen FOR UPDATE;

    IF v_saldo_origen < p_monto THEN
        p_codigo_res  := 1;
        p_mensaje_res := 'Saldo insuficiente en la cartera origen.';
        RETURN;
    END IF;

    UPDATE CARTERA SET saldo_pendiente = saldo_pendiente - p_monto WHERE id = p_id_origen;
    UPDATE CARTERA SET saldo_pendiente = saldo_pendiente + p_monto WHERE id = p_id_destino;

    COMMIT;

    p_codigo_res  := 0;
    p_mensaje_res := 'Transferencia exitosa.';

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        p_codigo_res  := 1;
        p_mensaje_res := 'Una o ambas carteras no existen.';
    WHEN OTHERS THEN
        ROLLBACK;
        p_codigo_res  := 2;
        p_mensaje_res := 'Error crítico: ' || SQLERRM;
END;
/

----------------- Procedimientos para obtener un historial de los movimientos de cartera -----------------
CREATE OR REPLACE PROCEDURE SP_GET_MOVIMIENTOS (
    p_id_cartera IN  NUMBER,
    p_recordset  OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_recordset FOR
        SELECT
            id_cartera,
            tipo_operacion,
            valor_anterior,
            valor_nuevo,
            usuario_bd,
            fecha_hora
        FROM AUD_CARTERA
        WHERE id_cartera = p_id_cartera
        ORDER BY fecha_hora DESC;
END;
/

--------- FUNCION PARA CALCULAR TASAS -------------------------
CREATE OR REPLACE FUNCTION FN_CALCULAR_TASAS (
    p_monto       IN NUMBER,
    p_tasa_anual  IN NUMBER,
    p_dias        IN NUMBER
) RETURN NUMBER DETERMINISTIC
AS
    v_resultado NUMBER(12,2);
BEGIN
    v_resultado := (p_monto * (p_tasa_anual / 100) * p_dias) / 360;
    RETURN NVL(v_resultado, 0);
EXCEPTION
    WHEN OTHERS THEN
        RETURN 0;
END;
/
