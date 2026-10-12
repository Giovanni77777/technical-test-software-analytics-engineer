import os

import psycopg


def get_connection():
    return psycopg.connect(os.getenv("DATABASE_URL", "postgresql://rdp:rdp@localhost:5432/rdp"))
