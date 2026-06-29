FROM python:3.12-slim

# 1. Prevent Python from writing pyc files and buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 2. Set working directory
WORKDIR /app

# 3. Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# 4. Install dependencies (Done as root, which is fine)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5. Switch to the non-root user before copying source code
USER appuser

# 6. Copy application source
COPY --chown=appuser:appuser . .

# 7. Expose FastAPI port
EXPOSE 8000

# 8. Start FastAPI with Uvicorn (Adding production flags)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips=*"]
