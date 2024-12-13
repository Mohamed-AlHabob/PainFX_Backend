# Use a specific Python version for consistency
FROM python:3.12-slim

# Set the working directory
WORKDIR /app
RUN mkdir -p /app/logs

# Install system dependencies for GDAL and other required tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for GDAL (to locate shared libraries and include files)
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy the entrypoint script and make it executable
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the application port
EXPOSE 8000

# Set the entry point to the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
