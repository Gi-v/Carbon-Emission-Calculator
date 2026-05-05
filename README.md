# Carbon Emission Calculator

## Motivation and Background
As environmental sustainability becomes a critical global priority, there is a pressing need for accessible tools that accurately quantify carbon emissions. This project was developed to provide an interpretable, data-driven approach to tracking and managing environmental impact. By utilizing custom emission factors and robust data modeling, the platform bridges the gap between complex emission quantification methods and everyday user activities. The ultimate goal is to empower users to make informed decisions, understand the environmental cost of their actions, and actively reduce their carbon footprint through manageable goals.

## Overview
The Carbon Emission Calculator is a comprehensive web-based tracking system designed to securely log daily activities, calculate associated greenhouse gas emissions, and actively monitor reduction targets. Built with a focus on delivering a highly interpretable reporting interface, this platform allows individuals or organizations to seamlessly integrate sustainability tracking into their routines.

## Key Features
* **Activity Catalog:** Log various emission-generating activities using a robust catalog configured with custom emission factors for precise calculations.
* **Interpretable Reporting:** A centralized dashboard providing a clear, high-level overview of total emissions, recent activities, and progress against environmental targets.
* **Goal Management:** Establish, track, and achieve customized emission reduction goals.
* **Historical Tracking:** Detailed logs and history views to analyze emission trends and data models over time.
* **Secure Authentication:** User account management and a secure login system to keep record management private.

## Technology Stack
* **Backend:** Python 3, Django 4.2
* **Database:** SQLite (optimized for core data modeling and record management)
* **Frontend:** HTML5, CSS3, Django Templates
* **Containerization:** Docker, Docker Compose
* **Continuous Integration:** GitHub Actions

## Project Structure
* `carbon_calculator/`: Main Django project configuration, including settings and core URL routing.
* `emission_app/`: The primary application module containing data models, views, and frontend templates.
* `carbon_emissions_schema.sql`: Base SQL schema definitions.
* `Dockerfile` & `docker-compose.yml`: Configuration files for containerized deployment.
* `.github/workflows/ci.yml`: Continuous integration pipeline configurations.

## Installation and Setup

### Prerequisites
* Python 3.10+
* pip (Python package installer)
* Docker and Docker Compose (for containerized setup)

### Option 1: Local Development Setup
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Carbon-Emission-Calculator
  
   
