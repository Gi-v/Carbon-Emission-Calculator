# 🌿 Carbon Emission Calculator

A web-based application built with **Django** that helps users track and manage their carbon emissions from daily activities. The project uses **SQLite** as its database management system to store activity types and emission records.

## 📌 About

This project allows users to:
- Log carbon-emitting activities (e.g., car travel, electricity usage)
- Automatically calculate CO₂ emissions based on predefined emission factors
- View a dashboard with summary statistics and a 7-day emission chart
- Browse and manage emission history
- Add custom activity types with their own emission factors

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, Django 4.2 |
| Database (DBMS) | SQLite3 |
| Frontend | HTML, Django Templates |
| Server | Gunicorn, Whitenoise |

## 🗄️ Database Schema

### ActivityType
| Field | Type | Description |
|-------|------|-------------|
| activity_name | CharField | Name of the activity (unique) |
| emission_factor | FloatField | kg CO₂ emitted per unit |
| unit | CharField | Unit of measurement (e.g., km, kWh) |

### EmissionRecord
| Field | Type | Description |
|-------|------|-------------|
| activity | ForeignKey | Links to an ActivityType |
| quantity | FloatField | Amount of activity performed |
| emission_amount | FloatField | Calculated CO₂ in kg (auto-computed) |
| date | DateField | Date of the activity |
| description | TextField | Optional notes |
| created_at | DateTimeField | Timestamp of record creation |


## 📄 Pages

| Page | URL | Description |
|------|-----|-------------|
| Dashboard | `/` | Overview with stats, top activities, and 7-day chart |
| Activity | `/activity/` | Add new emission records and activity types |
| History | `/history/` | View and delete past emission records |

## 📦 Dependencies

- Django 4.2.9
- python-decouple
- gunicorn
- whitenoise
- matplotlib
- pandas

## 📝 License

This project is licensed under the terms included in the [LICENSE](LICENSE) file.
