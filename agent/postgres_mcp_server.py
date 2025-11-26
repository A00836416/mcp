import os
import sys
import logging
import psycopg2
import psycopg2.extras
import re
from urllib.parse import urlparse
from fastmcp import FastMCP

# ---------------------------
#   CONFIGURAR LOGGING → stderr
# ---------------------------
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------
#   INICIO DEL MCP SERVER
# ---------------------------
server = FastMCP("postgres-server")


# ---------------------------
#   FUNCIÓN REAL DE QUERY
# ---------------------------

def run_query(sql: str):
    url = os.getenv("SUPABASE_DB_URL")
    if not url:
        return {"ok": False, "error": "Missing SUPABASE_DB_URL"}

    parsed = urlparse(url)

    try:
        with psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path.lstrip("/"),
            user=parsed.username,
            password=parsed.password,
            sslmode="require"
        ) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(sql)

                try:
                    rows = cur.fetchall()
                    return {"ok": True, "rows": [dict(r) for r in rows]}
                except psycopg2.ProgrammingError:
                    return {"ok": True, "rows": []}

    except Exception as e:
        logger.error(f"DB error: {e}")
        return {"ok": False, "error": str(e)}


# ---------------------------
#   TOOL ÚNICA: query()
# ---------------------------

@server.tool()
async def query(sql: str):
    """
    Ejecuta solo consultas SQL de lectura (SELECT).
    Bloquea cualquier comando peligroso.
    """
    sql_lower = sql.lower().strip()

    # Solo SELECT
    if not sql_lower.startswith("select"):
        return {"ok": False, "error": "Only SELECT queries are allowed"}

    # Detectar comandos peligrosos
    dangerous = r"\b(drop|truncate|alter|grant|revoke|delete|update|insert)\b"
    if re.search(dangerous, sql_lower):
        return {"ok": False, "error": "Query blocked for safety"}

    return run_query(sql)


# ---------------------------
#   EJECUCIÓN DEL SERVER MCP
# ---------------------------
if __name__ == "__main__":
    server.run(transport="stdio")
