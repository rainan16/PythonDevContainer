# Python 3 in a VSCode .devcontainer

Sample Python 3 project using a devcontainer pre-packed with a bunch of useful extensions.

You can modify settings and add or remove extensions to suit your needs by editing this file: [devcontainer.json](.devcontainer/devcontainer.json)

This setup is ready for Python development in a devcontainer without any interference.


## Get started

### Prerequisites

1. Docker or a Docker compliant CLI installed
2. On Windows use a Linux VM or WSL2 with
    - Docker Desktop installed OR
    - Docker CLI installed in WSL2 and Docker-Daemon started (activate systemd)
3. VSCode Extensions:
    - Dev Containers
    - WSL on Windows
  
For more information and troubleshootin see: <https://code.visualstudio.com/docs/devcontainers/tutorial>


### Build Dev container

Command/Ctrl + Shift + P
    "Dev Containers: Rebuild Container"

### Debug code

Just run ▶️ "Python: Flask in devcontainer" from the VSCode Debug menu on the left

## Extension in devcontainer

Extension that are automatically installed in the devcontainer see:
[devcontainer.json (customizations/vscode/extensions)](.devcontainer/devcontainer.json)
