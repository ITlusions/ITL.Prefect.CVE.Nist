# Use Python 3.11 slim image as the base image
FROM python:3.11-slim

# Set environment variables for Prefect API (update according to your Prefect setup)
ENV PREFECT_API_URL=http://prefect-server.prefect-server.svc.cluster.local:4200/api
ENV NVD_API_URL=https://services.nvd.nist.gov/rest/json/cves/2.0

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies for the project, including Prefect 3.x
COPY requirements.txt /opt/prefect/requirements.txt
RUN pip install --no-cache-dir -r /opt/prefect/requirements.txt

# Copy your local flow code into the container (assuming your flow is in the "linkedinjobs" directory)
COPY ./cveimporter /opt/prefect/cveimporter/

# Set the working directory in the container
WORKDIR /opt/prefect/cveimporter/

# Optionally, install Prefect 3.x again if it's listed in requirements.txt
RUN pip install --no-cache-dir prefect

# Set the default command to run the Prefect flow
# Replace "main.py" with the appropriate entry script for your flow
CMD ["python", "main.py"]
