"""
tools/ejemplo.py
────────────────
Ejemplo de tools para ASINFU.

Un tool es una función que el LLM puede INVOCAR para hacer algo:
calcular, llamar una API, transformar datos, etc.

Para agregar tus propios tools:
  1. Creá un archivo nuevo en esta carpeta (ej: tools/mi_equipo.py)
  2. Definí funciones con type hints y docstrings claros
  3. Importalas en este archivo y registralas en `registrar_tools()`
"""

from fastmcp import FastMCP


def registrar_tools(mcp: FastMCP) -> None:
    """Registra todos los tools en el servidor MCP."""

    @mcp.tool
    def saludar(nombre: str) -> str:
        """Saluda a una persona por su nombre.

        Args:
            nombre: El nombre de la persona a saludar.
        """
        return f"¡Hola, {nombre}! Bienvenido/a a ASINFU 👋"

    @mcp.tool
    def sumar(a: float, b: float) -> float:
        """Suma dos números y devuelve el resultado.

        Args:
            a: Primer número.
            b: Segundo número.
        """
        return a + b

    @mcp.tool
    async def listar_tools_disponibles() -> list[str]:
        """Lista todos los tools registrados en el servidor ASINFU."""
        tools = await mcp.list_tools()
        return [t.name for t in tools]