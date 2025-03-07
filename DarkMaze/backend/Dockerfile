FROM python:3.11

RUN groupadd -r appgroup && \
    useradd -r -m -g appgroup -d /app appuser && \
    chmod 775 /app

WORKDIR /app

COPY --chown=appuser:appgroup ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY --chown=appuser:appgroup ./src /app/src

USER appuser

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]