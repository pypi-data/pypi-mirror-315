#!/usr/bin/env python3
import argparse
import getpass
import json
import os

import requests
import yaml
from yaml.parser import ParserError
from yaml.scanner import ScannerError

API_URL = os.getenv("VALKYRIE_API_URL", "https://valkyrie-back-dev.azumotechnology.com/api/v1")


def execute_config(args):
    """
    Execute a sequence of commands specified in a YAML configuration file.
    """
    # Load and validate the YAML file
    try:
        with open(args.file, "r") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Configuration file '{args.file}' not found.")
        return
    except (ParserError, ScannerError) as e:
        print(f"Error: Invalid YAML format. {e}")
        return

    # Validate required keys
    if not isinstance(config, list):
        print("Error: Configuration file must be a list of command objects.")
        return

    for idx, command in enumerate(config, start=1):
        try:
            command_name = command.get("command")
            command_args = command.get("args", {})

            if not command_name:
                print(f"Error: Missing 'command' in step {idx}.")
                continue

            print(f"Executing command {idx}: {command_name} with args {command_args}")

            # Map the command to the corresponding CLI function
            command_func = COMMAND_MAP.get(command_name)
            if not command_func:
                print(f"Error: Unknown command '{command_name}' in step {idx}.")
                continue

            # Convert arguments to argparse-like namespace
            command_args_namespace = argparse.Namespace(**command_args)
            command_func(command_args_namespace)

        except Exception as e:
            print(f"Error executing step {idx}: {e}")
            continue


def authenticate(args):
    """
    Authenticate the user.
    """
    # Prompt for the password securely
    password = getpass.getpass(prompt="Password: ")
    payload = {"username": args.username, "password": password}
    response = requests.post(f"{API_URL}/auth/login", json=payload)

    if response.status_code == 200:
        print("Authentication successful")
        token = response.json().get("token")
        with open(f"{os.path.expanduser('~')}/.valkyrie_token", "w") as token_file:
            token_file.write(token)
    else:
        print("Authentication failed")
        print(response.text)


def tools(args):
    """
    Get all tools.
    """
    response = requests.get(f"{API_URL}/tools/", headers=_prepare_auth_header())
    _show_response(response)


def tool(args):
    """
    Get details of a specific tool by ID or identifier.
    """
    response = requests.get(
        f"{API_URL}/tools/{args.tool}/", headers=_prepare_auth_header()
    )
    _show_response(response)


def execute_endpoint(args):
    """
    Execute a tool endpoint with arguments for tool, endpoint, API key, and payload.
    """
    # Prepare the base payload with the API key
    payload = {"api_key": args.api_key}

    try:
        # Merge the provided payload if any
        if args.payload:
            user_payload = json.loads(args.payload)
            payload.update(user_payload)
    except json.JSONDecodeError:
        print("Invalid JSON format in payload.")
        return

    # Construct the API URL
    url = f"{API_URL}/tools/{args.tool}/execute/{args.endpoint}"

    # Send the POST request
    response = requests.post(url, json=payload, headers=_prepare_auth_header())

    # Display the response
    _show_response(response)


def create_api_key(args):
    """
    Create a new API key.
    """
    payload = {"key_name": args.key_name, "tool_id": args.tool}
    response = requests.post(
        f"{API_URL}/api-keys", json=payload, headers=_prepare_auth_header()
    )
    _show_response(response)


def get_api_keys(args):
    """
    Get all API keys.
    """
    response = requests.get(f"{API_URL}/api-keys/", headers=_prepare_auth_header())
    _show_response(response)


def delete_api_key(args):
    """
    Delete an API key.
    """
    response = requests.delete(
        f"{API_URL}/api-keys/{args.api_key}", headers=_prepare_auth_header()
    )
    _show_response(response)


def wallet(args):
    """
    Get the wallet details for the authenticated user.
    """
    response = requests.get(f"{API_URL}/users/wallet/", headers=_prepare_auth_header())
    _show_response(response)


def wallet_transactions(args):
    """
    Get all wallet transactions for the authenticated user with filters, ordering, and pagination.
    """
    # Build query parameters
    params = {}

    if hasattr(args, "type"):
        params["type"] = args.type
    if hasattr(args, "order"):
        params["order"] = args.order
    if hasattr(args, "page"):
        params["page"] = args.page
    if hasattr(args, "page_size"):
        params["page_size"] = args.page_size

    # Make the GET request with query parameters
    response = requests.get(
        f"{API_URL}/users/wallet/transactions",
        headers=_prepare_auth_header(),
        params=params,
    )
    _show_response(response)


