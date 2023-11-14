from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Sale  # Import your SQLAlchemy model

# Define your database URL
DATABASE_URL = "mysql+pymysql://your_username:your_password@localhost/hanifbaloch"
# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the 'sales' table in the database
Base.metadata.create_all(bind=engine)

# Now you can use the Sale model to interact with the 'sales' table
