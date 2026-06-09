"""
tools/portales.py
──────────────────
Tools para consultar el catálogo de portales gub.uy por grupo.
Fuente: data/portales_gub_uy.csv
"""

# pandas es una librería para trabajar con tablas de datos (como Excel pero en código)
import pandas as pd
# Path nos ayuda a construir rutas de archivos de forma segura en cualquier sistema operativo
from pathlib import Path
# FastMCP es el servidor que expone las herramientas al agente de IA
from fastmcp import FastMCP

# __file__ es la ruta de este archivo. Subimos dos carpetas (.parent.parent) para llegar
# a la raíz del proyecto y de ahí bajar a data/portales_gub_uy.csv
DATA_PATH = Path(__file__).parent.parent / "data" / "portales_gub_uy.csv"


def cargar_datos() -> pd.DataFrame:
    # Lee el CSV y lo convierte en una tabla (DataFrame).
    # dtype=str → trata todas las columnas como texto para evitar errores de tipo.
    # fillna("") → reemplaza las celdas vacías con texto vacío en lugar de NaN.
    # encoding="latin-1" → usa la codificación correcta del archivo
    return pd.read_csv(DATA_PATH, dtype=str, encoding="latin-1", sep=";").fillna("")


def registrar_tools(mcp: FastMCP) -> None:
    # Esta función recibe el servidor MCP y le agrega las 4 herramientas.
    # Se llama una sola vez al arrancar el servidor.

    @mcp.tool  # Le dice al servidor: "registrá esta función como herramienta disponible"
    def buscar_portal(termino: str) -> list[dict]:
        """Busca portales por cualquier término: nombre, sigla, URL o grupo.

        Args:
            termino: Texto a buscar (ej: 'interior', 'MI', 'Grupo 3').
        """
        df = cargar_datos()  # Carga la tabla del CSV

        t = termino.lower()  # Convierte el término a minúsculas para buscar sin importar mayúsculas

        # mask es una columna de True/False: True donde alguna columna contiene el término buscado.
        # El | significa "o" — alcanza con que coincida en UNA de las columnas.
        mask = (
            df["url"].str.lower().str.contains(t) |
            df["nombre_largo"].str.lower().str.contains(t) |
            df["sigla"].str.lower().str.contains(t) |
            df["grupo_portales"].str.lower().str.contains(t)
        )

        # df[mask] devuelve solo las filas donde mask es True.
        # .to_dict(orient="records") convierte la tabla en una lista de diccionarios,
        # que es el formato que el agente de IA puede leer fácilmente.
        return df[mask].to_dict(orient="records")

    @mcp.tool
    def portales_por_grupo(grupo: str) -> list[dict]:
        """Lista todos los portales de un grupo específico.

        Args:
            grupo: Nombre del grupo (ej: 'Grupo 3', 'Grupo Catálogos', 'Presidencia').
        """
        df = cargar_datos()

        # A diferencia de buscar_portal, acá usamos == (igual exacto) en vez de contains.
        # Solo devuelve filas donde el grupo coincide exactamente con lo buscado.
        mask = df["grupo_portales"].str.lower() == grupo.lower()

        return df[mask].to_dict(orient="records")

    @mcp.tool
    def grupo_de_portal(url_o_nombre: str) -> dict:
        """Devuelve el grupo al que pertenece un portal buscando por URL o nombre.

        Args:
            url_o_nombre: URL parcial o nombre del organismo (ej: 'ministerio-interior', 'DGI').
        """
        df = cargar_datos()
        t = url_o_nombre.lower()

        # Busca en URL, nombre largo y sigla (no en grupo, porque justamente queremos encontrar el grupo)
        mask = (
            df["url"].str.lower().str.contains(t) |
            df["nombre_largo"].str.lower().str.contains(t) |
            df["sigla"].str.lower().str.contains(t)
        )

        resultado = df[mask]

        # Si no encontró ninguna fila, devuelve un mensaje de error en vez de una lista vacía
        if resultado.empty:
            return {"error": f"No se encontró ningún portal para '{url_o_nombre}'"}

        # Solo devuelve las columnas relevantes (no todas), para una respuesta más limpia
        return resultado[["url", "nombre_largo", "sigla", "grupo_portales", "tipo_ambiente", "ambiente_portal"]].to_dict(orient="records")

    @mcp.tool
    def resumen_por_grupo() -> list[dict]:
        """Devuelve un resumen con la cantidad de portales por grupo."""
        df = cargar_datos()

        resumen = (
            df.groupby("grupo_portales")       # Agrupa todas las filas por el valor de la columna "grupo_portales"
            .size()                            # Cuenta cuántas filas hay en cada grupo
            .reset_index(name="cantidad")      # Convierte el resultado en una tabla con columna "cantidad"
            .sort_values("grupo_portales")     # Ordena alfabéticamente por nombre de grupo
        )

        return resumen.to_dict(orient="records")
