import sqlite3

# Connect to DB
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

print("📊 INSIGHTS FROM DATABASE\n")

# -------------------------------
# 1. Users per City
# -------------------------------
print("1️⃣ Users per City:")
cursor.execute("""
SELECT city, COUNT(*) as total_users
FROM addresses
GROUP BY city
ORDER BY total_users DESC;
""")

rows = cursor.fetchall()
for row in rows:
    print(row)

print("👉 Insight: Shows how users are distributed across cities.")
print("👉 In this dataset, each city has 1 user → no dominant location.\n")

print("-"*50)

# -------------------------------
# 2. Email Domain Analysis
# -------------------------------
print("2️⃣ Email Domain Distribution:")
cursor.execute("""
SELECT 
    SUBSTR(email, INSTR(email, '@') + 1) AS domain,
    COUNT(*) as count
FROM users
GROUP BY domain
ORDER BY count DESC;
""")

rows = cursor.fetchall()
for row in rows:
    print(row)

print("👉 Insight: Identifies most commonly used email providers.")
print("👉 Here, domains are diverse → no single provider dominates.\n")

print("-"*50)

# -------------------------------
# 3. Website Type Distribution
# -------------------------------
print("3️⃣ Website Types:")
cursor.execute("""
SELECT 
    CASE 
        WHEN website LIKE '%.com' THEN 'Commercial'
        WHEN website LIKE '%.org' THEN 'Organization'
        WHEN website LIKE '%.net' THEN 'Network'
        ELSE 'Other'
    END as type,
    COUNT(*) as count
FROM users
GROUP BY type;
""")

rows = cursor.fetchall()
for row in rows:
    print(row)

print("👉 Insight: Classifies users based on website type (.com, .org, etc).")
print("👉 Shows a balanced mix → dataset represents different web categories.\n")

print("-"*50)

# -------------------------------
# 4. Geographic Spread
# -------------------------------
print("4️⃣ Geographic Spread:")
cursor.execute("""
SELECT 
    MIN(lat), MAX(lat),
    MIN(lng), MAX(lng)
FROM addresses;
""")

row = cursor.fetchone()
print(f"Latitude Range: {row[0]} to {row[1]}")
print(f"Longitude Range: {row[2]} to {row[3]}")

print("👉 Insight: Shows how geographically spread the users are.")
print("👉 Wide range → users are globally distributed.\n")

print("-"*50)

# -------------------------------
# 5. Users per Company
# -------------------------------
print("5️⃣ Users per Company:")
cursor.execute("""
SELECT name, COUNT(*) 
FROM companies
GROUP BY name;
""")

rows = cursor.fetchall()
for row in rows:
    print(row)

print("👉 Insight: Shows how many users belong to each company.")
print("👉 Each company has 1 user → no company dominance.\n")

print("-"*50)

# Close connection
conn.close()

print("✅ Analysis Complete!")