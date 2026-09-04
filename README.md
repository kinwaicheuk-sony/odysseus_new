## My Personal Quick start

### First Time Installation
You will need the following packages to use Odysseus:
- [Docker](https://docs.docker.com/engine/install/ubuntu/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- [Ollama](#ollama)

#### Docker

Add your user to the docker group to run docker commands without sudo
```
sudo usermod -aG docker $USER
```

You will need to log out and log back in for this change to take effect. Or you can run the following command to apply the new group membership without logging out:

```
newgrp docker
```

### Odysseus

Copy `.env.example` to `.env` and edit add the following entry to allow LAN access to the Odysseus UI.

```
APP_BIND=0.0.0.0
```

You can also increase the upload size limit by adding the following entry to `.env`. The default is 10MB.
And `524288000` is 500MB. You can change it to your desired value. For more information, please refer to the [documentation](https://github.com/odysseus-dev/odysseus/issues/3364).

```
ODYSSEUS_CHAT_UPLOAD_MAX_BYTES=524288000
```

Then build the container
```
docker compose up -d --build
```

The UI can be accessed at `http://<your-ip>:7000` if you are on the same LAN.

Check the password immediately after the first build by running

```
docker compose logs odysseus
```

Otherwise you will lose the password. If that happens, delete `data/auth.json` and rebuild the container to generate a new password.


#### Useful commands

Stop the UI
```
docker compose down
```

Start the UI again (without rebuilding)
```
docker compose up -d
```



### Ollama

#### Installaion

```
curl -fsSL https://ollama.com/install.sh | sh
```

#### Auto start

Use this command to override the default service configuration. It will create a new file at `/etc/systemd/system/ollama.service.d/override.conf` with your changes.

```
sudo systemctl edit ollama
```

```bash
[Service]
Environment="OLLAMA_MODELS=/data/.ollama/models"
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_KEEP_ALIVE=30m"
```

For `OLLAMA_MODELS`, make sure the folder exists and is writable by the `ollama` user. You can create it with the following command:

```
mkdir -p /data/.ollama/
sudo chown -R ollama:ollama /data/.ollama
```


Then reload the systemd daemon and restart the service.

```
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

#### Getting Models

```
ollama pull <model-name>
```


<details>
  <summary>The following instructions are old and not recommended. You can skip them if you have already set up the auto start.</summary>
#### Manual start

```
OLLAMA_KEEP_ALIVE=30m OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

`OLLAMA_HOST=0.0.0.0:11434` is required for Odysseus in Docker to detect the Ollama server running on the host.

#### Useful commands
To check if it is running as a service, you can run the following command in your terminal:

```bash
systemctl status ollama
```

To restart the service
```bash
sudo systemctl restart ollama
```

```bash
sudo systemctl edit ollama
```

#### Trouble shooting auto start
I used to have 4 models. But upon reboot, I only have 1. It turns out I have `ollama` running as a service, but the service is running as `ollama` user, which does not have access to my home directory.

The whole thing happened when I created a systemd service for Ollama so that it can be started automatically on boot. The service file is located at `/etc/systemd/system/ollama.service` and have the following content.

```bash
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="PATH=/home/ravencheuk/.vscode-server/data/User/globalStorage/github.copilot-chat/debugCommand:/home/ravencheuk/.vscode-server/data/User/globalStorage/github.copilot-chat/copilotCli:/home/ravencheuk/.vscode-server/cli/servers/Stable-8761a5560cfd65fdd19ce7e2bd18dab5c0a4d84e/server/bin/remote-cli:/home/ravencheuk/miniforge3/bin:/home/ravencheuk/miniforge3/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"

[Install]
WantedBy=default.target
```

As you can see the `User` and `Group` are set to `ollama`.

A quick fix is to change the `User` and `Group` to your username.

Somehow Claude Sonnet 5 recommended me this

```bash
sudo systemctl edit ollama
```

```bash
[Service]
User=ravencheuk
Group=ravencheuk
Environment="OLLAMA_MODELS=/home/ravencheuk/.ollama/models"
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_KEEP_ALIVE=30m"
```

It works, but the solution is very ugly.
It's way better to directly edit the service file at `/etc/systemd/system/ollama.service` and change the `User` and `Group` to your username.

<p align="center">
  <img src="assets/branding/odysseus-wordmark.png" alt="Odysseus" width="238">
</p>

<p align="center">
  A self-hosted AI workspace for chat, agents, research, documents, email, notes, calendar, and local model workflows.
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="website/setup.md">Setup Guide</a> ·
  <a href="CONTRIBUTING.md">Contributing</a> ·
  <a href="ROADMAP.md">Roadmap</a>
</p>

<p align="center">
  <a href="https://repology.org/project/odysseus-ai/versions"><img src="https://repology.org/badge/vertical-allrepos/odysseus-ai.svg" alt="Packaging status"></a>
</p>

<p align="center">
  <img src="assets/branding/odysseus-browser.jpg" alt="Odysseus interface">
</p>

---

## Quick Start

> `dev` is the default branch and gets the newest changes first. Use [`main`](https://github.com/odysseus-dev/odysseus/tree/main) if you want the more curated branch.

```bash
git clone https://github.com/odysseus-dev/odysseus.git
cd odysseus
cp .env.example .env
docker compose up -d --build
```

Open `http://localhost:7000` when the containers are healthy. The first admin password is printed in `docker compose logs odysseus`.

Native installs, GPU notes, Windows/macOS instructions, HTTPS, and configuration live in the [setup guide](website/setup.md).

## Features

- **Chat + Agents** — local/API models, tools, MCP, files, shell, skills, and memory.
- **Cookbook** — hardware-aware model recommendations, downloads, and serving.
- **Deep Research** — multi-step web research with source reading and report generation.
- **Compare** — blind side-by-side model testing and synthesis.
- **Documents** — writing-first editor with AI edits, suggestions, Markdown, HTML, CSV, and syntax highlighting.
- **Email** — IMAP/SMTP inbox with triage, tags, summaries, reminders, and reply drafts.
- **Notes, Tasks + Calendar** — reminders, todos, scheduled agent tasks, and CalDAV sync.
- **Extras** — gallery/image editor, themes, uploads, web search, presets, sessions, and 2FA.

## Demo

A full hover-to-play tour lives on the [Odysseus landing page](https://odysseus-dev.github.io/odysseus/). Its source lives under [`website/`](website/).

## Contributing

Help is welcome. The best entry points are fresh-install testing, provider setup bugs, mobile/editor polish, docs, and small focused refactors. See [CONTRIBUTING.md](CONTRIBUTING.md) and [ROADMAP.md](ROADMAP.md).

## Security

Odysseus is a self-hosted workspace with powerful local tools. Keep auth enabled, keep private data out of Git, and do not expose raw model/service ports publicly.

- Keep `AUTH_ENABLED=true` for any network-accessible deployment.
- Keep `LOCALHOST_BYPASS=false` outside local development.

Deployment details are in the [setup guide](website/setup.md#security-notes).

## Star History

<a href="https://star-history.dera.page/#odysseus-dev/odysseus&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://star-history.dera.page/svg?repos=odysseus-dev/odysseus&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://star-history.dera.page/svg?repos=odysseus-dev/odysseus&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://star-history.dera.page/svg?repos=odysseus-dev/odysseus&type=date&legend=top-left" />
 </picture>
</a>

## License

AGPL-3.0-or-later -- see [LICENSE](LICENSE) and [ACKNOWLEDGMENTS.md](ACKNOWLEDGMENTS.md).
