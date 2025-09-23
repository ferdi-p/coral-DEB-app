# Dockerfile
FROM python:3.11-slim

# (Optional) If you need SciPy wheels, the slim image can build them; uncomment if needed:
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential gfortran && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PORT=8080

# safer: non-root user
RUN useradd -m appuser
USER appuser

EXPOSE 8080
CMD ["python", "main.py"]