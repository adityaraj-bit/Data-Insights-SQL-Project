# User Data ETL and Insights Pipeline

## Overview
This repository contains a lightweight, dependency-free Python application that demonstrates a complete Extract, Transform, Load (ETL) pipeline. It interfaces with the JSONPlaceholder API to fetch raw user data, rigorously validates the dataset, models it into a structured relational format, and stores the output in both an SQLite database and flat CSV files. An additional insights layer provides analytical queries against the processed data.

## Project Structure
The project is built entirely on Python's standard library, ensuring maximum compatibility and zero external dependency overhead.

**Key Scripts:**
* `main.py`: The core ETL engine. It performs the sequence of downloading JSON data, validating fields, and committing the cleaned data to SQLite and CSVs.
* `insights.py`: An analytical module that connects to the generated database to generate reporting metrics (e.g., geographic spread, email domain distribution, and website classifications).

## Features
* **Zero External Dependencies:** Built entirely with `urllib`, `json`, `sqlite3`, and `csv`.
* **Data Validation:** Implements strict data quality checks, including:
  * Duplicate ID rejection.
  * Email format verification.
  * Required field enforcing (e.g., mandatory city address).
  * Zip code integrity checks.
* **Relational Database Construction:** Normalizes standard JSON into three structured tables (`users`, `addresses`, `companies`), linked with foreign keys holding referential integrity.
* **Dual Output Formats:** Generates flat-file exports alongside the SQL database for flexible downstream usage.

## Setup and Installation
Since the project relies solely on the standard library, no virtual environments or `pip` installs are necessary.

Ensure you have Python 3.8+ installed on your system.

## Usage Instructions

### 1. Data Processing
To execute the ETL pipeline, run the main script from your terminal:
```bash
python main.py
```
This will fetch the remote data, apply validation rules, and construct the `users.db` SQLite database alongside `users.csv`, `addresses.csv`, and `companies.csv`. The script will output terminal logs indicating valid inserts and any invalid records caught by the validation filters.

### 2. Analytical Insights
Once the database is populated, you can run the insights generator to view analytical reporting on the terminal:
```bash
python insights.py
```
This query module provides aggregated data such as user distribution per city, most commonly used email domain clusters, and categorization of website domains.

## Database Schema Highlights
The resulting SQLite database (`users.db`) is normalized for analytical efficiency:
* **users**: Primary table storing basic contact parameters (id, name, username, email, phone, website).
* **addresses**: Holds geographic and mailing information, linked via `user_id` to the `users` table. Includes latitude and longitude for spatial analysis.
* **companies**: Contains organizational metadata tied to users via `user_id`.
