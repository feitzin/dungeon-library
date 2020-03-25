import maps
import curses

test = maps.Map("firstfloorhome.map", [1,2])
rows, columns = test.get_size()

screen = curses.initscr()

curses.curs_set(0)
curses.noecho()

map_window = curses.newwin(rows+1, columns+1, 0, 0)

c = None

running = 1
while(running):
    try:
        test.render(map_window)
        map_window.refresh()
        screen.refresh()
        c = chr(screen.getch())
        if c in ['w','d','s','a']:
            test.move_player(c)
        if c == 'e':
            test.interact()
        if c == 'q':
            running = 0
    except Exception as e:
        curses.endwin()
        print("Critical failure")
        print(e)
        running = 0
        pass
    
curses.endwin()
