# ─── 1. Import Libraries ────────────────────────────────────────────────────
import datetime
from datetime import date, datetime
import pandas as pd
from sqlalchemy import create_engine, text

# ─── 2. Connection Credentials ──────────────────────────────────────────────
#         Change these to match your MySQL server details
username  = 'username'  #here give your db user_name
password  = "password3"  #here give your db pssword 
host      = '127.0.0.1' #Give your host name 
db        = 'stgdb_banking_ram' #Give your DB name
new_db    = 'odsdb_banking_ram' #Give your new DB name

# ─── 3. Create DB Engine (pymysql driver) ───────────────────────────────────
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:3306/{db}"
)
"""
with engine.connect() as conn:
    stgdb_df = pd.read_sql(text("SELECT * FROM stg_accounts where AccountID IS NOT NULL"), conn)
    odsdb_df=pd.read_sql(text("select * from odsdb_banking_ram.ods_branches"),conn)
    print(odsdb_df)
    print(stgdb_df)
"""


with engine.connect() as conn:
    stgdb_df = pd.read_sql(text("SELECT * FROM stg_accounts where AccountID IS NOT NULL"), conn)
    #print(stgdb_df)
    odsdb_df=pd.DataFrame({
        "AccountID": stgdb_df["AccountID"],
        "AccountType": stgdb_df["AccountType"].astype(str).str.strip(),  # TRIM
        "Balance": stgdb_df["Balance"],
        "CreditScore": stgdb_df["CreditScore"],
        "Currency": stgdb_df["Currency"].astype(str).str.upper(),       # UPPER
        "CustomerID": stgdb_df["CustomerID"],
        "DateOpened": stgdb_df["DateOpened"],
        "ManagerID": stgdb_df["ManagerID"],
        "ODLimit": stgdb_df["ODLimit"],
        "load_dt": date.today(),                                      # CURRENT_DATE
        "load_ts": datetime.now()                                     # CURRENT_TIMESTAMP
    })

# --- Step 3: Insert into target table ---
    odsdb_df.to_sql(
        "ods_accounts",           # Target table name
        con=engine,
        schema=new_db,           # Target schema
        if_exists="replace",       # Append to existing data
        index=False
    )

    # --- Step 3: Load transactions ---
    stgdb_df = pd.read_sql(text("SELECT * FROM stg_transactions"), conn)
    stgdb_df["load_dt"] = date.today()
    stgdb_df["load_ts"] = datetime.now()
    stgdb_df.to_sql(
        "ods_transactions",
        con=engine,
        schema=new_db,
        if_exists="replace",
        index=False
    )

    # --- Step 4: Load payments ---
    stgdb_df = pd.read_sql(text("SELECT * FROM stg_payments"), conn)
    stgdb_df["load_dt"] = date.today()
    stgdb_df["load_ts"] = datetime.now()
    stgdb_df.to_sql(
        "ods_payments",
        con=engine,
        schema=new_db,
        if_exists="replace",
        index=False
    )

    # --- Step 5: Load creditcard ---
    stgdb_df = pd.read_sql(text("SELECT * FROM stg_creditcard"), conn)
    stgdb_df["load_dt"] = date.today()
    stgdb_df["load_ts"] = datetime.now()
    stgdb_df.to_sql(
        "ods_creditcard",
        con=engine,
        schema=new_db,
        if_exists="replace",
        index=False
    )

    # --- Step 6: Load loans ---
    stgdb_df = pd.read_sql(text("SELECT * FROM stg_loans"), conn)
    stgdb_df["load_dt"] = date.today()
    stgdb_df["load_ts"] = datetime.now()
    stgdb_df.to_sql(
        "ods_loans",
        con=engine,
        schema=new_db,
        if_exists="replace",
        index=False
    )

    # --- Step 7: Load customer profile ---
    stgdb_df = pd.read_sql(text("SELECT * FROM stg_cust_profile"), conn)
    odsdb_df = pd.DataFrame({
        "Address": stgdb_df["Address"],
        "BranchID": stgdb_df["BranchID"],
        "CustomerID": stgdb_df["CustomerID"],
        "DateOfBirth": stgdb_df["DateOfBirth"],
        "Email": stgdb_df["Email"],
        "FirstName": stgdb_df["FirstName"].astype(str).str.strip(),
        "LastName": stgdb_df["LastName"].astype(str).str.strip(),
        "PhoneNumber": stgdb_df["PhoneNumber"].astype(str).str[:20],
        "load_dt": date.today(),
        "load_ts": datetime.now()
    })

    odsdb_df.to_sql(
        "ods_cust_profile",
        con=engine,
        schema=new_db,
        if_exists="replace",
        index=False
    )

    # --- Step 8: Load branches ---
    stgdb_df = pd.read_sql(text("SELECT * FROM stg_branches"), conn)
    stgdb_df["load_dt"] = date.today()
    stgdb_df["load_ts"] = datetime.now()
    stgdb_df.to_sql(
        "ods_branches",
        con=engine,
        schema=new_db,
        if_exists="replace",
        index=False
    )

    # --- Step 9: Load employees ---
    stgdb_df = pd.read_sql(text("SELECT * FROM stg_employees"), conn)
    stgdb_df["load_dt"] = date.today()
    stgdb_df["load_ts"] = datetime.now()
    stgdb_df.to_sql(
        "ods_employees",
        con=engine,
        schema=new_db,
        if_exists="replace",
        index=False
    )

print("Data successfully loaded into all ODS tables.")
