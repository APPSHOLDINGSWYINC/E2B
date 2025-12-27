FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY multi_dump_parser.py .
COPY example_dump.txt .
COPY README.md .

# Create output directory
RUN mkdir -p /output

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command shows help
CMD ["python", "multi_dump_parser.py"]

# Usage examples:
# docker build -t agentx5-parser .
# docker run -v $(pwd)/data:/data -v $(pwd)/output:/output agentx5-parser python multi_dump_parser.py /data/dump.txt /output
