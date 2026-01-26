from pathlib import Path

# Default server settings
LADDRESS = "0.0.0.0"
LPORT = 53
UADDRESS = "1.1.1.1"
UPORT = 53
TIMEOUT = 5  # seconds
LOG_FORMAT = "request,reply,truncated,error"
LOG_PREFIX = None
LOGS_FILE = Path(__file__).with_name("dns_logs.log")

CONFIG_FILE = Path(__file__).with_name("settings.toml")
