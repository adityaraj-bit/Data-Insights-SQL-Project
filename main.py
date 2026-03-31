import json
import sqlite3
import csv
import urllib.request

# ---- STEP 1: LOAD JSON ----
url = "https://jsonplaceholder.typicode.com/users"
response = urllib.request.urlopen(url)
data = json.loads(response.read().decode('utf-8'))

# ---- STEP 2: CONNECT TO SQLITE ----
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

# ---- STEP 3: CREATE TABLES ----
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    username TEXT,
    email TEXT,
    phone TEXT,
    website TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    street TEXT,
    suite TEXT,
    city TEXT,
    zipcode TEXT,
    lat REAL,
    lng REAL,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    catchPhrase TEXT,
    bs TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# ---- STEP 4: PREPARE CSV FILES ----
users_file = open("users.csv", "w", newline='', encoding="utf-8")
addresses_file = open("addresses.csv", "w", newline='', encoding="utf-8")
companies_file = open("companies.csv", "w", newline='', encoding="utf-8")

users_writer = csv.writer(users_file)
addresses_writer = csv.writer(addresses_file)
companies_writer = csv.writer(companies_file)

# Write headers
users_writer.writerow(["id", "name", "username", "email", "phone", "website"])
addresses_writer.writerow(["user_id", "street", "suite", "city", "zipcode", "lat", "lng"])
companies_writer.writerow(["user_id", "name", "catchPhrase", "bs"])

# ---- VALIDATION HELPERS ----
seen_user_ids = set()

def is_valid_user(user):
    # 1. Duplicate ID check
    if user["id"] in seen_user_ids:
        print(f"❌ Duplicate user id: {user['id']}")
        return False
    seen_user_ids.add(user["id"])

    # 2. Email validation
    if "@" not in user.get("email", ""):
        print(f"❌ Invalid email for user id {user['id']}")
        return False

    # Address checks
    address = user.get("address", {})
    
    # 3. City null check
    if not address.get("city"):
        print(f"❌ Missing city for user id {user['id']}")
        return False

    # 4. Zipcode length check
    zipcode = address.get("zipcode", "")
    digits_only = ''.join(filter(str.isdigit, zipcode))
    if len(digits_only) < 5:
        print(f"❌ Invalid zipcode for user id {user['id']}")
        return False

    return True

# ---- STEP 5: INSERT DATA + WRITE CSV ----
for user in data:

    if not is_valid_user(user):
        continue  # Skip invalid records

    # USERS
    user_row = (
        user["id"],
        user["name"],
        user["username"],
        user["email"],
        user["phone"],
        user["website"]
    )

    cursor.execute("""
    INSERT INTO users (id, name, username, email, phone, website)
    VALUES (?, ?, ?, ?, ?, ?)
    """, user_row)

    users_writer.writerow(user_row)

    # ADDRESSES
    address = user["address"]
    geo = address["geo"]

    address_row = (
        user["id"],
        address["street"],
        address["suite"],
        address["city"],
        address["zipcode"],
        float(geo["lat"]),
        float(geo["lng"])
    )

    cursor.execute("""
    INSERT INTO addresses (user_id, street, suite, city, zipcode, lat, lng)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, address_row)

    addresses_writer.writerow(address_row)

    # COMPANIES
    company = user["company"]

    company_row = (
        user["id"],
        company["name"],
        company["catchPhrase"],
        company["bs"]
    )

    cursor.execute("""
    INSERT INTO companies (user_id, name, catchPhrase, bs)
    VALUES (?, ?, ?, ?)
    """, company_row)

    companies_writer.writerow(company_row)

# ---- STEP 6: CLEANUP ----
conn.commit()
conn.close()

users_file.close()
addresses_file.close()
companies_file.close()

print("✅ Valid data saved to SQLite AND CSV files!")