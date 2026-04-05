# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-04-04

### Added

- `capman account balance NAME` — show the current balance of an account from the CLI
- `GET /accounts/balance` API endpoint — returns the balance and asset of an account, looked up by `account_id` and/or `account_name` query params

### Changed

- CLI `account` and `transaction` commands extracted into separate modules (`cli/account/` and `cli/transaction/`)
- API account and transaction endpoints extracted into separate router modules
- Service layer split into subpackages (`services/accounts/`, `services/transactions/`, `services/financial/`)
- Improved account-related error messages for clarity

## [0.1.0] - 2026-04-04

### Added

- REST API with FastAPI exposing `GET /accounts`, `POST /accounts`, `GET /transactions`, and `POST /transactions` endpoints
- CLI (`capman`) with `account list`, `account create`, `transaction list`, and `transaction add` subcommands
- Database initialization via `capman init-db`
- Interactive API docs available at `http://127.0.0.1:8000/docs`
- Health check endpoint `GET /ping`
