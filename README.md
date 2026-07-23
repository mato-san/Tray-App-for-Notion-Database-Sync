# Tray-App-for-Notion-Database-Sync

A lightweight Windows system tray utility that keeps a local workflow in sync with Notion. Click the tray icon to trigger a sync on demand; the app prevents overlapping runs automatically.

## How it works

The project is split into two processes:

| File | Type | Role |
|---|---|---|
| `PyNot_App.exe` | Windows GUI (no console) | System tray icon + menu. Built with `pystray` + `Pillow`. |
| `Notion_Python.exe` | Windows console | Does the actual Notion API sync work. Built with `requests`, `pandas`. |

When you click **Sync** in the tray menu, `PyNot_App.exe` spawns `Notion_Python.exe` as a subprocess sitting next to it. It checks whether a previous sync is still running (via `Popen.poll()`) before starting a new one, so repeated clicks won't stack up duplicate processes.

```
Tray click → run_sync() → Popen(Notion_Python.exe) → Notion API
```

## Features

- One-click sync from the system tray — no terminal window needed
- Duplicate-run protection (won't start a second sync while one is active)
- Separates UI (GUI exe) from sync logic (console exe) so the worker can be run/tested independently of the tray

## Requirements

- Windows 10/11 (both exes are 64-bit PE Windows binaries; no macOS/Linux build yet)
- A Notion integration token, created at [notion.so/my-integrations](https://www.notion.so/my-integrations)
- The target database **shared with that integration** (Notion won't return data otherwise, even with a valid token)
- The **database ID**, not a page ID or the page's URL slug — these are commonly confused and produce 400/401 errors that look like auth problems but are actually ID-mismatch problems

## Installation

1. Download `PyNot_App.exe` and `Notion_Python.exe` from the [Releases](../../releases) page
2. Place them **in the same folder** — `PyNot_App.exe` locates its companion by looking next to its own path, so they can't be separated
3. Double-click `PyNot_App.exe` — an icon appears in the system tray
4. Right-click the icon → **Sync** to run manually

## Configuration

Not yet finalized in this writeup — pick one and document it here once decided:

- **Environment variables** (`NOTION_TOKEN`, `NOTION_DATABASE_ID`) — simplest, keeps secrets out of git entirely
- **A local config file** (`config.yaml` / `.env`) read at startup — easier for non-technical users, but must be `.gitignore`d

Either way, never commit the real token — ship a `config.example.yaml` or `.env.example` with placeholder values instead.

## Building from source

```bash
pip install -r requirements.txt
pyinstaller --onefile --windowed --icon=icon.ico PyNot_App.py
pyinstaller --onefile --console Notion_Python.py
```

Based on strings found in the binaries, `requirements.txt` should include at least:

```
pystray
Pillow
requests
pandas
PyYAML
colorama
pyinstaller
```

```
PyNot/
├── src/
│   ├── pynot_app.py          # tray icon + menu source (→ PyNot_App.exe)
│   ├── notion_sync.py        # sync worker source   (→ Notion_Python.exe)
│   └── icon.ico              # tray icon asset
├── build/
│   ├── PyNot_App.spec        # PyInstaller spec (reproducible builds)
│   └── Notion_Python.spec
├── dist/                     # build output — gitignored
├── config.example.yaml       # or .env.example — placeholder secrets
├── requirements.txt
├── .gitignore                # dist/, build/, __pycache__/, .env, *.spec~
├── LICENSE
├── CHANGELOG.md
├── .github/
│   └── workflows/
│       └── build.yml         # CI: build both exes on push/tag, attach to Release
└── README.md
```

Specifically worth prioritizing:

- **Source `.py` files** — the most important gap. Right now the logic only exists as compiled binaries, which means no diffing, no code review, and no way to fix a bug without starting over.
- **`.gitignore`** — keep `dist/`, `build/`, `__pycache__/`, and any `.env`/config file with real secrets out of version control.
- **`requirements.txt`** with pinned versions — so a fresh clone can rebuild identical binaries.
- **PyInstaller `.spec` files** — capture the exact build flags (`--onefile`, `--windowed`, icon path) instead of relying on remembering the command.
- **A `config.example` file** — shows the shape of the config without leaking your token.
- **GitHub Actions workflow** — auto-builds both exes and attaches them to a GitHub Release on tag push, so you're not manually re-uploading binaries each time.
- **LICENSE** — even a personal-use repo benefits from stating terms explicitly if you ever share the exes.

## Known issues / troubleshooting

- **401 Unauthorized** — token is invalid, expired, or the integration hasn't been shared into the target database's "Connections."
- **400 Bad Request on a valid-looking ID** — usually means a page ID was passed where a database ID was expected (or vice versa). Database IDs come from the database's own URL, not from a page inside it.

## License

Not yet specified — add a `LICENSE` file (MIT is a common default for personal tools like this).
