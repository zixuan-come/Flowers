import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://flowers:flowers123@localhost:3306/flowers")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "flowers666")





