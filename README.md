#  Carbon Emission Calculator

[![CI](https://github.com/Gi-v/Carbon-Emission-Calculator/actions/workflows/ci.yml/badge.svg)](https://github.com/Gi-v/Carbon-Emission-Calculator/actions)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django 4.2](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)

A comprehensive, web-based carbon footprint tracking system that helps individuals and organizations log daily activities, calculate associated greenhouse gas emissions, and monitor reduction targets — all through an interpretable, data-driven dashboard.

---

##  Table of Contents

- [Motivation](#-motivation)
- [Features](#-features)
- [Technology Stack](#️-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Option 1: Local Development](#option-1-local-development)
  - [Option 2: Docker Setup](#option-2-docker-setup)
- [Usage](#-usage)
- [Contributing](#-contributing)
- [License](#-license)

---

##  Motivation

As environmental sustainability becomes a critical global priority, there is a pressing need for accessible tools that accurately quantify carbon emissions. This project bridges the gap between complex emission quantification methods and everyday user activities — empowering users to make informed decisions, understand the environmental cost of their actions, and actively reduce their carbon footprint through manageable goals.

---

##  Features

| Feature | Description |
|---|---|
| **Activity Catalog** | Log emission-generating activities using a robust catalog with custom emission factors for precise calculations |
| **Interpretable Dashboard** | High-level overview of total emissions, recent activities, and progress against environmental targets |
| **Goal Management** | Establish, track, and achieve customized emission reduction goals |
| **Historical Tracking** | Detailed logs and history views to analyze emission trends over time |
| **Secure Authentication** | User account management with a secure login system |

---

##  Technology Stack

- **Backend:** Python 3, Django 4.2
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, Django Templates
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions

---

##  Project Structure

```
Carbon-Emission-Calculator/
├── carbon_calculator/          # Main Django project config (settings, root URLs)
├── emission_app/               # Core app (models, views, templates)
├── carbon_emissions_schema.sql # Base SQL schema definitions
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Multi-container orchestration
├── requirements.txt            # Python dependencies
└── .github/
    └── workflows/
        └── ci.yml              # GitHub Actions CI pipeline
```

---

##  Getting Started

### Prerequisites

- Python 3.10+
- pip
- Docker & Docker Compose *(for containerized setup only)*

---

### Option 1: Local Development

**1. Clone the repository:**
```bash
git clone <repository-url>
cd Carbon-Emission-Calculator
```

**2. Create and activate a virtual environment:**
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Apply database migrations:**
```bash
python manage.py migrate
```

**5. Create a superuser** *(optional — for admin panel access)*:
```bash
python manage.py createsuperuser
```

**6. Start the development server:**
```bash
python manage.py runserver
```

The application will be available at **http://127.0.0.1:8000/**

---

### Option 2: Docker Setup

**1. Clone the repository:**
```bash
git clone <repository-url>
cd Carbon-Emission-Calculator
```

**2. Build and start the containers:**
```bash
docker-compose up --build
```

**3. Apply database migrations** *(in a separate terminal)*:
```bash
docker-compose exec web python manage.py migrate
```

**4. Create a superuser** *(optional)*:
```bash
docker-compose exec web python manage.py createsuperuser
```

The application will be available at **http://localhost:8000/**

---

## Usage

1. **Register / Login** — Create a new user account or log in with existing credentials.
2. **Dashboard** — View your high-level emission summary and track progress against active goals.
3. **Log Activity** — Navigate to the activity catalog, select an action (e.g., transportation, energy usage), input your metrics, and let the system calculate your footprint.
4. **History & Goals** — Review past entries in the history tab and set new emission reduction targets to lower your environmental impact over time.

---

##  Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m 'feat: add your feature'`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please ensure your code passes all CI checks before submitting.

---

## License

This project is licensed under the [Apache 2.0 License](LICENSE).
