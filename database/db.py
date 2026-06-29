import os
import sqlite3
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

# Priority:
# 1) Vercel/Neon Postgres: POSTGRES_URL or DATABASE_URL
# 2) MySQL: MYSQL_HOST etc.
# 3) Local SQLite fallback for laptop testing only
POSTGRES_URL = os.getenv("POSTGRES_URL") or os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL_NON_POOLING")
USE_POSTGRES = bool(POSTGRES_URL)
USE_MYSQL = bool(os.getenv("MYSQL_HOST") and os.getenv("MYSQL_USER") and os.getenv("MYSQL_DATABASE")) and not USE_POSTGRES

if USE_POSTGRES:
    import psycopg2
elif USE_MYSQL:
    import mysql.connector

BASE_DIR = Path(__file__).resolve().parent.parent
SQLITE_PATH = os.getenv("SQLITE_PATH", str(BASE_DIR / "zensky_local.db"))


def get_connection():
    if USE_POSTGRES:
        return psycopg2.connect(POSTGRES_URL, sslmode="require")

    if USE_MYSQL:
        return mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            autocommit=False,
        )

    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    if USE_POSTGRES:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                company VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(50) NOT NULL,
                service VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    elif USE_MYSQL:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                company VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(50) NOT NULL,
                service VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    else:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                company TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                service TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    conn.commit()
    cursor.close()
    conn.close()


def insert_contact(name, company, email, phone, service, message):
    conn = get_connection()
    cursor = conn.cursor()

    if USE_POSTGRES or USE_MYSQL:
        query = """
            INSERT INTO contacts (name, company, email, phone, service, message)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
    else:
        query = """
            INSERT INTO contacts (name, company, email, phone, service, message)
            VALUES (?, ?, ?, ?, ?, ?)
        """

    cursor.execute(query, (name, company, email, phone, service, message))
    conn.commit()
    cursor.close()
    conn.close()
