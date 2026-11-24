# NetDevOps Portfolio: Automated Network Lab

![CI Pipeline](https://github.com/wa9463673-rgb/netdevops-portfolio/actions/workflows/ci.yml/badge.svg)
[![NetDevOps CI Pipeline](https://github.com/wa9463673-rgb/netdevops-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/wa9463673-rgb/netdevops-portfolio/actions/workflows/ci.yml)

## 📌 Project Overview
This repository contains a production-ready Network Automation (NetDevOps) portfolio. It demonstrates the full lifecycle of network automation: from generating configurations using data-driven templates to pushing them to devices, validating the state, and automating backups with Git.

## 🛠️ Technologies Used
*   **Python 3.11** (Netmiko, NAPALM, GitPython)
*   **Ansible** (Cisco IOS collection)
*   **Jinja2** (Configuration templating)
*   **GitHub Actions** (CI/CD Pipeline for automated testing)
*   **Pytest** (Unit testing)

## 📂 Repository Structure
*   `ansible/`: Playbooks and inventory for configuration management.
*   `automation/`: Python scripts for pushing configs (`push_config.py`), validating networks (`validate_network.py`), and automated backups (`backup_configs.py`).
*   `backups/`: Automated timestamped configuration backups.
*   `inventory/`: YAML files containing network device data.
*   `templates/`: Jinja2 templates for generating Cisco IOS configurations.
*   `tests/`: Pytest unit tests ensuring template rendering is accurate.

## 🚀 How to Run (Local Execution)
*(Note: A virtual environment and a running network lab are required to execute against live devices).*

1. Clone the repository:
   `git clone https://github.com/wa9463673-rgb/netdevops-portfolio.git`
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run the dry-run push script:
   `python automation/python/push_config.py`

## 🧪 CI/CD Pipeline
This project uses GitHub Actions. Every push to the `main` branch triggers a cloud runner that installs the dependencies and runs `pytest` to ensure the Jinja2 configuration templates render without syntax errors.