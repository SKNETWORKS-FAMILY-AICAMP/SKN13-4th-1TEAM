import os
from sqlalchemy import create_engine

HOST = os.getenv("MYSQL_HOST")
PORT = os.getenv("MYSQL_PORT")
USER = os.getenv("MYSQL_USER")
PASS = os.getenv("MYSQL_PASSWORD")
DB = os.getenv("MYSQL_DATABASE")

engine = create_engine(f"mysql+pymysql://{USER}:{PASS}@{HOST}:{PORT}/{DB}")
# engine = create_engine(f"mysql+pymysql://root:password@localhost:3306/{DB}")
