# Azure SQL Deployment Guide
**Project**: Automated Post-Hospital Patient Monitoring System  
**Author**: Graduation Project Team  
**Date**: 2026-07-10  

This guide walks through every step required to deploy the `patient_vitals` table to Azure SQL Database and load the cleaned dataset into it.

---

## Prerequisites

Before starting, ensure the following are available:

- An active **Azure subscription**
- **ODBC Driver 18 for SQL Server** installed on your local machine
  - Download: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- The local project environment fully configured (`.venv` activated, all packages installed)
- The cleaned dataset exists at: `data/processed/patient_vitals_clean.csv`

---

## Step 1: Create Azure SQL Database

1. Go to the [Azure Portal](https://portal.azure.com) and sign in.
2. In the search bar, type **SQL databases** and click the result.
3. Click **+ Create**.
4. Fill in the **Basics** tab:

   | Field | Recommended Value |
   | :--- | :--- |
   | **Subscription** | Your active subscription |
   | **Resource group** | Create new: `rg-patient-monitoring` |
   | **Database name** | `patient-monitoring-db` |
   | **Server** | Click *Create new* (see below) |
   | **Compute + storage** | Select **Basic** or **General Purpose (Serverless)** for dev/test |
   | **Backup storage redundancy** | Locally-redundant (cheapest for dev) |

5. Under **Server — Create new**:

   | Field | Value |
   | :--- | :--- |
   | **Server name** | `patient-monitoring-srv` *(must be globally unique)* |
   | **Location** | Choose the region closest to you |
   | **Authentication method** | SQL authentication |
   | **Server admin login** | e.g. `sqladmin` |
   | **Password** | A strong password (save it — you'll need it for `.env`) |

6. Click **Review + Create**, then **Create**.
7. Wait for the deployment to complete (~2–3 minutes).

---

## Step 2: Configure Firewall Rules

Azure SQL Database blocks all external connections by default. You must whitelist your IP.

1. Navigate to your newly created **SQL server** resource (not the database — the server).
2. In the left menu, click **Networking** (under *Security*).
3. Under **Firewall rules**, click **+ Add your client IPv4 address**.
   - Azure automatically detects and fills your current public IP.
4. Optionally, add the range `0.0.0.0` – `255.255.255.255` for development convenience *(not recommended for production)*.
5. Ensure **Allow Azure services and resources to access this server** is set to **Yes**.
6. Click **Save**.

---

## Step 3: Obtain the Server Name

The fully-qualified server hostname is required for the `.env` file.

1. Go to your **SQL server** resource in the Azure Portal.
2. On the **Overview** page, locate the **Server name** field.
3. It will look like:

   ```
   patient-monitoring-srv.database.windows.net
   ```

4. Copy this value — it goes into `AZURE_SQL_SERVER` in your `.env` file.

---

## Step 4: Fill the .env File

1. In the project root, copy the template:

   ```bash
   cp .env.example .env
   ```

2. Open `.env` and fill in the four required variables:

   ```env
   AZURE_SQL_SERVER=patient-monitoring-srv.database.windows.net
   AZURE_SQL_DATABASE=patient-monitoring-db
   AZURE_SQL_USERNAME=sqladmin
   AZURE_SQL_PASSWORD=YourStrongPassword123!
   ```

   > **Security Warning**: Never commit `.env` to Git. It is already listed in `.gitignore`.

---

## Step 5: Execute create_patient_vitals.sql

The table must exist in Azure SQL before the Python loader can insert data.

### Option A: Azure Portal Query Editor (no tools needed)

1. In the Azure Portal, navigate to your **SQL database** (not the server).
2. In the left menu, click **Query editor (preview)**.
3. Log in with your SQL admin credentials.
4. In the query pane, paste the entire contents of `sql/create_patient_vitals.sql`.
5. Click **Run**.
6. Expected result: `Query succeeded. Rows affected: 0.`

### Option B: SSMS or Azure Data Studio (recommended)

1. Open **SQL Server Management Studio (SSMS)** or **Azure Data Studio**.
2. Connect using:
   - **Server**: `patient-monitoring-srv.database.windows.net`
   - **Authentication**: SQL Server Authentication
   - **Login / Password**: your admin credentials
   - **Database**: `patient-monitoring-db`
3. Open a new query window.
4. Open and run the file: `sql/create_patient_vitals.sql`
5. Expected result: `Commands completed successfully.`

### Verify the table was created

Run the following in the query editor to confirm the table exists:

```sql
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
  AND TABLE_NAME = 'patient_vitals';
```

Expected result: 1 row returned with `patient_vitals`.

---

## Step 6: Run the Loading Script

With the `.env` configured and the table created, run the Python loader from the project root:

```bash
# Windows PowerShell — activate virtual environment first
.\.venv\Scripts\Activate.ps1

# Run the loader
python src/database/load_to_sql.py
```

```bash
# Linux / macOS
source .venv/bin/activate
python src/database/load_to_sql.py
```

### Expected Console Output

```
Loading cleaned dataset from: .../data/processed/patient_vitals_clean.csv
Dataset loaded successfully. Shape: 200,020 rows x 14 columns.
Aligning DataFrame column names with the SQL table schema...
Column alignment complete.
Establishing connection to Azure SQL Database...
Database connection established successfully.

Starting batch insert into [patient_vitals] (batch size: 10,000 rows)...
------------------------------------------------------------
Inserted 10,000 rows...
Inserted 20,000 rows...
Inserted 30,000 rows...
Inserted 40,000 rows...
Inserted 50,000 rows...
Inserted 60,000 rows...
Inserted 70,000 rows...
Inserted 80,000 rows...
Inserted 90,000 rows...
Inserted 100,000 rows...
Inserted 110,000 rows...
Inserted 120,000 rows...
Inserted 130,000 rows...
Inserted 140,000 rows...
Inserted 150,000 rows...
Inserted 160,000 rows...
Inserted 170,000 rows...
Inserted 180,000 rows...
Inserted 190,000 rows...
Inserted 200,000 rows...
Inserted 200,020 rows...
------------------------------------------------------------
Data successfully loaded into patient_vitals.
Total rows inserted: 200,020
```

> **Note**: Loading 200,020 rows over a network connection typically takes 3–10 minutes depending on your internet speed and the Azure SQL tier selected.

---

## Step 7: Verify the Inserted Rows

After the loading script completes, run the following query in the Azure Portal Query Editor or SSMS to confirm all rows were inserted:

```sql
SELECT COUNT(*) AS total_rows
FROM dbo.patient_vitals;
```

**Expected result**: `200020`

For a more detailed verification, run the full suite of queries in `sql/verification_queries.sql`.

---

## Troubleshooting

| Error | Likely Cause | Resolution |
| :--- | :--- | :--- |
| `[ERROR] Database connection failed` | Wrong server name, username, or password | Double-check `.env` values match Azure Portal |
| `Login failed for user` | Incorrect credentials | Re-check `AZURE_SQL_USERNAME` and `AZURE_SQL_PASSWORD` |
| `Cannot open server requested by the login` | Database name is wrong | Verify `AZURE_SQL_DATABASE` matches the database name in Azure |
| `TCP Provider: No connection could be made` | Firewall not configured | Add your client IP in Azure SQL Networking → Firewall rules |
| `Invalid object name 'dbo.patient_vitals'` | Table was not created | Run `sql/create_patient_vitals.sql` first |
| `[ERROR] Cleaned dataset not found` | CSV missing | Run `python src/cleaning/clean_data.py` first |
