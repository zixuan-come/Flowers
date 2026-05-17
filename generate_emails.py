# ============ Configuration ============
PREFIX = "cc"          # Email prefix, e.g. "zx" -> zx0@139.com, "zxx" -> zxx0@139.com
DOMAIN = "139.com"     # Email domain
BEGIN = 0              # Start index (inclusive)
END = 1000          # End index (exclusive), total = END - BEGIN
OUTPUT_FILE = "emails.csv"
# ========================================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("email\n")
    for i in range(BEGIN, END):
        f.write(f"{PREFIX}{i}@{DOMAIN}\n")

print(f"Done. Generated {END - BEGIN} emails -> {OUTPUT_FILE}")


