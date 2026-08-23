FROM python:3.12.8-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN groupadd --system forgepulse && useradd --system --gid forgepulse --home-dir /app forgepulse
COPY pyproject.toml ./
COPY forgepulse ./forgepulse
RUN pip install --no-cache-dir .
USER forgepulse
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health/live')"
CMD ["uvicorn", "forgepulse.app:app", "--host", "0.0.0.0", "--port", "8080"]
