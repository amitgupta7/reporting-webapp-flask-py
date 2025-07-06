# Reporting Web Application

This repository contains a Flask-based web application for generating reports on historic appliance data. It includes utilities for syncing data, splitting CSV files, and generating reports.

## Features
- **Flask Web Server**: A web interface for visualizing appliance data.
- **Data Syncing**: Sync data between date ranges using AWS S3.
- **CSV Splitting**: Split large CSV files into smaller files for individual pods.
- **Report Generation**: Generate support reports for specific pods.

## Prerequisites
- Python 3.7 or later
- `aws-cli` installed and configured (for syncing data)
- Flask and other dependencies (installed via `make init`)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone [<repository-url>](https://github.com/amitgupta7/reporting-webapp-flask-py)
   cd reporting-webapp-flask-py
   ```
2. Install python dependencies and download the data from s3.
    ```bash
    make init
    make auth
    ## Download data for last 30 days.
    ## Alternatively, provide date range as DAYS="2024-09-26 2024-10-03" 
    make sync-ndays DAYS=30
    make split-csv
    ## This should result in .applianceDataDir/<appliance_id> folder with telemetry data for all appliances for last 30 days.
    ```
3. Generate report using cli (non interactive).
    ```bash
    ## If date range data isn't downloaded, use:
    make sync-ndays split-csv DAYS="2024-09-26 2024-10-03" 
    ## Generate applaince report for POD=58e98e10-1b19-4c84-93c0-db2ad5903b80
    make report POD=58e98e10-1b19-4c84-93c0-db2ad5903b80 DAYS="2024-09-26 2024-10-03"
    ```
    
4. Start the web application on `http://localhost:5000`
    ```bash
    make run
    ```
<img width="1725" alt="image" src="https://github.com/user-attachments/assets/f1047202-63de-493a-b336-799794c9c295" />
