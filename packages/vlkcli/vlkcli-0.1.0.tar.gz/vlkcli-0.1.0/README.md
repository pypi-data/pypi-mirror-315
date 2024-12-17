# Valkyrie CLI

## Overview

Valkyrie CLI is a command-line interface designed to interact with the Valkyrie API, providing functionality for user authentication, tool management, API key creation, wallet operations, and more. It supports executing individual commands and processing sequences of commands from a YAML configuration file.

---

## Features

- **Authentication**: Login with username and password to obtain a session token.
- **Tools Management**: View all tools, fetch tool details, and execute specific tool endpoints.
- **API Key Management**: Create, list, and delete API keys associated with tools.
- **Wallet Operations**: Retrieve wallet details and transaction history.
- **Batch Command Execution**: Execute a sequence of commands defined in a YAML file.

---

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:AzumoHQ/azumo-valkyrie-cli.git
   cd azumo-valkyrie-cli
   ```

2. Install the CLI using `setup.py`:
   ```bash
   python setup.py install
   ```

3. After installation, the `vlk` command will be available in your terminal.

---

## Usage

Run the CLI using the `vlk` command:
```bash
vlk <command> [options]
```

### Commands

#### **Authentication**
- Login:
  ```bash
  vlk login <username>
  ```

#### **Tools**
- List all tools:
  ```bash
  vlk tools
  ```
- Get tool details:
  ```bash
  vlk tools:info --tool <tool_id>
  ```
- Execute a tool endpoint:
  ```bash
  vlk tools:run --tool <tool_id> --endpoint <endpoint> --api-key <api_key> --payload <json_payload>
  ```

#### **API Keys**
- List API keys:
  ```bash
  vlk api-keys
  ```
- Create an API key:
  ```bash
  vlk api-keys:create --key-name <name> --tool <tool_id>
  ```
- Delete an API key:
  ```bash
  vlk api-keys:delete --api-key <api_key_id>
  ```

#### **Wallet**
- View wallet details:
  ```bash
  vlk wallet
  ```
- View wallet transactions:
  ```bash
  vlk wallet:transactions --type <CREDIT|DEBIT> --order <asc|desc> --page <page_num> --page_size <num>
  ```

#### **Execute Configuration**
- Run a sequence of commands from a YAML file:
  ```bash
  vlk execute-config --file <config.yaml>
  ```

---

## Example YAML Configuration

```yaml
- command: login
  args:
    username: omaribannez@gmail.com

- command: tools
  args: {}

- command: tools:info
  args:
    tool: the-dog-api

- command: wallet
  args: {}

- command: wallet:transactions
  args:
    page_size: 2
    page: 2
    order: desc
```

Run the configuration:
```bash
vlk execute-config --file config.yaml
```

---

## Authentication Token

After successful login, a token is saved in `~/.valkyrie_token` for subsequent authenticated requests. Ensure to keep this file secure.