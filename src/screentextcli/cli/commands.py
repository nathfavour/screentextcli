import os
from screentextcli.skeleton import watch_dirs  # reuse scanning function

def start(args, config):
    """
    Start monitoring directories.
    Uses --dirs from CLI if provided; otherwise falls back to config file.
    """
    dirs = args.dirs if args.dirs is not None else config["dirs"]
    scan_interval = config.get("scan_interval", 5)
    watch_dirs(dirs, scan_interval)

def config(args, config):
    """
    Display the current configuration.
    """
    # Pretty-print configuration
    import json
    print(json.dumps(config, indent=4))
