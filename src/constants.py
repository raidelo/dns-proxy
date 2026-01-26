from pathlib import Path

LOCAL_ADDRESS = "0.0.0.0"
LOCAL_PORT = 53
UPSTREAM_ADDRESS = "1.1.1.1"
UPSTREAM_PORT = 53
DEFAULT_TIMEOUT = 5  # seconds

DEFAULT_LOGGING_FMT = "request,reply,truncated,error"
DEFAULT_LOGGING_PREFIX = None
DEFAULT_SETTINGS_FILE = Path(__file__).with_name("settings.toml")
DEFAULT_LOGS_FILE = Path(__file__).with_name("dns_logs.log")
