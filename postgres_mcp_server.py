import os
import psycopg2
import psycopg2.extras
from urllib.parse import urlparse
from fastmcp import FastMCP

server = FastMCP("postgres-server")

# ---------------------------
#   FUNCIÓN REAL DE QUERY
# ---------------------------

def run_query(sql: str):
    url = os.getenv("SUPABASE_DB_URL")
    if not url:
        raise ValueError("Missing SUPABASE_DB_URL in environment")

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
                    # Query sin resultados (ej: INSERT/UPDATE)
                    return {"ok": True, "rows": []}

    except Exception as e:
        return {"ok": False, "error": str(e)}


# ---------------------------
#   TOOLS EXTERNOS MCP
# ---------------------------

@server.tool()
async def query(sql: str):
    """Consulta SQL general desde MCP."""
    return run_query(sql)

@server.tool()
async def get_logs(limit: int = 10):
    """Consulta los últimos logs."""
    sql = f"SELECT * FROM logs ORDER BY created_at DESC LIMIT {limit}"
    return run_query(sql)


if __name__ == "__main__":
    server.run(transport="stdio")
