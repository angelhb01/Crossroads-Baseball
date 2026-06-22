FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy app code andmodels
COPY src/ ./src/
COPY models/ ./models/

# Expose PORT
EXPOSE 8000

# Run command to start api
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]