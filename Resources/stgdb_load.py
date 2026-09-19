# ─── 1. Import Libraries ────────────────────────────────────────────────────
import pandas as pd
from sqlalchemy import create_engine, text

# ─── 2. Connection Credentials ──────────────────────────────────────────────
#         Change these to match your MySQL server details
username  = 'username'  #here give your db user_name
password  = "password3"  #here give your db pssword 
host      = '127.0.0.1' #Give your host name 
db        = 'stgdb_banking_ram' #Give your DB name

# ─── 3. Create DB Engine (pymysql driver) ───────────────────────────────────
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:3306/{db}"
)

# Retrieve as DataFrame
with engine.connect() as conn:
    df = pd.read_sql(text("SELECT * FROM stg_branches"), conn)

print(df)

#SELECT * FROM table
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM stg_branches"))
    for row in result:
        print(dict(row._mapping))  # Convert Row object to dictionary


# ─── 4. Source Folder Path ──────────────────────────────────────────────────
#         Change this to where you dataset files
folder = "D:\\RAM\\Banking\\data\\"  # double \\ for escape sequence

# ─── 5. Table → File Mapping Dictionary ─────────────────────────────────────
#        Key   = target staging table name in MySQL
#        Value = full path to the source CSV file
table_file_dict = {
    "stg_transactions" : folder + "transactions.csv",
    "stg_accounts"     : folder + "accounts.csv",
    "stg_payments"     : folder + "payments.csv",
    "stg_creditcard"   : folder + "creditcard.csv",
    "stg_loans"        : folder + "loans.csv",
    "stg_cust_profile" : folder + "cust.csv",
    "stg_branches"     : folder + "branches.csv",
    "stg_employees"    : folder + "employee.csv",
}

# print(table_file_dict) to read filelocation

# ─── 6. Loop & Load ─────────────────────────────────────────────────────────
#        Iterates 8 times (one per dictionary entry)
#        Each iteration: reads CSV → loads to MySQL staging table
for table, file in table_file_dict.items():
    # Read CSV into a pandas DataFrame (in-memory table)
    df = pd.read_csv(file)

    ## Optional: filter/transform before loading, e.g.:
    ## if table == 'stg_branches':
    ##     df = df.query("BranchID == 130")

    # Load DataFrame → MySQL staging table (replace if already exists)
    df.to_sql(table, con=engine, index=False, if_exists="replace")

    print(f"Rows loaded into table: {table}")
