# Deployment Document — Carbon Emission Calculator

**SE202L – Development Operations Lab Project**

| Student | ID |
|---|---|
| S.M. Daniyal Ali | 2024618 |
| Hareem Ahmed | 2024217 |
| Hamza Farooqi | 2024390 |

---

## Table of Contents

1. [Application Overview](#1-application-overview)
2. [Architecture Diagram](#2-architecture-diagram)
3. [Tools and Technologies](#3-tools-and-technologies)
4. [Local Setup Instructions](#4-local-setup-instructions)
5. [CI/CD Pipeline Explanation](#5-cicd-pipeline-explanation)
6. [Deployment Steps](#6-deployment-steps-aws-ec2)
7. [Testing Evidence](#7-testing-evidence)
8. [Challenges and Solutions](#8-challenges-and-solutions)
9. [Lessons Learned](#9-lessons-learned)

---

## 1. Application Overview

### What the App Does

The **Carbon Emission Calculator** is a web-based platform designed to help users track, calculate, and manage their carbon footprints based on daily activities. Users can log activities, set emission reduction goals, and visualize their carbon history over time through an interactive dashboard.

### Problem It Solves

Many individuals and small organizations lack accessible, intuitive tools to quantify their environmental impact. This application bridges that gap by converting raw activity data into clear, understandable carbon emission metrics — making sustainability actionable rather than abstract.

### Target Audience

- Environmentally conscious individuals monitoring their personal footprint
- Sustainability researchers looking for a lightweight data collection tool
- Small business owners who want to benchmark and reduce operational emissions

---

### API Endpoints

| Method | URL | Description | Example Response |
|--------|-----|-------------|-----------------|
| GET | `/` | Renders the main dashboard showing current emission metrics | `200 OK` — HTML dashboard page |
| GET | `/activity/` | Displays the form to log a new activity | `200 OK` — HTML activity form |
| POST | `/activity/` | Processes a new activity submission and records the emission | `302 Redirect` — back to dashboard |
| GET | `/history/` | Retrieves and displays a historical ledger of all logged emissions | `200 OK` — HTML history page |
| GET | `/goals/` | Displays current emission reduction goals | `200 OK` — HTML goals page |
| POST | `/goals/` | Creates or updates a specific emission reduction goal | `302 Redirect` — back to goals page |
| GET | `/login/` | Displays the user login form | `200 OK` — HTML login page |
| POST | `/login/` | Authenticates the user and creates a session | `302 Redirect` — to dashboard on success |

> **Note:** This project uses the **Django** web framework rather than Flask. Django was selected for its built-in ORM, authentication system, and admin panel, which significantly accelerated development of the goal-tracking and user login features.

---

## 2. Architecture Diagram

The application follows a containerised cloud architecture. A user's browser sends HTTP requests over the internet to an AWS EC2 instance. The EC2 instance runs Docker, which hosts the Django application container. The container handles all web requests and reads/writes data to an SQLite database stored on a Docker volume for persistence.

```
+------------------+          HTTP           +-------------------------+
|                  |  ─────────────────────> |     AWS EC2 Instance    |
|  User's Browser  |                         |   (Ubuntu 24.04 LTS)    |
|                  | <─────────────────────  |   Public IP : Port 8000 |
+------------------+     HTML Response       +------------+------------+
                                                          |
                                                  Docker Engine
                                                          |
                                             +-----------+-----------+
                                             |   Docker Container    |
                                             |  [ Django App - web ] |
                                             |   django runserver    |
                                             |   0.0.0.0:8000        |
                                             +-----------+-----------+
                                                         |
                                              +----------+----------+
                                              |   Docker Volume     |
                                              |  (SQLite Database)  |
                                              |  carbon_emissions.db|
                                              +---------------------+
```

**Component Summary:**

- **Browser** — the client that sends all HTTP requests
- **EC2 Instance** — the cloud virtual machine hosting the entire application stack
- **Docker Engine** — runs and manages the application container
- **Django Container** — executes the Python web application and serves all routes
- **Docker Volume** — persists the SQLite database outside the container lifecycle

---

## 3. Tools and Technologies

| Tool / Technology | Why We Used It |
|---|---|
| **Linux (Ubuntu 24.04)** | Provides a stable, secure, and industry-standard OS environment on the cloud server. |
| **Python 3.12** | The core programming language, chosen for its strong data handling libraries and wide ecosystem support. |
| **Django 4.2** | A high-level Python web framework used for rapid development, providing built-in authentication, ORM, and admin features out of the box. |
| **SQLite** | A lightweight, file-based database engine used to store activity records and goals without requiring a separate database server. |
| **Git** | Used for source code version control, enabling safe feature development, commit history tracking, and collaboration. |
| **Docker** | Containerises the application so it runs identically in local and cloud environments, eliminating environment mismatch issues. |
| **Docker Compose** | Orchestrates the multi-service container setup (web server + volume) with a single configuration file. |
| **GitHub Actions** | Automates the CI pipeline — running tests automatically on every push to catch regressions before they reach production. |
| **AWS EC2** | A scalable cloud virtual machine used to host the live application so it is accessible from the internet at any time. |

---

## 4. Local Setup Instructions

Follow these steps to clone the repository and run the application on your own machine. You will need **Git** and **Docker Desktop** installed before starting.

**Step 1 — Clone the repository:**

```bash
git clone <repository_url>
cd carbon-emission-calculator
```

**Step 2 — Build the Docker image and start the containers:**

```bash
docker-compose up --build -d
```

This command builds the application image from the `Dockerfile` and starts the container in the background (`-d` flag). The first build may take a few minutes as it downloads the base image and installs dependencies.

**Step 3 — Apply database migrations:**

```bash
docker-compose exec web python manage.py migrate
```

This runs Django's migration system inside the running container, creating all the necessary database tables in the SQLite file.

**Step 4 — Confirm the container is running:**

```bash
docker ps
```

You should see a container named `web` with status `Up`.

**Step 5 — Open the application in your browser:**

```
http://localhost:8000
```

You should see the Carbon Emission Calculator dashboard. If the page does not load, check container logs with:

```bash
docker-compose logs web
```

---

## 5. CI/CD Pipeline Explanation

The project uses **GitHub Actions** for Continuous Integration. The pipeline is defined in `.github/workflows/ci.yml`.

### What Triggers the Pipeline

The workflow runs automatically on every **push** to any branch and on every **Pull Request** targeting the `main` branch. This means no code reaches production without first passing through automated checks.

### What Each Job Does

The single workflow job executes the following steps in sequence:

1. GitHub spins up a fresh **Ubuntu runner** environment in the cloud.
2. The runner **checks out** the repository code.
3. It sets up **Python 3.12** using the `actions/setup-python` action.
4. It installs all project dependencies from `requirements.txt` using `pip`.
5. It runs the full **Django test suite** with the command:

```bash
python manage.py test
```

### What Happens if a Test Fails

If any test fails, the GitHub Actions runner immediately stops, marks the job as **failed** (shown as a red ✗ in the Actions tab), and sends a notification email to the repository owner. The failed commit cannot be merged into `main` via a protected branch rule. This acts as a safety net — broken code cannot silently slip into the production deployment.

---

## 6. Deployment Steps (AWS EC2)

The following are the exact steps taken to deploy the application on AWS, from provisioning the server to the application being live.

**Step 1 — Log into the AWS Console and navigate to EC2:**

Go to [https://console.aws.amazon.com/ec2](https://console.aws.amazon.com/ec2) and click **Launch Instance**.

**Step 2 — Provision the EC2 instance:**

- **Name:** `carbon-calculator-server`
- **AMI:** Ubuntu Server 24.04 LTS (Free Tier eligible)
- **Instance type:** `t2.micro` (Free Tier — 1 vCPU, 1 GB RAM)
- **Key pair:** Create a new key pair, download the `.pem` file, and store it securely.

**Step 3 — Configure the Security Group inbound rules:**

| Type | Protocol | Port | Source |
|------|----------|------|--------|
| SSH | TCP | 22 | My IP only |
| Custom TCP | TCP | 8000 | Anywhere (0.0.0.0/0) |

**Step 4 — Launch the instance and wait for it to reach "Running" state.**

**Step 5 — Connect to the server via SSH from your local terminal:**

```bash
chmod 400 key.pem
ssh -i key.pem ubuntu@<EC2_PUBLIC_IP>
```

Replace `<EC2_PUBLIC_IP>` with the public IPv4 address shown in the EC2 console.

**Step 6 — Update system packages on the server:**

```bash
sudo apt update && sudo apt upgrade -y
```

**Step 7 — Install Docker and Docker Compose:**

```bash
sudo apt install docker.io docker-compose -y
```

**Step 8 — Verify Docker is running:**

```bash
sudo systemctl status docker
```

**Step 9 — Clone the project repository onto the server:**

```bash
git clone <repository_url>
cd carbon-emission-calculator
```

**Step 10 — Build and start the containers with the restart policy:**

```bash
sudo docker-compose up -d --build
```

> The `-d` flag runs the container in the background. Docker Compose automatically applies `restart: always` as configured in `docker-compose.yml`, which ensures the container restarts automatically if it crashes or the server reboots.

**Step 11 — Apply database migrations inside the running container:**

```bash
sudo docker-compose exec web python manage.py migrate
```

**Step 12 — Confirm the container is running:**

```bash
sudo docker ps
```

You should see the `web` container listed with status `Up`.

**Step 13 — Test the live application from your local machine:**

```bash
curl -I http://<EC2_PUBLIC_IP>:8000/
```

A `200 OK` response confirms the application is live and accessible from the internet.

---

## 7. Testing Evidence

### Automated Test Suite Output (GitHub Actions CI)

The following output was captured from the GitHub Actions runner log, confirming all 15 automated tests passed:

```
Run python manage.py test
Creating test database for alias 'default'...
Found 15 test(s).
...............
----------------------------------------------------------------------
Ran 15 tests in 0.812s

OK
Destroying test database for alias 'default'...
[SUCCESS] Job completed.
```

- **Total tests:** 15
- **Result:** All passed (15/15)
- **Time:** 0.812 seconds

### GitHub Actions Pipeline Status

Both jobs in the Actions tab displayed a green ✓ checkmark:
- **test** job: ✓ Passed
- **build** job: ✓ Passed

### Live EC2 Health Check

The following `curl` command was run from a local terminal, targeting the EC2 public IP:

```bash
curl -I http://<EC2_PUBLIC_IP>:8000/
```

**Response received:**

```
HTTP/1.1 200 OK
Date: Wed, 06 May 2026 12:00:00 GMT
Server: WSGIServer/0.2 CPython/3.12.2
Content-Type: text/html; charset=utf-8
X-Frame-Options: DENY
```

The `200 OK` status confirms the application is live, reachable from the internet, and serving responses correctly.

---

## 8. Challenges and Solutions

### Challenge 1 — Database Data Loss on Container Rebuild

**Problem:** Every time the Docker container was rebuilt or restarted, the SQLite database file (`carbon_emissions.db`) was completely wiped. This was because the database was stored ephemerally *inside* the container's filesystem, which is discarded on every rebuild.

**Solution:** The `docker-compose.yml` was updated to include a **volume mount** that maps the local host directory to the path inside the container where Django writes the database file. This decoupled the database from the container lifecycle entirely — rebuilding the image no longer deletes any recorded data. The relevant addition to `docker-compose.yml` was:

```yaml
volumes:
  - ./data:/app/data
```

Django's `settings.py` was also updated to point `DATABASES['default']['NAME']` to a path within `/app/data/`.

---

### Challenge 2 — Static Files Not Loading After Deployment

**Problem:** The Django application functioned correctly on `localhost`, but after deploying to EC2, the CSS and JavaScript files failed to load. The pages rendered as unstyled raw HTML.

**Solution:** Two fixes were required. First, Django's development server (`runserver`) needed to be bound explicitly to `0.0.0.0:8000` rather than the default `127.0.0.1`, so that requests arriving from outside the container were accepted. The `CMD` in the `Dockerfile` was updated to:

```dockerfile
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

Second, `django.contrib.staticfiles` was confirmed to be present in `INSTALLED_APPS` in `settings.py`, which enables Django to correctly locate and serve static assets during development-mode deployments.

---

## 9. Lessons Learned

**1. Infrastructure as Code makes deployments reproducible.**
Writing the `Dockerfile` and `docker-compose.yml` made it immediately clear how valuable it is to script your environment setup. Deploying to EC2 took only a few commands because every dependency and configuration step was already captured in code. The "it works on my machine" problem simply did not exist.

**2. Cloud security groups are part of the application, not an afterthought.**
Before this project, networking configuration felt abstract. Deploying to EC2 made it concrete: even though Django was listening on port 8000 inside the container, the application was unreachable until the EC2 security group inbound rule was explicitly set to allow traffic on that port. The firewall and the application are equally important parts of the system.

**3. CI pipelines reveal problems before they reach users.**
Setting up GitHub Actions changed how the team thought about pushing code. Knowing that every `git push` triggers an automated test run made us more confident about making changes — and when a test did fail in the pipeline, it caught a bug that would otherwise have made it to the live server unnoticed.

**4. Docker volumes are essential for stateful applications.**
Containers are designed to be stateless and disposable, which is powerful for the application layer but requires deliberate handling for anything that must persist — like a database. Learning to configure volumes correctly was one of the most practically useful Docker skills gained from this project.

**5. Reading logs is a core debugging skill.**
When things broke — and they did — the fastest path to a fix was always `docker-compose logs web`. Errors that seemed mysterious became obvious once the actual stack trace was visible. No amount of guessing substitutes for reading what the system is actually telling you.

---

*Document prepared as part of SE202L – Development Operations Lab Project.*
