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

    INSERT INTO AUD_CARTERA (ID_CARTERA,
                             TIPO_OPERACION,
                             VALOR_ANTERIOR,
                             VALOR_NUEVO,
                             USUARIO_BD,
                             FECHA_HORA)
                      VALUES (NVL(:OLD.ID, :NEW.ID),
                              v_tipo_op,
                              CASE WHEN v_tipo_op != 'INSERT' THEN TO_CHAR(:OLD.SALDO_PENDIENTE) ELSE NULL END,
                              CASE WHEN v_tipo_op != 'DELETE' THEN TO_CHAR(:NEW.SALDO_PENDIENTE) ELSE NULL END,
                              USER,
                              SYSTIMESTAMP);
END;
/
