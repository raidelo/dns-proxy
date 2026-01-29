from pathlib import Path

MAIN_PATH = Path.home().joinpath(".config/dns-proxy")

# Default server settings
LADDRESS = "0.0.0.0"
LPORT = 53
UADDRESS = "1.1.1.1"
UPORT = 53
TIMEOUT = 5  # seconds
LOG_FORMAT = "request,reply,truncated,error"
LOG_PREFIX = False
LOGS_FILE = MAIN_PATH.joinpath("dns.log")

CONFIG_FILE = MAIN_PATH.joinpath("settings.toml")
