"""
ASINFU - Servidor MCP base
Punto de entrada principal del servidor.
"""

from fastmcp import FastMCP
from tools.ejemplo import registrar_tools
from tools.portales import registrar_tools as registrar_portales
from resources.ejemplo import registrar_resources
from prompts.ejemplo import registrar_prompts

# ─── Inicialización del servidor ─────────────────────────────────────────────
mcp = FastMCP(
    name="ASINFU",
    instructions=(
        "Servidor MCP interno de ASINFU. "
        "Expone herramientas, recursos y prompts para los equipos de trabajo."
    ),
)

# ─── Registro de componentes ──────────────────────────────────────────────────
registrar_tools(mcp)
registrar_portales(mcp)
registrar_resources(mcp)
registrar_prompts(mcp)

# ─── Ejecución ────────────────────────────────────────────────────────────────
# Modo HTTP:  python server.py --http   (para probar desde el inspector)
# Modo stdio: python server.py          (para Claude Desktop / Claude Code)

if __name__ == "__main__":
    import sys, os
    use_http = "--http" in sys.argv or os.environ.get("MCP_TRANSPORT") == "streamable-http"
    if use_http:
        mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
    else:
        mcp.run()