FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/opt/prefect/cveimporter \
    PREFECT_API_URL=http://prefect-server.prefect-demo.svc.cluster.local:4200/api \
    NVD_API_URL=https://services.nvd.nist.gov/rest/json/cves/2.0

COPY requirements.txt /opt/prefect/requirements.txt
RUN pip install --no-cache-dir -r /opt/prefect/requirements.txt

COPY ./cveimporter /opt/prefect/cveimporter/
COPY prefect.yaml /opt/prefect/cveimporter/prefect.yaml

WORKDIR /opt/prefect/cveimporter
CMD ["python", "main.py"]