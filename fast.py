from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Product, Sale, Inventory, Promotion
from datetime import datetime
import random

# Replace 'mysql://username:password@localhost/database' with your MySQL connection string.
DATABASE_URL = "mysql+pymysql://your_username:your_password@localhost/hanifbaloch"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_dummy_data():
    # Create tables if they don't exist
    Product.__table__.create(bind=engine, checkfirst=True)
    Sale.__table__.create(bind=engine, checkfirst=True)
    Inventory.__table__.create(bind=engine, checkfirst=True)
    Promotion.__table__.create(bind=engine, checkfirst=True)

    session = SessionLocal()

    # Create some products
    products = [
        Product(name="Product A", description="Description A", category="Category 1"),
        Product(name="Product B", description="Description B", category="Category 2"),
        Product(name="Product C", description="Description C", category="Category 1"),
    ]

    for product in products:
        session.add(product)

    # Create some sales
    sales = []
    for _ in range(10):
        sale = Sale(
            sale_date=datetime.now(),
            quantity=random.randint(1, 10),
            revenue=random.uniform(10.0, 100.0),
            product=random.choice(products)
        )
        sales.append(sale)

    session.add_all(sales)

    # Create some inventory data
    inventory_items = []
    for product in products:
        inventory = Inventory(
            product=product,
            quantity=random.randint(50, 100),
            alert_threshold=20
        )
        inventory_items.append(inventory)

    session.add_all(inventory_items)

    # Create some promotions
    promotions = [
        Promotion(description="Promotion 1", discount=0.1),
        Promotion(description="Promotion 2", discount=0.2),
    ]

    for promotion in promotions:
        session.add(promotion)

    session.commit()
    session.close()


if __name__ == "__main__":
    create_dummy_data()
