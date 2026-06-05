"""
prompts/ejemplo.py
───────────────────
Ejemplo de prompts para ASINFU.

Un prompt es una plantilla reutilizable que guía cómo el LLM
interactúa con el usuario o con los datos.

Para agregar tus propios prompts:
  1. Creá un archivo nuevo en esta carpeta (ej: prompts/mi_equipo.py)
  2. Definí funciones decoradas con @mcp.prompt
  3. Importalas y registralas en `registrar_prompts()`
"""

from fastmcp import FastMCP


def registrar_prompts(mcp: FastMCP) -> None:
    """Registra todos los prompts en el servidor MCP."""

    @mcp.prompt
    def revision_codigo(lenguaje: str, codigo: str) -> str:
        """Plantilla para revisar un bloque de código.

        Args:
            lenguaje: Lenguaje de programación (ej: 'Python', 'TypeScript').
            codigo: El código a revisar.
        """
        return (
            f"Revisá el siguiente código {lenguaje} y proporcioná feedback sobre:\n"
            f"1. Posibles bugs o errores\n"
            f"2. Mejoras de legibilidad y estilo\n"
            f"3. Optimizaciones de rendimiento\n"
            f"4. Buenas prácticas del lenguaje\n\n"
            f"```{lenguaje.lower()}\n{codigo}\n```"
        )

    @mcp.prompt
    def generar_ticket(titulo: str, descripcion: str, equipo: str = "general") -> str:
        """Plantilla para generar la descripción de un ticket de trabajo.

        Args:
            titulo: Título breve del ticket.
            descripcion: Descripción detallada del problema o tarea.
            equipo: Equipo responsable (default: 'general').
        """
        return (
            f"Generá un ticket de trabajo bien estructurado con la siguiente información:\n\n"
            f"**Título:** {titulo}\n"
            f"**Equipo:** {equipo}\n"
            f"**Descripción inicial:** {descripcion}\n\n"
            f"El ticket debe incluir: contexto, criterios de aceptación, "
            f"posibles dependencias y estimación de esfuerzo."
        )