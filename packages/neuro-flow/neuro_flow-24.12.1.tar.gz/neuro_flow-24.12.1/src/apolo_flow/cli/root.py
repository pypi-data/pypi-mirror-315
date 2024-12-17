import dataclasses

from rich.console import Console

from apolo_flow.parser import ConfigDir


@dataclasses.dataclass(frozen=True)
class Root:
    config_dir: ConfigDir
    console: Console
    verbosity: int
    show_traceback: bool
