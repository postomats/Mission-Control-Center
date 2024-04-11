from fastapi import FastAPI
from .routers import admin, order, catalog, index


app = FastAPI(title="Mission control center")
app.include_router(index.router, tags=["healcheck"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(order.router, prefix="/order", tags=["order"])
app.include_router(catalog.router, prefix="/catalog", tags=["catalog"])
