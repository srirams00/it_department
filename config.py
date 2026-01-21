import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

db = psycopg2.connect(DATABASE_URL)
