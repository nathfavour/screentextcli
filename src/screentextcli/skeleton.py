"""
screentextz - A CLI tool that continuously scans directories for new image files,
extracts text using Tesseract CLI, and copies the text to the system clipboard.

To install:
    In setup.cfg specify:
         console_scripts =
             screentextz = screentextcli.skeleton:run
    Then run “pip install .” or “pip install -e .”
"""

import argparse
import json
import logging
import sys
import os
import time
import subprocess

from screentextcli import __version__
from screentextcli.cli import commands  # new import for subcommand handlers

__author__ = "nathfavour"
__copyright__ = "nathfavour"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

# ---- Config management ----
def load_config():
    """Load settings from ~/screentextz.json; create file with defaults if missing."""
    config_path = os.path.join(os.path.expanduser("~"), "screentextz.json")
    default = {
        "dirs": [os.path.expanduser("~/Pictures/Screenshots")],
        "scan_interval": 5
    }
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            json.dump(default, f, indent=4)
        return default
    else:
        with open(config_path, "r") as f:
            config = json.load(f)
        for key, value in default.items():
            config.setdefault(key, value)
        return config

# ---- Functions for directory scanning and clipboard management ----
def copy_to_clipboard(text):
    """Copy text to the system clipboard using available CLI tools."""
    if sys.platform == "win32":
        subprocess.run("clip", input=text, text=True, shell=True)
    elif sys.platform == "darwin":
        subprocess.run("pbcopy", input=text, text=True)
    else:
        subprocess.run(["xclip", "-selection", "clipboard"], input=text, text=True)

def watch_dirs(dirs, scan_interval=5):
    """Continuously scan given directories for new image files and process them."""
    processed = set()
    image_exts = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")
    
    # Pre-scan: mark all existing images as processed
    for d in dirs:
        for root, _, files in os.walk(d):
            for file in files:
                if file.lower().endswith(image_exts):
                    processed.add(os.path.join(root, file))
    
    _logger.info("Monitoring directories: " + ", ".join(dirs))
    try:
        while True:
            for d in dirs:
                for root, _, files in os.walk(d):
                    for file in files:
                        if file.lower().endswith(image_exts):
                            full_path = os.path.join(root, file)
                            if full_path in processed:
                                continue
                            _logger.info(f"Processing new image: {full_path}")
                            try:
                                result = subprocess.run(
                                    ["tesseract", full_path, "stdout"],
                                    capture_output=True, text=True
                                )
                                text = result.stdout.strip()
                                if text:
                                    copy_to_clipboard(text)
                                    _logger.info("Extracted text copied to clipboard.")
                                else:
                                    _logger.warning("No text extracted from image.")
                            except Exception as e:
                                _logger.error(f"Error processing {full_path}: {e}")
                            processed.add(full_path)
            time.sleep(scan_interval)
    except KeyboardInterrupt:
        _logger.info("Stopping directory monitoring.")

# ---- CLI with subcommands ----
def parse_args(args):
    """Parse command line parameters using subparsers."""
    parser = argparse.ArgumentParser(
        description="screentextz - continuously scan directories for new images, extract text using Tesseract, and copy it to the clipboard."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"screentextcli {__version__}",
    )
    parser.add_argument(
        "-v", "--verbose", dest="loglevel",
        help="set loglevel to INFO", action="store_const", const=logging.INFO,
    )
    parser.add_argument(
        "-vv", "--very-verbose", dest="loglevel",
        help="set loglevel to DEBUG", action="store_const", const=logging.DEBUG,
    )
    subparsers = parser.add_subparsers(dest="command", help="subcommands")  # removed required=True
    start_parser = subparsers.add_parser("start", help="start monitoring directories")
    start_parser.add_argument(
        "--dirs",
        nargs="+",
        help="Directories to monitor (overrides configuration)"
    )
    subparsers.add_parser("config", help="display current configuration")
    parsed = parser.parse_args(args)
    if parsed.command is None:
        parsed.command = "start"  # default to start if no subcommand is provided
    return parsed

def setup_logging(loglevel):
    """Setup basic logging."""
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout, format=logformat,
                        datefmt="%Y-%m-%d %H:%M:%S")

def main(cli_args):
    """Main entry point for screentextz CLI."""
    args = parse_args(cli_args)
    loglevel = args.loglevel or logging.WARNING
    setup_logging(loglevel)
    config = load_config()
    # Dispatch to the appropriate command handler
    if args.command == "start":
        from screentextcli.cli import commands  # local import if needed
        commands.start(args, config)
    elif args.command == "config":
        from screentextcli.cli import commands  # local import if needed
        commands.config(args, config)

def run():
    """Execute main passing command line arguments."""
    main(sys.argv[1:])

if __name__ == "__main__":
    run()
