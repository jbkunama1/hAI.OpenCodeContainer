# hAI.OpenCodeContainer

Docker Compose Setup für [OpenCode](https://opencode.ai) - AI-Powered Code Editor.

## 🚀 Quick Start mit Portainer

### 1. Docker Netzwerk erstellen

```bash
docker network create highfishNetwork
```

### 2. In Portainer deployen

1. **Stacks** → **Add stack**
2. **Name:** `opencode`
3. **Build method:** Git Repository
4. **Repository URL:** `https://github.com/jbkunama1/hAI.OpenCodeContainer.git`
5. **Stack file:** `docker-compose.yml`
6. **Environment Variables** eintragen (siehe unten)
7. **Deploy the stack** ✓

### 3. Environment Variables

| Variable | Beispiel | Beschreibung |
|----------|----------|--------------|
| `OPENCODE_PORT` | `4096` | Externer Port |
| `TZ` | `Europe/Berlin` | Zeitzone |
| `OPENCODE_SERVER_PASSWORD` | `DeinPasswort123!` | Login-Passwort |
| `OPENAI_API_KEY` | `sk-xxxxxxxx` | OpenAI-kompatibler API Key |
| `LOCAL_ENDPOINT` | `https://api.example.com/v1` | API Endpoint URL |
| `OPENCODE_DATA_DIR` | `/home/user/opencode/data` | Daten-Verzeichnis |
| `OPENCODE_PROJECTS_DIR` | `/home/user/opencode/projects` | Projekt-Verzeichnis |

## 🏗️ Architektur

```
┌─────────────────────────────────────────┐
│         opencode Container              │
│  (ghcr.io/opencode-ai/opencode:latest)  │
├─────────────────────────────────────────┤
│  Port: 4096 (Web UI)                    │
│  Network: highfishNetwork               │
│  Volumes:                               │
│    - ~/opencode/data (Config)           │
│    - ~/opencode/projects (Workspace)    │
└─────────────────────────────────────────┘
```

## 🔧 Features

- ✅ OpenAI-kompatible API Integration
- ✅ GitHub MCP Support (jbkunama1/*)
- ✅ Portainer-ready (Environment Variables)
- ✅ highfishNetwork Integration
- ✅ Persistent Data Storage

## 📝 Notes

- **Secrets** niemals ins Repo committen!
- Nur über Portainer UI als Environment Variables setzen
- Bei Updates bleiben Secrets erhalten

## 🦈 Network

Das Setup nutzt das externe Docker-Netzwerk `highfishNetwork`.

---

**Repository:** https://github.com/jbkunama1/hAI.OpenCodeContainer
