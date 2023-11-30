from rich.console import Console
from rich.live import Live
from cmd_parser import read_cmds_to_objects
from display import create_layout, update_header, update_status, process_commands


if __name__ == "__main__":
    console = Console()
    layout = create_layout()
    update_header(layout)
    update_status(layout, [])

    with Live(layout, console=console, refresh_per_second=4):
        file_path = "data/scen1-2.txt"
        cmds = read_cmds_to_objects(file_path)
        process_commands(cmds, layout)

    console.print("[bold green]All commands processed![/bold green]")
