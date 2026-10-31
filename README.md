# hAI.OpenCodeContainer

Docker Setup für [OpenCode](https://opencode.ai) - AI-Powered Code Editor mit Auto-Build via GitHub Actions, Unterstützung für eigene OpenAI-kompatible LLMs und integriertem MCP Server mit JWT Authentication.

## 🏗️ Architektur

```
git push origin master
        ↓
GitHub Actions: Build & Push → ghcr.io/jbkunama1/hai.opencodecontainer
        ↓
Portainer: Stack Update (re-pullt latest)
        ↓
Container läuft auf Port 8076 ✓
```

## 🚀 Quick Start mit Portainer

### 1. Docker Netzwerk erstellen (falls nicht vorhanden)

```bash
docker network create highfishNetwork
```

### 2. GHCR Registry in Portainer einrichten

Das Image wird von GitHub Container Registry gepullt:

**Option A: Image public machen (empfohlen)**
- GitHub → Packages → `hai.opencodecontainer` → Package Settings → Change visibility → Public

**Option B: Private mit Auth**
- Portainer → Registries → Add registry
- Registry: `ghcr.io`
- Username: `jbkunama1`
- Password: GitHub PAT mit `read:packages` Scope

### 3. Stack deployen

1. **Stacks** → **Add stack**
2. **Name:** `opencode`
3. **Build method:** Git Repository
4. **Repository URL:** `https://github.com/jbkunama1/hAI.OpenCodeContainer.git`
5. **Stack file:** `docker-compose.portainer.yml`
6. **Environment Variables** eintragen (siehe unten)
7. **Deploy the stack** ✓

### 4. Environment Variables (Pflicht)

| Variable | Beispiel | Beschreibung |
|----------|----------|--------------|
| `OPENCODE_SERVER_PASSWORD` | `DeinPasswort123!` | Login-Passwort |
| `OPENAI_API_KEY` | `sk-xxxxxxxx` | API Key (für OpenAI oder kompatible) |
| `LOCAL_ENDPOINT` | `http://localhost:8000/v1` | OpenAI-kompatibler API Endpoint |
| `CUSTOM_OPENAI_ENDPOINT` | `http://localhost:8000/v1` | Zusätzlicher OpenAI-kompatibler Endpoint |
| `CUSTOM_MCP_ENDPOINT` | `http://localhost:9000` | MCP Server Endpoint |

### 5. Environment Variables (Optional)

| Variable | Default | Beschreibung |
|----------|---------|--------------|
| `OPENCODE_SERVER_USERNAME` | `opencode` | Login-Username |
| `OPENCODE_PORT` | `8076` | Externer Port |
| `TZ` | `Europe/Berlin` | Zeitzone |
| `OPENCODE_DATA_DIR` | `~/opencode/data` | Daten-Verzeichnis |
| `OPENCODE_PROJECTS_DIR` | `~/opencode/projects` | Projekt-Verzeichnis |

## 🔐 Login

Nach dem Deploy unter `http://<server-ip>:8076` erreichbar:

| Feld | Wert |
|------|------|
| **Username** | `opencode` (oder dein `OPENCODE_SERVER_USERNAME`) |
| **Password** | Dein `OPENCODE_SERVER_PASSWORD` |

## 🔄 Auto-Build Workflow

Bei jedem Push auf `master`/`main`:

1. GitHub Actions baut das Docker Image aus dem `Dockerfile`
2. Push zu `ghcr.io/jbkunama1/hai.opencodecontainer:latest`
3. Tags: `latest`, `master`, `<commit-sha>`

**Automatisches Deploy zu Portainer:**
- Der `portainer-deploy.yml` Workflow automatisch bei Merge auf master/main
- Updated das Stack mit dem neuen Image und deployt automatisch

## 🚀 GitHub Actions

### Build & Push (manuell oder automatisch)
- Trigger: Push auf master/main, tags v*, manuell
- Unterstützt beide Dockerfiles: `Dockerfile` und `Dockerfile.gui`
- Pusht zu GHCR mit mehreren Tags

### Portainer Deploy (automatisch bei Merge)
- Trigger: Push auf master/main, manuell
- Updated Portainer Stack mit neuestem Image
- Führt Health Check durch
- Benötigt GitHub Secrets:
  - `PORTAINER_URL`: Portainer API URL
  - `PORTAINER_TOKEN`: Portainer API Token
  - `OPENCODE_SERVER_PASSWORD`: Server Passwort
  - `OPENAI_API_KEY`: API Key
  - `LOCAL_ENDPOINT`: OpenAI Endpoint
  - `CUSTOM_OPENAI_ENDPOINT`: Custom OpenAI Endpoint
  - `CUSTOM_MCP_ENDPOINT`: Custom MCP Endpoint

## 🩺 Troubleshooting

| Problem | Ursache | Lösung |
|---------|---------|--------|
| `xdg-open` Crash | Container hat keinen Browser | Bereits gefixt (Fake-Script im Image) |
| `unhealthy` + 401 | Healthcheck mit Auth | Bereits gefixt (akzeptiert 401) |
| Nicht erreichbar | Server bindet auf 127.0.0.1 | Bereits gefixt (`--hostname 0.0.0.0`) |
| GHCR pull denied | Image ist private | Public machen oder Registry-Auth in Portainer |
| Port 8076 belegt | Andere Service nutzt Port | Port ändern oder Service stoppen |

## 🔧 Features

- ✅ OpenAI-kompatible API Integration (Multi-Endpoint)
- ✅ GitHub MCP Support (jbkunama1/*)
- ✅ Eigener OpenAI-kompatibler LLM Support
- ✅ **Integrierter MCP Server** mit JWT Authentication
- ✅ Auto-Build via GitHub Actions
- ✅ Auto-Deploy bei Merge
- ✅ GHCR Image Registry
- ✅ Portainer-ready (Environment Variables)
- ✅ Basic Auth (Username/Password)
- ✅ highfishNetwork Integration
- ✅ Persistent Data Storage
- ✅ Health Check & Monitoring (Ports 8076, 9000, 9001)
- ✅ Docker Compose & Portainer Support
- ✅ Fehlerbehandlung für JWT Token Validation

## 📝 Notes

- **Secrets** niemals ins Repo committen!
- Env Vars nur über Portainer UI setzen
- Bei Updates bleiben Secrets erhalten
- Der Port wurde von 4096 auf 8076 geändert
- Nutze `docker-compose.portainer.yml` für Portainer Deployment

## 🔌 MCP Server Integration

Der MCP Server ist jetzt **integriert** in den OpenCode-Container und läuft zusammen mit der OpenCode Web UI.

### MCP Server Features

- 🔐 **JWT Token Authentication** - Sicherheitssteuerung
- 📋 **MCP 1.0 Protocol** - Vollständig kompatibel
- 🛡️ **Health Check** - Port 9001
- 🔑 **Token Management** - Auto-Erstellung und Ablauf (30 Tage Gültigkeit)
- 🔧 **Fehlerbehandlung** - Robuste JWT Token Validation

### Deployment

Der MCP Server ist **integriert** in den OpenCode Container. Deployment erfolgt über Portainer mit dem `docker-compose.portainer.yml` Stack:

```bash
# In Portainer
1. Stack hinzufügen
2. Repository URL: https://github.com/jbkunama1/hAI.OpenCodeContainer.git
3. Stack file: docker-compose.portainer.yml
4. Environment Variables eintragen
5. Deploy Stack
```

### MCP API Nutzung

**Token erstellen:**
```bash
curl -X POST http://localhost:9000/mcp \
  -H "Authorization: Bearer CREATE_TOKEN" | jq -r '.token'
```

**Chat via MCP:**
```bash
curl -X POST http://localhost:9000/mcp \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "chat",
    "params": {
      "message": "Hallo OpenCode!"
    }
  }'
```

**MCP Tools auflisten:**
```bash
curl -X POST http://localhost:9000/mcp \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools.list"
  }'
```

### MCP Secret Key

Optional für zusätzliche Sicherheit:
```bash
OPENCODE_MCP_SECRET_KEY=dein-sicheres-secret-key-xyz
```

Wenn nicht gesetzt, wird automatisch ein zufälliger Secret Key generiert.

## 🦈 Network

Das Setup nutzt das externe Docker-Netzwerk `highfishNetwork`.

## 🔌 Custom Endpoints

### Eigene OpenAI-kompatible LLMs
Setze die folgenden Environment Variables:
```bash
CUSTOM_OPENAI_ENDPOINT=http://localhost:8000/v1
OPENAI_API_KEY=dein-api-key
```

### Eigener MCP Server
```bash
CUSTOM_MCP_ENDPOINT=http://localhost:9000
```

### Portainer Secrets Setup
1. Gehe zu Portainer → Stacks → `opencode` → Environment
2. Klicke auf "Add environment variable"
3. Füge die Secrets hinzu (Werte aus GitHub Secrets)
4. Deploy Stack neu

---

**Repository:** https://github.com/jbkunama1/hAI.OpenCodeContainer
**Image:** https://github.com/jbkunama1/hAI.OpenCodeContainer/pkgs/container/hai.opencodecontainer
