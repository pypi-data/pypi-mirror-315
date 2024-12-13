"""
gpu_collector.py
"""
import json
import logging
from server_metrics.utils.prom.gpu import create_gpu_prom_file
from server_metrics.utils.models import Server
from server_metrics.utils.ssh import run_ssh_subprocess
from server_metrics.utils.xml_parser import xml_to_json

def run_nvidia_smi(server: Server) -> str:
    """
    Gets GPU data from servers using nvidia-smi

    Args:
        server (Server):

    Returns:
        str:
    """

    # Command to connect via SSH and run nvidia-smi
    ssh_command = "nvidia-smi -q -x"
    result = run_ssh_subprocess(server, ssh_command)

    if result.stdout:
        try:
            xml_output = xml_to_json(result.stdout)
            json_output = json.dumps(xml_output, indent=4)
            json_data = json.loads(json_output)
            prom_file_contents = create_gpu_prom_file(server.hostname, json_data)
        except json.JSONDecodeError as e:
            logging.error("Failed to decode JSON: %s", e)
            prom_file_contents = ""
    else:
        prom_file_contents = ""

    return prom_file_contents
