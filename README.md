# ITL.Prefect.Nist.CVE

This project provides an automated flow to fetch Common Vulnerabilities and Exposures (CVEs) from the [NVD API](https://nvd.nist.gov/developers) using Prefect for orchestration. It integrates Pydantic for configuration management, ensuring that environment-specific settings are loaded dynamically via environment variables.

## Project Structure

```
ITL.Prefect.Nist.CVE/
│   .env                  # Environment variables file
│   Chart.yaml            # Helm chart for Kubernetes deployment
│   Dockerfile            # Dockerfile for containerization
│   README.md             # Project documentation
│   requirements.txt      # Python dependencies
│   values.yaml           # Helm values for deployment configuration
│
├───.github/
│   └───workflows/
│       └───build-and-push.yaml  # GitHub Actions workflow for CI/CD
│
├───cveimporter/
│   │   main.py            # Entry point for running the flow
│   │
│   └───base/
│       └───config.py      # Configuration management using Pydantic
│       └───flows.py       # Prefect flow orchestration
│       └───tasks.py       # Prefect tasks for fetching and processing CVEs
│
└───templates/
        configmap.yaml      # Kubernetes ConfigMap template
        job.yaml            # Kubernetes Job template
        _helpers.tpl        # Helm helper functions
```

### Key Components

1. **`main.py`**:  
   The entry point that triggers the Prefect flow when executed. It imports and runs the `nvd_cve_flow` from the `flows.py` module.

2. **`base/config.py`**:  
   This file handles the configuration of environment variables using Pydantic. It ensures that settings like API URLs are correctly loaded from the environment. The configuration structure is as follows:
   - `nvd_api_url`: URL for the NVD CVE API.
   - `prefect_api_url`: URL for the Prefect API.
   
   These settings are pulled from an `.env` file or environment variables and validated using Pydantic's `BaseSettings` class.

3. **`base/flows.py`**:  
   Defines the Prefect flow `nvd_cve_flow`. The flow orchestrates the following steps:
   - Fetches CVE data from the NVD API for a specified date range.
   - Processes the fetched CVE data and prints a summary of the first 5 CVEs.

4. **`base/tasks.py`**:  
   Contains Prefect tasks that are used in the flow:
   - `fetch_cves_from_nvd`: Fetches CVEs from the NVD API using HTTP requests.
   - `process_cve_data`: Processes and prints key details from the fetched CVE data.

5. **`templates/`**:  
   Helm templates for Kubernetes deployment, including ConfigMaps, Jobs, and Helm helpers for managing configurations.

<br>

## Configuration Management with Pydantic

The project uses Pydantic's `BaseSettings` for managing configuration, making it easier to handle environment-specific settings like API URLs. Pydantic automatically loads these values from environment variables or an `.env` file.

Here's an example of the `.env` file required to run the project:

```
NVD_API_URL=https://services.nvd.nist.gov/rest/json/cves/2.0
PREFECT_API_URL=http://your-prefect-server-url
```

The configuration is defined in `base/config.py`:

```python
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    nvd_api_url: str = Field(..., env="NVD_API_URL")
    prefect_api_url: str = Field(..., env="PREFECT_API_URL")
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Running the Project

### Prerequisites

- Python 3.9+
- Docker (if running in containers)
- Prefect (local agent or Prefect Cloud)
- Environment variables set up in an `.env` file

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ITL.Prefect.Nist.CVE.git
   cd ITL.Prefect.Nist.CVE
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create the `.env` file:
   ```bash
   echo "NVD_API_URL=https://services.nvd.nist.gov/rest/json/cves/2.0" > .env
   echo "PREFECT_API_URL=http://your-prefect-server-url" >> .env
   ```

### Running the Flow

To run the flow locally, execute the following command:

```bash
python cveimporter/main.py
```

The flow will fetch CVE data from the NVD API for the current day and process the results, printing the details of the first 5 CVEs.

---

## CI/CD with GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/build-and-push.yaml`) for automating builds and pushing Docker images. The workflow can be triggered on code push or pull request events and handles the following steps:

- Build the Docker image.
- Push the image to a container registry (e.g., DockerHub).

---

## Deployment

This project can be deployed to a Kubernetes cluster using Helm. The Helm chart (`Chart.yaml`) and values configuration (`values.yaml`) allow you to define various deployment configurations like API URLs and resource limits.

### Helm Deployment Steps

1. Package the Helm chart:
   ```bash
   helm package .
   ```

2. Install the chart in your Kubernetes cluster:
   ```bash
   helm install itl-cve-importer ./itl-prefect-nist-cve
   ```

---

## Future Improvements

- **Logging**: Add proper logging instead of `print` statements for better observability.
- **Error Handling**: Implement retries for API requests and better error handling.
- **Data Storage**: Store CVE data in a database or a file system for long-term analysis.

