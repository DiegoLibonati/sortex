# Sortex

## Educational Purpose

This project was created primarily for **educational and learning purposes**.  
While it is well-structured and could technically be used in production, it is **not intended for commercialization**.  
The main goal is to explore and demonstrate best practices, patterns, and technologies in software development.

## Description

**Sortex** is a desktop application built with Python and Tkinter that automatically organizes the files inside any directory by grouping them into extension-named subfolders. Instead of manually sorting a cluttered folder full of mixed file types, you point Sortex at a directory and it takes care of everything in one click.

When you trigger the organize operation, Sortex scans the target directory, detects every file extension present, creates a dedicated subfolder for each one following the naming convention `<EXTENSION>_ORGANIZER` (e.g. `PDF_ORGANIZER`, `MP3_ORGANIZER`, `PNG_ORGANIZER`), and moves each file into its corresponding folder. The result is a clean, structured directory where every file type lives in its own place.

You are not forced to organize everything at once. The extensions panel lets you select exactly which file types to include in the operation — check only the ones you care about and Sortex will ignore the rest. Supported extensions out of the box include `mp4`, `pdf`, `exe`, `png`, `jpg`, `jpeg`, `txt`, `json`, `mp3`, `m3u8`, `zip`, and `gif`.

For more granular control, Sortex also offers a size filter. You can define a minimum and maximum file size in megabytes, and only files that fall within that range will be moved. This is useful when you want to organize large media files without touching lightweight config or text files, or vice versa.

If the result is not what you expected, or you simply want to undo the operation, the **Revert Organize** button restores the original layout: every file is moved back to the root of the directory and all the `_ORGANIZER` folders are deleted, leaving the directory exactly as it was before.

The application is intentionally simple and self-contained. There is no database, no cloud sync, and no background service — it runs locally, operates only on the directory you choose, and does nothing unless you explicitly trigger an action.

## Technologies used

1. Python >= 3.11
2. Tkinter

## Libraries used

The project splits its dependencies into separate requirements files so you only install what you need for each workflow (runtime, development, testing, build).

#### Requirements.txt

```
python-dotenv==1.0.1
```

#### Requirements.dev.txt
```
pre-commit==4.3.0
pip-audit==2.7.3
ruff==0.11.12
```

#### Requirements.test.txt

```
pytest==8.4.2
pytest-env==1.1.5
pytest-cov==4.1.0
pytest-timeout==2.3.1
pytest-xdist==3.5.0
```

#### Requirements.build.txt

```
pyinstaller==6.16.0
```

## Getting Started

Follow these steps to run Sortex locally from source.

1. Clone the repository
2. Go to the repository folder and execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute in Linux/Mac: `source venv/bin/activate`
5. Copy the development environment file: `cp .env.example.dev .env` (on Windows: `copy .env.example.dev .env`)
6. Execute: `pip install -r requirements.txt`
7. Execute: `pip install -r requirements.dev.txt`
8. Execute: `pip install -r requirements.test.txt`
9. Use `python app.py` or `python -m src` to execute the program

### Pre-Commit for Development

1. Once you're inside the virtual environment, let's install the hooks specified in the pre-commit. Execute: `pre-commit install`
2. Now every time you try to commit, the pre-commit lint will run. If you want to do it manually, you can run the command: `pre-commit run --all-files`

## Env Keys

The `.env` file you copied in the previous step controls how the application boots. These are the variables it understands:

1. `ENVIRONMENT`: Defines the application environment. Accepts `development`, `production`, or `testing`.

```
ENVIRONMENT=development
```

## Testing

With the environment set up, you can run the test suite to verify everything works as expected.

1. Go to the repository folder
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute in Linux/Mac: `source venv/bin/activate`
5. Execute: `pip install -r requirements.txt`
6. Execute: `pip install -r requirements.test.txt`
7. Execute: `pytest --log-cli-level=INFO`

## Security Audit

You can check your dependencies for known vulnerabilities using **pip-audit**.

1. Go to the repository folder
2. Activate your virtual environment
3. Execute: `pip install -r requirements.dev.txt`
4. Execute: `pip-audit -r requirements.txt`

## Build

Once the code is tested and the dependencies are clean, you can ship Sortex as a standalone executable (`.exe` on Windows, or binary on Linux/Mac) using **PyInstaller**.

> **Security notice:** `app.spec` bundles the `.env` file into the executable. Never put real
> production secrets (API keys, passwords, tokens) inside the repo-level `.env` before building.
> Instead, create a dedicated `.env.prod` file with production values, copy it to `.env` just
> before running PyInstaller, and delete it afterwards. The development `.env` (`ENVIRONMENT=development`)
> is safe to use for local builds only.

### Windows

1. Go to the repository folder
2. Activate your virtual environment: `venv\Scripts\activate`
3. Install build dependencies: `pip install -r requirements.build.txt`
4. Create the executable: `pyinstaller app.spec`

Alternatively, you can run the helper script: `build.bat`

### Linux / Mac

1. Go to the repository folder
2. Activate your virtual environment: `source venv/bin/activate`
3. Install build dependencies: `pip install -r requirements.build.txt`
4. Create the executable: `pyinstaller app.spec`

Alternatively, you can run the helper script: `./build.sh`

## Known Issues

None at the moment.

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/sortex`](https://www.diegolibonati.com.ar/#/project/sortex)
