from fastapi import APIRouter
from app.core.sql_agent import SQLAgent

router = APIRouter()
sql_agent = SQLAgent() # Initialize once

@router.get("/tables")
async def get_tables_info():
    """Returns the database schema info for the frontend UI."""
    schema_info = sql_agent.get_database_schema()
    return {"schema": schema_info}
