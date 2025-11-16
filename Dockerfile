FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements_hf.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY gemm_simulator.py .
COPY cache_simulator.py .

# Expose port
EXPOSE 7860

# Set environment variable for port
ENV PORT=7860

# Run the application
CMD ["python", "app.py"]
