import re
import asyncio
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.exceptions import OutputParserException

from app.config import get_settings

class SQLAgent:
    def __init__(self):
        self.settings = get_settings()
        self.db_uri = f"sqlite:///{self.settings.BUSINESS_DB_PATH}"
        
        # Initialize SQLDatabase wrapper from Langchain
        try:
            self.db = SQLDatabase.from_uri(self.db_uri, sample_rows_in_table_info=3)
        except Exception as e:
            print(f"Warning: Could not initialize database connection to {self.db_uri}. {e}")
            self.db = None
            
        self.llm = ChatTongyi(
            model_name="qwen-max",
            dashscope_api_key=self.settings.DASHSCOPE_API_KEY,
            temperature=0
        )
        
        if self.db:
            self.chain = create_sql_query_chain(self.llm, self.db)
        else:
            self.chain = None

    def get_database_schema(self) -> str:
        """Returns the introspected database schema info"""
        if not self.db:
            return "No database configured."
        return self.db.get_table_info()

    async def generate_sql(self, user_question: str) -> str:
        """Translates natural language to SQL using Qwen-Max"""
        if not self.chain:
            raise ValueError("SQL Agent not fully initialized (missing database).")
            
        raw_response = await self.chain.ainvoke({"question": user_question})
        return self._extract_sql(raw_response)

    def _extract_sql(self, response: str) -> str:
        """Extracts pure SQL from LLM's potentially chatty output."""
        sql = response
        if "```sql" in response:
            sql = response.split("```sql")[1].split("```")[0].strip()
        elif "SQLQuery:" in response:
            sql = response.split("SQLQuery:")[1].strip()
            if "```" in sql:
                sql = sql.split("```")[0].strip()
                
        # Additional cleanup finding SELECT
        match = re.search(r'(?i)(SELECT[\s\S]*?;)', sql)
        if match:
            sql = match.group(1)
        else:
            match = re.search(r'(?i)(SELECT[\s\S]*)', sql)
            if match:
                sql = match.group(1).split("\n\n")[0]
                
        sql = sql.strip()
        return sql

    def execute_sql(self, sql_query: str) -> dict:
        """Executes the given SQL against the target database safely."""
        if not self.db:
            raise ValueError("SQL Agent not fully initialized.")
            
        # Basic safety check
        upper_query = sql_query.upper()
        if not upper_query.startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed for safety.")
        if any(keyword in upper_query for keyword in ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "GRANT", "CREATE"]):
            raise ValueError("Data modification commands are strictly blocked.")
            
        # Ensure it has a reasonable limit
        if "LIMIT" not in upper_query:
            sql_query = sql_query.rstrip(";") + " LIMIT 500;"
            
        try:
            from sqlalchemy import text
            with self.db._engine.connect() as connection:
                result = connection.execute(text(sql_query))
                columns = list(result.keys())
                rows = [list(row) for row in result.fetchall()]
                
            return {
                "columns": columns,
                "rows": rows,
                "error": None
            }
        except Exception as e:
            return {
                "columns": [],
                "rows": [],
                "error": str(e)
            }
