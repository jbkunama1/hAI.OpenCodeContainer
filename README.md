# 💻 hAI.OpenCodeContainer

<div align="center">

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![DietPi](https://img.shields.io/badge/DietPi-00AEEF?style=for-the-badge)](https://dietpi.com)
[![OpenCode](https://img.shields.io/badge/OpenCode-KI--Agent-6a0dad?style=for-the-badge)](https://opencode.ai)
[![License: MIT](https://img.shields.io/badge/Lizenz-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)

[![Stack](https://img.shields.io/badge/🧱_Stack-Portainer-blue?style=flat-square)](https://www.portainer.io)
[![Update](https://img.shields.io/badge/🔄_Update-automatisch-teal?style=flat-square)](https://github.com/jbkunama1/hAI.OpenCodeContainer)
[![Self-Hosted](https://img.shields.io/badge/🏠_Self--Hosted-DietPi-green?style=flat-square)](https://dietpi.com)

**DietPi x86_64 – OpenCode + code-server + Git + GitHub CLI als Docker-Container.**

<a href="https://www.buymeacoffee.com/highfish">
<img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174">
</a>

</div>

---

Das Image wird automatisch per **GitHub Actions** gebaut und auf **GHCR**
(`ghcr.io/jbkunama1/hAI.OpenCodeContainer:latest`) gepusht. Per Portainer
wird es nur noch gepullt, nicht mehr lokal gebaut.

## Deployment per Portainer Stack

Voraussetzung: Portainer ist mit dem Docker-Endpoint des DietPi-Hosts
verbunden.

1. **Stacks → Add stack**
2. **Name**: z. B. `opencode`
3. **Build method**: **Web editor** (oder Repository) mit diesem Inhalt —
   aus [`compose.yml`](compose.yml):

```yaml
services:
  dev:
    image: ghcr.io/jbkunama1/hai.opencodcontainer:latest
    pull_policy: always
    container_name: coding-gui
    stdin_open: true
    tty: true

    environment:
      PASSWORD: "${CODE_PASSWORD}"
      TZ: "Europe/Berlin"
      OPENAI_API_KEY: "${OPENAI_API_KEY:-}"
      ANTHROPIC_API_KEY: "${ANTHROPIC_API_KEY:-}"
      OPENROUTER_API_KEY: "${OPENROUTER_API_KEY:-}"
      OPENAI_BASE_URL: "${OPENAI_BASE_URL:-}"
      MCP_SERVER_API_KEY: "${MCP_SERVER_API_KEY:-}"
      GH_TOKEN: "${GH_TOKEN:-}"

    volumes:
      - "./projects:/home/coder/project"
      - "coder-home:/home/coder"

    ports:
      - "8833:8080"

    restart: "unless-stopped"
    networks:
      - highfishNetwork
    user: "${UID_GID:-1000:1000}"

networks:
  highfishNetwork:
    external: true

volumes:
  coder-home: {}
```

4. **Environment variables** im Formular setzen (siehe Tabelle).
5. **Deploy the stack**.

> **Registry-Zugriff:** Ist das GHCR-Image **public**, genügt `latest` ohne
> Credentials. Ist es **privat**, muss in Portainer unter **Registries** eine
> GHCR-Registry mit einem GitHub **Personal Access Token** (Scope
> `read:packages`) hinterlegt werden.

## Environment

| Variable               | Pflicht | Zweck                          |
|------------------------|---------|--------------------------------|
| `MCP_SERVER_API_KEY`  | nein    | API-Key für MCP-Server beim Starten des Containers |
| `CODE_PASSWORD`        | ja      | code-server-Loginpasswort      |
| `OPENAI_API_KEY`       | nein    | OpenAI für OpenCode            |
| `ANTHROPIC_API_KEY`    | nein    | Anthropic für OpenCode         |
| `OPENROUTER_API_KEY`   | nein    | OpenRouter für OpenCode        |
| `OPENAI_BASE_URL`      | nein    | Basis-URL für OpenAI-kompatible APIs (z. B. lokaler LLM-Server oder anderer Provider) |
| `GH_TOKEN`             | nein    | GitHub-Auth für `gh` (optional)|

## Auto-Updates (neu gebaut -> Neustart)

Der Stack nutzt `pull_policy: always`, d. h. bei jedem Redeploy zieht
Portainer das neueste `ghcr.io/.../hAI.OpenCodeContainer:latest`.

**Automatisch nach jedem GHCR-Push (empfohlen):**

1. Im Stack in Portainer: **Stack settings** -> **Poll for updates** aktivieren
   und bei **Webhook** die angezeigte URL kopieren.
2. In diesem Repo unter **Settings → Webhooks** einen Webhook anlegen:
   - **Payload URL**: die kopierte Portainer-Webhook-URL
   - **Content type**: `application/json`
   - **Events**: **Package published** (GHCR) — oder, falls der Webhook
     separat eingerichtet wird, einmal pro `push`.
3. Bei jedem GHCR-Update ruft GitHub die URL auf, Portainer pullt das neue
   Image und stellt den Stack neu.

**Alternative: Watchtower** (kein GitHub-Trigger nötig)

```bash
docker run -d --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower:latest \
  --interval 3600 --cleanup
```

## Zugriff

Per SSH-Tunnel:

```bash
ssh -L 8833:127.0.0.1:8833 dietpi@DEINE-DIETPI-IP
```
Browser: `http://localhost:8833` — Passwort = `CODE_PASSWORD`.

## GitHub & OpenCode im Container

```bash
gh auth login
cd /home/coder/project && gh repo clone BENUTZERNAME/REPOSITORY
opencode                      # KI-Agent im Projektverzeichnis
opencode mcp add              # MCP-Server hinzufügen
```

## Image selbst bauen (optional)

Nur nötig, wenn du nicht das gepushte GHCR-Image nutzen willst:

```bash
git clone https://github.com/jbkunama1/hAI.OpenCodeContainer.git
cd hAI.OpenCodeContainer
docker build -f Dockerfile.gui -t ghcr.io/jbkunama1/hAI.OpenCodeContainer:latest .
```