def _prepare_auth_header():
    headers = {"Content-Type": "application/json"}
    try:
        with open(f"{os.path.expanduser('~')}/.valkyrie_token", "r") as token_file:
            token = token_file.read()
            headers["Authorization"] = f"Bearer {token}"
        return headers
    except FileNotFoundError:
        print("Authentication token not found. Please authenticate first.")
        return headers


# Map command names to their corresponding functions
COMMAND_MAP = {
    "login": authenticate,
    "tools": tools,
    "tools:info": tool,
    "tools:run": execute_endpoint,
    "api-keys": get_api_keys,
    "api-keys:create": create_api_key,
    "api-keys:delete": delete_api_key,
    "wallet": wallet,
    "wallet:transactions": wallet_transactions,
}


def _show_response(response):
    try:
        print(json.dumps(response.json(), indent=4))
    except json.JSONDecodeError:
        print(response.text)


def main():
    parser = argparse.ArgumentParser(
        description="Valkyrie CLI for interacting with the API."
    )

    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Authenticate
    auth_parser = subparsers.add_parser("login", help="Authenticate the user.")
    auth_parser.add_argument("username", help="Your username.")
    auth_parser.set_defaults(func=authenticate)

    # Get tools
    tools_parser = subparsers.add_parser("tools", help="Get all tools.")
    tools_parser.set_defaults(func=tools)

    # Get a specific tool
    tool_parser = subparsers.add_parser(
        "tools:info", help="Get details of a specific tool."
    )
    tool_parser.add_argument(
        "--tool", required=True, help="ID or identifier of the tool."
    )
    tool_parser.set_defaults(func=tool)

    # Execute an endpoint
    execute_parser = subparsers.add_parser("tools:run", help="Execute a tool endpoint.")
    execute_parser.add_argument(
        "--tool", required=True, help="ID or identifier of the tool."
    )
    execute_parser.add_argument(
        "--endpoint", required=True, help="Endpoint to execute."
    )
    execute_parser.add_argument(
        "--api-key", required=True, help="API key to include in the payload."
    )
    execute_parser.add_argument(
        "--payload", default="{}", help="Additional payload in JSON format."
    )
    execute_parser.set_defaults(func=execute_endpoint)

    # Get API keys
    get_api_keys_parser = subparsers.add_parser("api-keys", help="Get all API keys.")
    get_api_keys_parser.set_defaults(func=get_api_keys)

    # Create an API key
    create_api_key_parser = subparsers.add_parser(
        "api-keys:create", help="Create a new API key."
    )
    create_api_key_parser.add_argument(
        "--key-name", required=True, help="Name of the API key."
    )
    create_api_key_parser.add_argument(
        "--tool", required=True, help="ID or identifier of the tool."
    )
    create_api_key_parser.set_defaults(func=create_api_key)

    # Delete an API key
    delete_api_key_parser = subparsers.add_parser(
        "api-keys:delete", help="Delete an API key."
    )
    delete_api_key_parser.add_argument(
        "--api-key", required=True, help="ID of the API key to delete."
    )
    delete_api_key_parser.set_defaults(func=delete_api_key)

    # Get wallet details
    get_wallet_parser = subparsers.add_parser(
        "wallet", help="Get wallet details for the authenticated user."
    )
    get_wallet_parser.set_defaults(func=wallet)

    # Get wallet transactions
    get_wallet_transactions_parser = subparsers.add_parser(
        "wallet:transactions",
        help="Get wallet transactions for the authenticated user.",
    )
    get_wallet_transactions_parser.add_argument(
        "--type", choices=["CREDIT", "DEBIT"], help="Filter transactions by type."
    )
    get_wallet_transactions_parser.add_argument(
        "--order", choices=["asc", "desc"], help="Order transactions (asc or desc)."
    )
    get_wallet_transactions_parser.add_argument(
        "--page", type=int, help="Page number for pagination."
    )
    get_wallet_transactions_parser.add_argument(
        "--page_size", type=int, help="Number of results per page."
    )
    get_wallet_transactions_parser.set_defaults(func=wallet_transactions)

    # Execute YAML file
    execute_config_parser = subparsers.add_parser(
        "execute-config",
        help="Execute a series of commands from a YAML configuration file.",
    )
    execute_config_parser.add_argument(
        "--file", required=True, help="Path to the YAML configuration file."
    )
    execute_config_parser.set_defaults(func=execute_config)

    args = parser.parse_args()

    # Execute the corresponding function
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
