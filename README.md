# ITL.Prefect.CVE.Nist

This project provides an automated flow to fetch Common Vulnerabilities and Exposures (CVEs) from the [NVD API](https://nvd.nist.gov/developers) using Prefect for orchestration. It integrates Pydantic for configuration management, ensuring that environment-specific settings are loaded dynamically via environment variables.

## Project Structure

```
ITL.Prefect.CVE.Nist/
│   .env                  # Environment variables file (not committed)
│   Dockerfile            # Image build; copies cveimporter/ and prefect.yaml
│   prefect.yaml          # Prefect deployment definition (work pool, schedule, job variables)
│   README.md             # Project documentation
│   requirements.txt      # Python dependencies
│
├───.github/
│   └───workflows/
│       └───build-and-push.yaml  # GitHub Actions workflow for CI/CD
│
└───cveimporter/
    │   main.py            # Runs the flow locally
    │
    └───base/
        └───config.py      # Settings loaded from environment / .env
        └───flows.py       # update_cve_data_flow: watermark, windows, pagination
        └───tasks.py       # fetch_cve_data and process_cve_data tasks
```

### Key Components

1. **`main.py`**:  
   The entry point that runs `update_cve_data_flow` from the `base/flows.py` module.

2. **`base/config.py`**:  
   This file handles the configuration of environment variables using Pydantic. It ensures that settings like API URLs are correctly loaded from the environment. The configuration structure is as follows:
   - `nvd_api_url`: URL for the NVD CVE API.
   - `prefect_api_url`: URL for the Prefect API.
   
   These settings are pulled from an `.env` file or environment variables and validated using Pydantic's `BaseSettings` class.

3. **`base/flows.py`**:  
   Defines the Prefect flow `update-cve-data-flow`. The flow orchestrates the following steps:
   - Reads the watermark Variable `nist_cve_last_update` (default 2024-09-22 UTC).
   - Fetches CVEs from the NVD API in 90-day `lastModified` windows, paging 2000 results at a time.
   - Advances the watermark after each completed window, so a crashed run resumes from the last finished window.

4. **`base/tasks.py`**:  
   Contains Pre_data`: Fetches one page from the NVD API over a shared `requests.Session`, with 3 retries.
   - `process_cve_data`: Processes and prints the ID and English description of each CVE in a page
   - `process_cve_data`: Processes and prints key details from the fetched CVE data.

5. **`prefect.yaml`**:  
   Deployment `nist-cve-import` on the `itl-amalia` work pool, scheduled daily at 02:00 UTC, running image `nweistra/itlprefectcveflow:latest`.

<br>

## Configuration Management with Pydantic

The project uses Pydantic's `BaseSettings` for managing configuration, making it easier to handle environment-specific settings like API URLs. Pydantic automatically loads these values from environment variables or an `.env` file.

Here's an example of the `.env` file required to run the project:

```
NVD_API_URL=https://services.nvd.nist.gov/rest/json/cves/2.0
PREFECT_API_URL=http://your-prefect-server-url
NVD_API_KEY=optional-nvd-key
```

`NVD_API_KEY` is optional. Without it, requests are sent at 6-second intervals; with it, 0.6 seconds.

The configura_settings import BaseSettings, SettingsConfigDictnfig.py`:

```python
from pydantic import
    prefect_api_url: str
    nvd_api_key: str | None = None
clasmodel_config = SettingsConfigDict(env_file=".env", extra="ignore")eld(..., env="NVD_API_URL")
    prefect_api_url: str = Field(..., env="PREFECT_API_URL")
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Running the Project
11+ (the image uses 3.11)
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
cd cveimporter
python main.py
```

The flow reads the watermark, fetches all CVEs modified since then, and prints each CVE's ID and English description. Locally it uses the `PREFECT_API_URL` from `.env`, and it updates the watermark Variable on that server.

---

## CI/CD with GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/build-and-push.yaml`) for automating builds and pushing Docker images. The workflow can be triggered on code push or pull request events and handles the following steps:

- Build the Docker iDocker Hub as `nweistra/itlprefectcveflow` with `:<commit sha>` and `:latest` tags. Pull requests build without pushing
- Push the image to a container registry (e.g., DockerHub).

---

## Deployment
e project is deployed through Prefect, not Helm. `prefect.yaml` registers the `nist-cve-import` deployment on the `itl-amalia` Kubernetes work pool. Each run starts a Job in the `prefect-demo` namespace.

### Deployment Steps

1. Build the image (this copies `prefect.yaml` into it):
   ```bash
   docker build -t nweistra/itlprefectcveflow:latest .
   ```

2. For a kind cluster, load the image onto the node:
   ```bash
   kind load docker-image nweistra/itlprefectcveflow:latest --name itl-prefect
   ```

3. Register the deployment from the image:
   ```bash
   docker run --rm --add-host prefect.localhost:host-gateway -e PREFECT_API_URL=http://prefect.localhost:8080/api -e PYTHONUTF8=1 --entrypoint prefect nweistra/itlprefectcveflow:latest deploy --all
   ```

4. Trigger a run:Handle non-transient NVD errors beyond the task-level retries
   ```bash
   prefect deployment run "update-cve-data-flow/nist-cve-import"
   ```

The `namespace: prefect-demo` job variable is required. The worker's service account can only create Jobs in that namespace.m install itl-cve-importer ./itl-prefect-nist-cve
   ```

---

## Future Improvements

- **Logging**: Add proper logging instead of `print` statements for better observability.
- **Error Handling**: Implement retries for API requests and better error handling.
- **Data Storage**: Store CVE data in a database or a file system for long-term analysis.

