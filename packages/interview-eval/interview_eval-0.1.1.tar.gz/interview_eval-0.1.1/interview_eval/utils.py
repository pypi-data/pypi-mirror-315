import logging
import os
import re
from datetime import datetime
from pathlib import Path

import yaml
from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

# Custom theme for rich
custom_theme = Theme(
    {
        "interviewer": "green",
        "interviewee": "blue",
        "info": "cyan",
        "warning": "yellow",
        "error": "red",
        "success": "green",
    }
)

console = Console(theme=custom_theme)


def setup_logging(config: dict, verbose: bool) -> logging.Logger:
    """Setup logging configuration."""
    logger = logging.getLogger("interview")
    logger.setLevel(logging.INFO)

    # Create formatter for file logging only
    formatter = logging.Formatter("%(asctime)s - %(message)s")

    # Setup file handler if enabled
    try:
        if config["logging"]["save_to_file"]:
            output_dir = Path(config["logging"]["output_dir"])
            output_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = config["logging"]["filename_template"].format(timestamp=timestamp)
            file_handler = logging.FileHandler(output_dir / filename)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.INFO)
            logger.addHandler(file_handler)
    except KeyError:
        return None   

    return logger


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file with environment variable support."""
    load_dotenv()

    with open(config_path, "r") as file:
        content = file.read()
        # Replace ${VAR} with environment variables
        env_vars = re.findall(r"\${([^}]+)}", content)
        for var in env_vars:
            env_value = os.getenv(var)
            if env_value:
                content = content.replace(f"${{{var}}}", env_value)

    return yaml.safe_load(content)
