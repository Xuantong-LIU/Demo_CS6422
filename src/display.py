import time
import config
from rich.table import Table
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.align import Align
from resource_allocation import process_request, process_release
import config
import asciichartpy as acp


console = Console()


def create_layout():
    layout = Layout()

    layout.split_row(
        Layout(name="left_panel", size=30),
        Layout(name="main_panel", ratio=1)
    )

    layout["left_panel"].split_column(
        Layout(name="status"),
        Layout(name="logs")
    )

    layout["main_panel"].split_row(
        Layout(name="header", ratio=1),
        Layout(name="bodyAndGraph", ratio=2)
    )

    layout["bodyAndGraph"].split_column(
        Layout(name="body", ratio=2),
        Layout(name="graph", ratio=1)
    )

    return layout


# welcome
def update_header(layout):
    header_text = (
        "Cloud Compute Resources Management System\n"
        "A simulation of CPU resource allocation and release.\n"
        f"Commands are processed from {config.path}."
    )
    layout["header"].update(
        Panel(header_text, title="Welcome", border_style="bold green"))

    log_panel = Panel("", title="Logs", border_style="red")
    layout["logs"].update(log_panel)

    graph_panel = Panel("", title="Graph", border_style="red")
    layout["logs"].update(graph_panel)


# left head
def draw_graph_panel(sent_data, graph_name, color):
    return Panel(
        Align.left(
            acp.plot(sent_data, {'min': 0, 'height': 10}), vertical="bottom"),
        title=f"[bold][yellow]{graph_name}[/bold][/yellow]",
        border_style=color,
        style="green",
    )


def update_status(layout, recv_buffer):
    status_table = Table.grid(expand=True)
    status_table.add_column(justify="left")
    status_table.add_row(f"Total CPU: {config.TOTAL_CPU}")
    status_table.add_row(f"Remaining CPU: {config.remaining_cpu:.2f}")
    status_table.add_row(f"Allocated CPU: {config.allocated_cpu:.2f}")
    status_table.add_row(f"Alarm Rate: {config.alarm_rate}")
    status_table.add_row(f"Fraction Value: {config.fraction_value}")
    status_table.add_row(f"Low-usage Rate: {config.low_usage_rate}")
    status_table.add_row(f"Overbooking: {config.overbooking}")
    recv_buffer.append(config.allocated_cpu)

    layout["status"].update(
        Panel(status_table, title="System Status", border_style="blue"))

    layout["graph"].update(
        draw_graph_panel(recv_buffer, "Allocated CPU", "red")
    )


def process_commands(cmds, layout):
    command_results = []  # use to store the cmd output
    log_entries = []      # use to store logs
    recv_buffer = []
    max_lines = 6

    for cmd in cmds:
        # make sure cmd is a dictionary type
        if not isinstance(cmd, dict):
            log_entry = f"Invalid command format: {cmd}"
            log_entries.append(log_entry)  # add it to the log
            continue

        # process the cmd
        if cmd.get("operation") == "request":
            response, is_error = process_request(
                cmd.get("name"), cmd.get("number"))
        elif cmd.get("operation") == "release":
            response, is_error = process_release(
                cmd.get("name"), cmd.get("number"))
        else:
            log_entry = f"Unknown operation in command: {cmd}"
            log_entries.append(log_entry)  # add it to the log
            continue

        if is_error:
            log_entries.append(response)

            if len(log_entries) > max_lines:
                log_entries = log_entries[-max_lines:]
        else:
            command_results.append(response)

            if len(command_results) > max_lines:
                command_results = command_results[-max_lines:]

        # refresh Command Output
        body_panel = Panel("\n".join(command_results),
                           title="Command Output", border_style="yellow")
        layout["body"].update(body_panel)

        # refresh Logs
        log_panel = Panel("\n".join(log_entries),
                          title="Logs", border_style="red")
        layout["logs"].update(log_panel)

        update_status(layout, recv_buffer)
        time.sleep(1)

    if log_entries:
        log_panel = Panel("\n".join(log_entries),
                          title="Logs", border_style="red")
        layout["logs"].update(log_panel)
