import sqlite3

# Connect to DB
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

print("INSIGHTS FROM DATABASE\n")

# -------------------------------
# 1. Users per City
# -------------------------------
print("Users per City:")
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
print("Email Domain Distribution:")
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
print("Website Types:")
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
print("Geographic Spread:")
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
print("Users per Company:")
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


print("Zipcode Format Consistency:")

cursor.execute("""
SELECT 
    LENGTH(zipcode),
    COUNT(*)
FROM addresses
GROUP BY LENGTH(zipcode);
""")

for row in cursor.fetchall():
    print(row)

print("👉 Insight: Zipcodes vary in format → dataset includes mixed standards.\n")
print("-"*50)




print("Phone Format Patterns:")

cursor.execute("""
SELECT 
    CASE 
        WHEN phone LIKE '%(%' THEN 'Bracket Format'
        WHEN phone LIKE '%.%' THEN 'Dot Format'
        WHEN phone LIKE '%-%' THEN 'Dash Format'
        ELSE 'Other'
    END as format,
    COUNT(*)
FROM users
GROUP BY format;
""")

for row in cursor.fetchall():
    print(row)

print("👉 Insight: Multiple phone formats detected → useful for testing normalization systems.\n")
print("-"*50)


print("Longitude Segmentation:")

cursor.execute("""
SELECT 
    CASE 
        WHEN lng >= 0 THEN 'Eastern'
        ELSE 'Western'
    END as region,
    COUNT(*)
FROM addresses
GROUP BY region;
""")

rows = cursor.fetchall()
print(rows)

print("-"*50)

print("Latitude Segmentation:")

cursor.execute("""
SELECT 
    CASE 
        WHEN lat >= 0 THEN 'Northern Hemisphere'
        ELSE 'Southern Hemisphere'
    END as hemisphere,
    COUNT(*)
FROM addresses
GROUP BY hemisphere;
""")

rows = cursor.fetchall()
print(rows)
# Close connection
conn.close()

print("✅ Analysis Complete!")