import time
import config
from rich.table import Table
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from resource_allocation import process_request, process_release
import config


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
        Layout(name="body", ratio=2)
    )

    return layout


# welcome
def update_header(layout):
    header_text = (
        "Cloud Compute Resources Management System\n"
        "A simulation of CPU resource allocation and release.\n"
        "Commands are processed from {'data.txt'}."
    )
    layout["header"].update(
        Panel(header_text, title="Welcome", border_style="bold green"))

    log_panel = Panel("", title="Logs", border_style="red")
    layout["logs"].update(log_panel)


# left head


def update_status(layout):
    status_table = Table.grid(expand=True)
    status_table.add_column(justify="left")
    status_table.add_row(f"Total CPU: {config.TOTAL_CPU}")
    status_table.add_row(f"Remaining CPU: {config.remaining_cpu}")
    status_table.add_row(f"Allocated CPU: {config.allocated_cpu}")
    status_table.add_row(f"Alarm Rate: {config.alarm_rate}")
    status_table.add_row(f"Fraction Value: {config.fraction_value}")
    status_table.add_row(f"Low-usage Rate: {config.low_usage_rate}")

    layout["status"].update(
        Panel(status_table, title="System Status", border_style="blue"))


def process_commands(cmds, layout):
    command_results = []  # 用于存储命令执行结果的列表
    log_entries = []      # 用于存储日志条目的列表

    for cmd in cmds:
        # 确保 cmd 是一个字典
        if not isinstance(cmd, dict):
            log_entry = f"Invalid command format: {cmd}"
            log_entries.append(log_entry)  # 添加到日志列表
            continue  # 跳过这个命令，继续处理下一个

        # 处理命令
        if cmd.get("operation") == "request":
            response, is_error = process_request(
                cmd.get("name"), cmd.get("number"))
        elif cmd.get("operation") == "release":
            response, is_error = process_release(
                cmd.get("name"), cmd.get("number"))
        else:
            log_entry = f"Unknown operation in command: {cmd}"
            log_entries.append(log_entry)  # 添加到日志列表
            continue  # 未知的操作，跳过

        # 如果是错误消息，则添加到日志列表，否则添加到命令结果列表
        if is_error:
            log_entries.append(response)
        else:
            command_results.append(response)

        # 更新界面的 "Command Output" 部分
        body_panel = Panel("\n".join(command_results),
                           title="Command Output", border_style="yellow")
        layout["body"].update(body_panel)

        # 更新界面的 "Logs" 部分
        log_panel = Panel("\n".join(log_entries),
                          title="Logs", border_style="red")
        layout["logs"].update(log_panel)

        update_status(layout)
        time.sleep(1)

    # 如果有日志条目，最后再更新一次日志面板
    if log_entries:
        log_panel = Panel("\n".join(log_entries),
                          title="Logs", border_style="red")
        layout["logs"].update(log_panel)
