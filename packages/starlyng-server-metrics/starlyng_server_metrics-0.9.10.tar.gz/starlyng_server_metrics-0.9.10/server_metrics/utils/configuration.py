"""
configuration.py
"""

from pathlib import Path
import argparse
import os
import logging
from typing import List
from dotenv import load_dotenv
from server_metrics.utils.models import Server
from server_metrics.utils.conversion import get_hostname

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run server metrics collectors.")
    parser.add_argument('--servers', type=str, help="Comma-separated list of servers in the format ip:port.")
    parser.add_argument('--key_path', type=str, help="Path to the SSH key.")
    parser.add_argument('--username', type=str, help="SSH username.")
    parser.add_argument('--combined_metrics_dir', type=str, help="Directory for combined_metrics.prom")
    return parser.parse_args()

def load_env_variables(dotenv_path=None):
    """Load environment variables from a .env file if it exists."""
    try:
        if dotenv_path is None:
            logging.info("No dotenv_path provided, skipping loading environment variables.")
            return

        if not Path(dotenv_path).exists():
            raise FileNotFoundError(f"The specified dotenv file does not exist: {dotenv_path}")

        load_dotenv(dotenv_path=dotenv_path)
    except (FileNotFoundError, PermissionError, OSError, TypeError) as error:
        logging.error("An error occurred: %s", error)

def get_configuration(args):
    """Retrieve configuration details, prioritizing command-line arguments, then environment variables."""
    servers_str = args.servers or os.getenv('SERVERS')
    key_path = args.key_path or os.getenv('KEY_PATH')
    username = args.username or os.getenv('USERNAME')
    combined_metrics_dir = args.combined_metrics_dir or os.getenv('COMBINED_METRICS_DIR', None)

    if not servers_str or not key_path or not username:
        raise ValueError("Missing configuration: ensure servers, key_path, and username are provided.")

    servers = [tuple(server.split(':')) for server in servers_str.split(',')]
    servers = [(ip, int(port)) for ip, port in servers]
    formatted_servers: List[Server] = []
    for server_ip, server_port in servers:
        server_info = {
            'hostname': get_hostname(server_ip, server_port),
            'ip': server_ip,
            'key_path': key_path,
            'port': server_port,
            'username': username,
        }
        formatted_servers.append(Server(**server_info))

    return formatted_servers, combined_metrics_dir

def load_configuration(dotenv_path=None):
    """
    Loads configuration from command-line arguments, environment variables, and .env file if it exists.

    This function first attempts to load the server configuration, SSH key path, and username
    from command-line arguments. If they are not provided, it falls back to environment variables 
    or the .env file located in the current working directory or a provided path.

    Returns:
        tuple: A tuple containing:
            - servers (list of servers): A list of servers.
            - combined_metrics_dir (str): Directory for combined_metrics.prom
    """
    args = parse_arguments()
    load_env_variables(dotenv_path=dotenv_path)
    return get_configuration(args)
