"""
resources/ejemplo.py
─────────────────────
Ejemplo de resources para ASINFU.

Un resource es información de solo lectura que el LLM puede CONSULTAR:
documentos, configuraciones, datos de referencia, etc.

Para agregar tus propios resources:
  1. Creá un archivo nuevo en esta carpeta (ej: resources/mi_equipo.py)
  2. Definí funciones decoradas con @mcp.resource("uri://ruta")
  3. Importalas y registralas en `registrar_resources()`
"""

from fastmcp import FastMCP


def registrar_resources(mcp: FastMCP) -> None:
    """Registra todos los resources en el servidor MCP."""

    @mcp.resource("asinfu://info")
    def info_servidor() -> str:
        """Información general del servidor ASINFU."""
        return (
            "ASINFU - Servidor MCP Interno\n"
            "Versión: 0.1.0\n"
            "Descripción: Servidor base para exponer tools y recursos a los equipos.\n"
            "Documentación: ver README.md\n"
        )

    @mcp.resource("asinfu://equipos/{equipo}/config")
    def config_equipo(equipo: str) -> dict:
        """Devuelve la configuración de un equipo específico.

        Args:
            equipo: Nombre del equipo (ej: 'backend', 'datos', 'frontend').
        """
        configs = {
            "backend": {"lenguaje": "Python", "framework": "FastAPI", "tests": "pytest"},
            "datos": {"lenguaje": "Python", "herramientas": ["pandas", "dbt", "airflow"]},
            "frontend": {"lenguaje": "TypeScript", "framework": "React", "tests": "vitest"},
        }
        return configs.get(equipo, {"error": f"Equipo '{equipo}' no encontrado"})