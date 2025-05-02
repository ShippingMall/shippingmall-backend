import logging
from fastapi import FastAPI
from sqlalchemy import inspect
from app.database import engine, Base
from app.routes import shipment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
def startup_event():
    logger.info("🚀 Starting ShippingMall Backend API...")
    logger.info("🔧 Creating all database tables if not exist...")
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    if table_names:
        for table in table_names:
            logger.info(f"📦 Table ready: {table}")
            columns = inspector.get_columns(table)
            for col in columns:
                col_info = f" └── {col['name']} ({col['type']})"
                logger.info(col_info)
    else:
        logger.warning("⚠️ No tables found after initialization!")

app.include_router(shipment.router, prefix="/shipments", tags=["Shipments"])

@app.get("/")
def read_root():
    return {"message": "🚀 ShippingMall Backend API is live"}
