# capital-manager

> Personal capital manager — track your income and expenses through a REST API or a command-line interface.

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [REST API](#rest-api)
  - [CLI](#cli)
- [Project Structure](#project-structure)
- [Development](#development)

---

## Overview

**capital-manager** is a self-hosted personal finance tool that lets you record and query income and expense entries. It exposes a fully documented REST API powered by FastAPI and an interactive command-line interface built with Typer, so you can interact with your data however you prefer.

## Tech Stack

| Layer           | Library                                      |
| --------------- | -------------------------------------------- |
| Web framework   | [FastAPI](https://fastapi.tiangolo.com/)     |
| ASGI server     | [Uvicorn](https://www.uvicorn.org/)          |
| CLI             | [Typer](https://typer.tiangolo.com/)         |
| Data validation | [Pydantic v2](https://docs.pydantic.dev/)    |
| ORM / database  | [SQLAlchemy 2](https://docs.sqlalchemy.org/) |
| Build backend   | [Hatchling](https://hatch.pypa.io/)          |
| Package manager | [uv](https://docs.astral.sh/uv/)             |
| Testing         | [pytest](https://docs.pytest.org/)           |

## Requirements

- Python **≥ 3.13**
- [uv](https://docs.astral.sh/uv/) (recommended) — or any PEP 517-compatible installer

## Installation

Clone the repository and install all dependencies using `uv`:

```bash
git clone https://github.com/raidelo/capital-manager.git
cd capital-manager
uv sync
```

This will create a virtual environment and install the project along with all its dependencies in one step.

## Usage

All commands are available through the `capman` entry point.

### Database initialization

Before using the app for the first time, initialize the database tables:

```bash
capman init-db
```

### REST API

Start the API server:

```bash
capman api [--host 127.0.0.1] [--port 8000] [--reload]
```

Then open the interactive Swagger UI docs in your browser:

```
http://127.0.0.1:8000/docs
```

#### Endpoints

| Method | Path                | Description                                                                                      |
| ------ | ------------------- | ------------------------------------------------------------------------------------------------ |
| `GET`  | `/ping`             | Health check                                                                                     |
| `GET`  | `/accounts`         | List all accounts                                                                                |
| `POST` | `/accounts`         | Create a new account                                                                             |
| `GET`  | `/accounts/balance` | Get balance of one or all accounts (`account_id` and/or `account_name` as optional query params) |
| `GET`  | `/transactions`     | List all transactions                                                                            |
| `POST` | `/transactions`     | Create a new transaction                                                                         |

### CLI

#### `capman account`

| Subcommand | Arguments      | Description                                              |
| ---------- | -------------- | -------------------------------------------------------- |
| `list`     | —              | List all accounts                                        |
| `create`   | `NAME` `ASSET` | Create a new account                                     |
| `balance`  | `[NAME]`       | Show balance of a specific account, or all if none given |

```bash
capman account list
capman account create "My Wallet" USD
capman account balance            # lists all accounts with their balances
capman account balance "My Wallet"
```

#### `capman transaction`

| Subcommand | Arguments                 | Options                  | Description           |
| ---------- | ------------------------- | ------------------------ | --------------------- |
| `list`     | —                         | —                        | List all transactions |
| `add`      | `ACCOUNT` `AMOUNT` `TYPE` | `-d, --description TEXT` | Add a transaction     |

`TYPE` must be either `income` or `expense`.

```bash
capman transaction list
capman transaction add "My Wallet" 150.00 income
capman transaction add "My Wallet" 45.50 expense --description "Groceries"
```

Run `capman --help` or `capman <command> --help` for full details on any command.

## Project Structure

```
capital-manager/
├── src/
│   └── capital_manager/       # Main package
│       ├── api/               # FastAPI application and routers
│       └── cli/               # Typer CLI entrypoint
├── tests/                     # pytest test suite
├── pyproject.toml             # Project metadata and dependencies
├── uv.lock                    # Locked dependency versions
└── README.md
```

## Development

Install dev dependencies and run the test suite:

```bash
uv sync --dev
uv run pytest
```

Any changes to the source files under `src/` are reflected immediately without reinstalling.
