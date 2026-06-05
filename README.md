# ASINFU — Servidor MCP

Servidor MCP (Model Context Protocol) interno para exponer **tools**, **resources** y **prompts** a los equipos de trabajo a través de Claude.

---

## ¿Qué es esto?

Un servidor MCP permite que Claude acceda a herramientas personalizadas tuyas. Podés pensar en él como una API, pero diseñada específicamente para LLMs.

Tiene tres tipos de componentes:

| Tipo | ¿Qué es? | Analogía |
|------|----------|----------|
| **Tool** | Función que Claude puede invocar | Endpoint POST |
| **Resource** | Datos de solo lectura que Claude puede consultar | Endpoint GET |
| **Prompt** | Plantilla reutilizable que el usuario puede invocar | Slash command |

---

## Estructura del proyecto

```
asinfu/
├── server.py                        # Punto de entrada del servidor
├── pyproject.toml                   # Dependencias (para uv)
├── claude_desktop_config.example.json  # Config de referencia para Claude Desktop
├── tools/
│   └── ejemplo.py                   # Tools de ejemplo — agregá los tuyos acá
├── resources/
│   └── ejemplo.py                   # Resources de ejemplo
└── prompts/
    └── ejemplo.py                   # Prompts de ejemplo
```

---

## Instalación rápida

### 1. Instalá `uv` (gestor de paquetes recomendado)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Cloná o copiá este proyecto

```bash
cd /ruta/donde/quieras/guardar
# (copiá la carpeta asinfu acá)
cd asinfu
```

### 3. Instalá las dependencias

```bash
uv sync
```

### 4. Probá el servidor con el MCP Inspector

```bash
uv run fastmcp dev server.py
```

Esto abre el inspector en `http://localhost:6274` donde podés probar todos los tools y resources sin necesidad de Claude Desktop.

---

## Conectarlo con Claude Desktop

1. Abrí la configuración de Claude Desktop:
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2. Agregá la sección `mcpServers` (usá `claude_desktop_config.example.json` como referencia):

```json
{
  "mcpServers": {
    "asinfu": {
      "command": "uv",
      "args": [
        "--directory",
        "/RUTA/ABSOLUTA/A/asinfu",
        "run",
        "server.py"
      ]
    }
  }
}
```

> **Importante:** Reemplazá `/RUTA/ABSOLUTA/A/asinfu` con la ruta real en tu máquina.
> Podés obtenerla con `pwd` (macOS/Linux) o `cd` (Windows) desde la carpeta del proyecto.

3. Reiniciá Claude Desktop. Deberías ver un ícono de herramientas (🔧) en el chat.

---

## Cómo agregar nuevos tools

1. Creá un archivo en `tools/mi_nuevo_tool.py`:

```python
from fastmcp import FastMCP

def registrar_tools(mcp: FastMCP) -> None:

    @mcp.tool
    def mi_herramienta(parametro: str) -> str:
        """Descripción clara del tool (el LLM lee esto para saber cuándo usarlo).

        Args:
            parametro: Descripción del parámetro.

        Returns:
            Descripción de lo que devuelve.
        """
        return f"Resultado: {parametro}"
```

2. Importalo y registralo en `server.py`:

```python
from tools.mi_nuevo_tool import registrar_tools as registrar_mi_tool
# ...
registrar_mi_tool(mcp)
```

---

## Próximos pasos

- [ ] Agregar tus tools específicos del equipo
- [ ] Conectar con APIs internas (autenticación, bases de datos, etc.)
- [ ] Evaluar si escalar a un servidor HTTP remoto compartido con el equipo
- [ ] Agregar tests en `tests/`

---

## Recursos útiles

- [Documentación de FastMCP](https://gofastmcp.com)
- [Especificación MCP](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
