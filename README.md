# Mock MCP Server

Serveur MCP mock minimal en Python, pour tester un client MCP sans backend réel.

## Tools disponibles

| Tool | Paramètre | Retour |
|------|-----------|--------|
| `search` | `query: str` | Liste de résultats factices (string brute) |
| `read_doc` | `doc_id: str` | Contenu factice du document (string brute) |
| `whoami` | — | Debug : headers HTTP + body JSON-RPC (`method`/`params`) de la requête `tools/call` courante |

## Démarrage

```bash
make install   # crée le venv et installe les dépendances
make start     # lance le serveur
```

## Adresse

Le serveur écoute en HTTP (transport `streamable-http`) sur :

```
http://127.0.0.1:8000/mcp
```

## Config

Transport, host et port sont définis dans [server.py](server.py). En local le serveur écoute sur `127.0.0.1:8000`, mais il lit aussi les variables d'env `HOST`/`PORT` (nécessaire pour Koyeb, cf. ci-dessous) :

```python
host = os.environ.get("HOST", "0.0.0.0")
port = int(os.environ.get("PORT", 8000))
mcp.run(transport="streamable-http", host=host, port=port)
```

## Docker

```bash
make docker-build   # build l'image
make docker-run      # build + lance le conteneur sur http://localhost:8000/mcp
```

## Déploiement sur Koyeb

Le projet est prêt pour un déploiement Docker sur Koyeb :

- [Dockerfile](Dockerfile) : image `python:3.12-slim`, installe `requirements.txt`, lance `python server.py`
- Le serveur lit `PORT` (toujours injecté par Koyeb) et bind sur `0.0.0.0`
- Le health check par défaut de Koyeb est un simple **TCP** sur le port exposé → rien à configurer côté healthcheck

Étapes (via CLI, après avoir push le repo sur GitHub ou une image sur un registry) :

```bash
# Option A - depuis un repo GitHub
koyeb app init mock-mcp-server \
  --git github.com/<user>/<repo> \
  --git-branch main \
  --git-builder docker \
  --ports 8000:http \
  --routes /:8000

# Option B - depuis une image Docker déjà poussée sur un registry
docker build -t <registry>/mock-mcp-server .
docker push <registry>/mock-mcp-server
koyeb app init mock-mcp-server \
  --docker <registry>/mock-mcp-server \
  --ports 8000:http \
  --routes /:8000
```

Une fois déployé, le serveur sera accessible sur `https://<app>-<org>.koyeb.app/mcp`.

> Le projet n'est pas encore un repo git (`git init` requis pour l'option A).

## Stack

- Python 3.12
- [`mcp`](https://pypi.org/project/mcp/) SDK v2.x (`MCPServer`, ex-`FastMCP`)
