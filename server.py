import os

from mcp.server.mcpserver import Context, MCPServer

mcp = MCPServer("Mock MCP Server")


@mcp.tool()
def search(query: str) -> str:
    """Recherche mockée : retourne une liste de résultats factices pour la requête donnée."""
    return (
        f"Résultats pour '{query}':\n"
        f"1. doc-001 - Introduction à MCP\n"
        f"2. doc-002 - Guide de configuration\n"
        f"3. doc-003 - FAQ et dépannage"
    )


@mcp.tool()
def read_doc(doc_id: str) -> str:
    """Lecture mockée : retourne le contenu factice du document demandé."""
    return (
        f"Contenu du document '{doc_id}':\n"
        f"Ceci est un contenu de test généré pour le document {doc_id}. "
        f"Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    )


@mcp.tool()
def whoami(ctx: Context) -> str:
    """Debug : retourne les headers et le body JSON-RPC de la requête tools/call courante."""
    headers = ctx.headers or {}
    rc = ctx.request_context
    headers_block = "\n".join(f"  {k}: {v}" for k, v in headers.items()) or "  (aucun)"
    return (
        f"Protocol version: {ctx.protocol_version}\n"
        f"Request ID: {ctx.request_id}\n"
        f"Méthode JSON-RPC: {rc.method}\n"
        f"Headers:\n{headers_block}\n"
        f"Body (params):\n{rc.params}"
    )


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="streamable-http", host=host, port=port)
