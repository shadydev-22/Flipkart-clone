from database import engine, Base
from models import *

def init_db():
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating new tables...")
    Base.metadata.create_all(bind=engine)
    print("Database re-initialized successfully.")

if __name__ == "__main__":
    init_db()
