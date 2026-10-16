FROM docker.io/library/python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt \
    && useradd --system --uid 10001 --create-home cpc

COPY src/ /app/src/
COPY scripts/healthcheck.py /app/healthcheck.py
ENV PYTHONPATH=/app/src

USER 10001:10001

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "cpc.main:app", "--host", "0.0.0.0", "--port", "8000"]
