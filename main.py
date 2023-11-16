from fastapi import FastAPI, HTTPException, Query
from fastapi.dependencies import models
from sqlalchemy.orm import sessionmaker

from database import SessionLocal
from models import Sale, Product, Inventory
from datetime import datetime, timedelta
from sqlalchemy import func, create_engine
from datetime import date

app = FastAPI()


# Endpoint to retrieve and filter sales data
@app.get("/sales")
def get_sales(date_from: str = Query(None), date_to: str = Query(None), product_id: int = None, category: str = None):
    # Parse date strings to datetime objects
    date_from = datetime.strptime(date_from, '%Y/%m/%d') if date_from else datetime.min
    date_to = datetime.strptime(date_to, '%Y/%m/%d') if date_to else datetime.now()

    db = SessionLocal()
    query = db.query(Sale)

    if product_id:
        query = query.filter(Sale.product_id == product_id)

    if category:
        query = query.join(Product).filter(Product.category == category)

    query = query.filter(Sale.sale_date >= date_from, Sale.sale_date <= date_to)
    sales = query.all()

    return sales


@app.get("/revenue")
def analyze_revenue(
    period: str = Query(..., description="Analysis period: 'daily', 'weekly', 'monthly', 'annual'"),
    start_date: date = Query(None, description="Start date in the format 'YYYY/MM/DD'"),
    end_date: date = Query(None, description="End date in the format 'YYYY/MM/DD'")
):
    # Ensure that the request parameters are correctly provided and have the expected data types.
    if period not in ["daily", "weekly", "monthly", "annual"]:
        raise HTTPException(status_code=400, detail="Invalid period")

    db = SessionLocal()

    query = db.query(Sale)

    if start_date:
        start_date = datetime.strptime(str(start_date), "%Y-%m-%d")
    if end_date:
        end_date = datetime.strptime(str(end_date), "%Y-%m-%d")
    if period == "daily":
        query = query.group_by(Sale.sale_date).with_entities(Sale.sale_date.label("date"), func.sum(Sale.revenue).label("revenue"))
    elif period == "weekly":
        query = query.group_by(func.year(Sale.sale_date), func.week(Sale.sale_date)).with_entities(func.year(Sale.sale_date).label("year"), func.week(Sale.sale_date).label("week"), func.sum(Sale.revenue).label("revenue"))
    elif period == "monthly":
        query = query.group_by(func.year(Sale.sale_date), func.month(Sale.sale_date)).with_entities(func.year(Sale.sale_date).label("year"), func.month(Sale.sale_date).label("month"), func.sum(Sale.revenue).label("revenue"))
    elif period == "annual":
        query = query.group_by(func.year(Sale.sale_date)).with_entities(func.year(Sale.sale_date).label("year"), func.sum(Sale.revenue).label("revenue"))

    revenue_data = query.all()

    return revenue_data


# Endpoint to compare revenue across different periods and categories
@app.get("/compare_revenue")
def compare_revenue(period1: str, period2: str, category: str = None):
    revenue_period1 = analyze_revenue(period1, category)
    revenue_period2 = analyze_revenue(period2, category)

    if revenue_period1["revenue"] > revenue_period2["revenue"]:
        comparison_result = f"{period1} revenue is higher than {period2} revenue"
    elif revenue_period1["revenue"] < revenue_period2["revenue"]:
        comparison_result = f"{period2} revenue is higher than {period1} revenue"
    else:
        comparison_result = f"{period1} and {period2} revenues are equal"

    return {
        "period1": revenue_period1,
        "period2": revenue_period2,
        "comparison_result": comparison_result,
    }


# Endpoint to view current inventory status
@app.get("/inventory")
def get_inventory():
    db = SessionLocal()
    inventory = db.query(Inventory).all()
    return inventory


# Functionality to update inventory levels
@app.put("/update_inventory")
def update_inventory(product_id: int, quantity: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    inventory_item = db.query(Inventory).filter(Inventory.product_id == product_id).first()

    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    # Update inventory quantity
    inventory_item.quantity = quantity

    # Implement tracking of changes over time (e.g., creating a change history entry)
    change_entry = Inventory(product_id=product_id, changed_quantity=quantity)
    db.add(change_entry)

    # Commit the changes
    db.commit()

    # Close the database session
    db.close()

    return {"message": "Inventory updated successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
