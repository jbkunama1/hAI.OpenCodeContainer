# hAI.OpenCodeContainer

Docker Setup für [OpenCode](https://opencode.ai) - AI-Powered Code Editor mit Auto-Build via GitHub Actions.

## 🏗️ Architektur

```
git push origin master
        ↓
GitHub Actions: Build & Push → ghcr.io/jbkunama1/hai.opencodecontainer
        ↓
Portainer: Stack Update (re-pullt latest)
        ↓
Container läuft ✓
```

## 🚀 Quick Start mit Portainer

### 1. Docker Netzwerk erstellen

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
5. **Stack file:** `docker-compose.yml`
6. **Environment Variables** eintragen (siehe unten)
7. **Deploy the stack** ✓

### 4. Environment Variables (Pflicht)

| Variable | Beispiel | Beschreibung |
|----------|----------|--------------|
| `OPENCODE_SERVER_PASSWORD` | `DeinPasswort123!` | Login-Passwort |
| `OPENAI_API_KEY` | `sk-xxxxxxxx` | OpenAI-kompatibler API Key |
| `LOCAL_ENDPOINT` | `https://api.example.com/v1` | API Endpoint URL |

### 5. Environment Variables (Optional)

| Variable | Default | Beschreibung |
|----------|---------|--------------|
| `OPENCODE_SERVER_USERNAME` | `opencode` | Login-Username |
| `OPENCODE_PORT` | `4096` | Externer Port |
| `TZ` | `Europe/Berlin` | Zeitzone |
| `OPENCODE_DATA_DIR` | `~/opencode/data` | Daten-Verzeichnis |
| `OPENCODE_PROJECTS_DIR` | `~/opencode/projects` | Projekt-Verzeichnis |

## 🔐 Login

Nach dem Deploy unter `http://<server-ip>:4096` erreichbar:

| Feld | Wert |
|------|------|
| **Username** | `opencode` (oder dein `OPENCODE_SERVER_USERNAME`) |
| **Password** | Dein `OPENCODE_SERVER_PASSWORD` |

## 🔄 Auto-Build Workflow

Bei jedem Push auf `master`/`main`:

1. GitHub Actions baut das Docker Image aus dem `Dockerfile`
2. Push zu `ghcr.io/jbkunama1/hai.opencodecontainer:latest`
3. Tags: `latest`, `master`, `<commit-sha>`

**Update in Portainer:** Stack → Editor → "Re-pull image and redeploy"

## 🩺 Troubleshooting

| Problem | Ursache | Lösung |
|---------|---------|--------|
| `xdg-open` Crash | Container hat keinen Browser | Bereits gefixt (Fake-Script im Image) |
| `unhealthy` + 401 | Healthcheck mit Auth | Bereits gefixt (akzeptiert 401) |
| Nicht erreichbar | Server bindet auf 127.0.0.1 | Bereits gefixt (`--hostname 0.0.0.0`) |
| GHCR pull denied | Image ist private | Public machen oder Registry-Auth in Portainer |

## 🔧 Features

- ✅ OpenAI-kompatible API Integration
- ✅ GitHub MCP Support (jbkunama1/*)
- ✅ Auto-Build via GitHub Actions
- ✅ GHCR Image Registry
- ✅ Portainer-ready (Environment Variables)
- ✅ Basic Auth (Username/Password)
- ✅ highfishNetwork Integration
- ✅ Persistent Data Storage

## 📝 Notes

- **Secrets** niemals ins Repo committen!
- Env Vars nur über Portainer UI setzen
- Bei Updates bleiben Secrets erhalten

## 🦈 Network

Das Setup nutzt das externe Docker-Netzwerk `highfishNetwork`.

---

**Repository:** https://github.com/jbkunama1/hAI.OpenCodeContainer
**Image:** https://github.com/jbkunama1/hAI.OpenCodeContainer/pkgs/container/hai.opencodecontainer
