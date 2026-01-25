def get_section_without_defaults(parser: ConfigParser, section: str) -> dict:
    if parser.has_section(section):
        data = {
            item[0]: item[1]
            for item in parser.items(section)
            if item not in parser.items(parser.default_section)
            and not item[0].startswith("$")
        }

        return data

    return {}


def parse_logs_file(logs_file: str, default_value: str):
    if isinstance(logs_file, str):
        if logs_file.strip().lower() in ["true", "1", "activate", "enable", "on"]:
            return default_value

        elif logs_file.strip().lower() in [
            "false",
            "0",
            "deactivate",
            "disable",
            "off",
        ]:
            return False

        else:
            return logs_file

    else:
        return default_value if logs_file else logs_file
