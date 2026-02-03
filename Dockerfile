FROM python:3.12-slim

WORKDIR /src

ENV PYTHONPATH=/src

COPY requirements.txt .

# instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# copiar codigo fuente
COPY . /src

# puerto de la aplicacion
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]



