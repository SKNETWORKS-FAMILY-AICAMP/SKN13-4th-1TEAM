import os
from sqlalchemy import create_engine

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASS = os.getenv("PASS")
DB = os.getenv("DB")

engine = create_engine(f"mysql+pymysql://{USER}:{PASS}@{HOST}:{PORT}/{DB}")
# engine = create_engine(f"mysql+pymysql://root:password@localhost:3306/{DB}")