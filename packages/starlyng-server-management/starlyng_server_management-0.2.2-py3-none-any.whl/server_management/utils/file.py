"""file.py"""
import logging
import os
import time
from typing import List, Tuple
from ssh_connection import Server

def get_last_reboot(server_mgmt_dir: str, minutes_since_last_reboot: float) -> bool:
    """
    Check if a reboot has occurred within the specified time frame.

    Args:
        server_mgmt_dir (str): Directory for server management files.
        minutes_since_last_reboot (float): Time threshold in minutes.

    Returns:
        bool: True if a reboot occurred within the specified time, False otherwise.
    """
    file_path = os.path.join(server_mgmt_dir, 'last_reboot')
    logging.info("Checking last reboot file: %s", file_path)

    if not os.path.exists(file_path):
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_timestamp = float(f.read().strip())
    except (ValueError, IOError) as e:
        logging.error("The file %s does not contain a valid timestamp: %s", file_path, e)
        return False

    time_difference = int((time.time() - file_timestamp) / 60)
    logging.info("Time since last reboot: %s minutes", time_difference)
    return time_difference <= minutes_since_last_reboot

def set_last_reboot(server_mgmt_dir: str) -> None:
    """
    Record the current time as the last reboot time.

    Args:
        server_mgmt_dir (str): Directory for server management files.
    """
    file_path = os.path.join(server_mgmt_dir, 'last_reboot')

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(time.time()))
    except IOError as e:
        logging.error("Error writing to last_reboot file: %s", e)

def create_bcm_sel_list_logs(logs_for_bcm_servers: List[Tuple[Server, str]], server_mgmt_dir: str) -> bool:
    """
    Create log files for BCM SEL list data.

    Args:
        logs_for_bcm_servers (List[Tuple[Server, str]]): List of servers and their logs.
        server_mgmt_dir (str): Directory for server management files.

    Returns:
        bool: True if logs are successfully created, False otherwise.
    """
    crash_reports_dir = os.path.join(server_mgmt_dir, 'crashes')

    try:
        os.makedirs(crash_reports_dir, exist_ok=True)
        current_time = int(time.time())

        for server, logs in logs_for_bcm_servers:
            file_name = f'{current_time}-{server.hostname}_bcm_sel_list.log'
            file_path = os.path.join(crash_reports_dir, file_name)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(logs)

        return True

    except OSError as e:
        logging.error("Error creating crash reports: %s", e)
        return False
