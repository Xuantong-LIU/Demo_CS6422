import curses


def main(stdscr):
    stdscr.clear()
    stdscr.addstr("请输入一些文字: ")
    stdscr.refresh()
    input_str = stdscr.getstr()
    stdscr.addstr(f"你输入的是: {input_str.decode('utf-8')}")
    stdscr.refresh()
    stdscr.getch()


curses.wrapper(main)
