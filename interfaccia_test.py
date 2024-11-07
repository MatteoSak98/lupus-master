#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses

title = '''
 _                              _         _____     _           _       
| |                            (_)       |_   _|   | |         | |      
| |    _   _ _ __  _   _ ___    _ _ __     | | __ _| |__  _   _| | __ _ 
| |   | | | | '_ \| | | / __|  | | '_ \    | |/ _` | '_ \| | | | |/ _` |
| |___| |_| | |_) | |_| \__ \  | | | | |   | | (_| | |_) | |_| | | (_| |
\_____/\__,_| .__/ \__,_|___/  |_|_| |_|   \_/\__,_|_.__/ \__,_|_|\__,_|
            | |                                                        
            |_|                                                        
'''

regole_text = '''
Benvenuto alle Regole del Gioco!
Il gioco consiste in...

Premi ENTER per tornare al menu principale.
'''

def draw_menu(stdscr, current_row):
    stdscr.clear()
    stdscr.addstr(0, 0, title)
    stdscr.addstr(10, 2, "Nuova Partita")
    stdscr.addstr(11, 2, "Regole")
    stdscr.addstr(12, 2, "Ruoli")
    stdscr.addstr(13, 2, "Exit")

    for row_num, row_title in enumerate(["Nuova Partita", "Regole", "Ruoli", "Exit"]):
        x = 2
        y = row_num + 10
        if current_row == row_num:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row_title)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row_title)

    stdscr.refresh()
    
def nuova_partita():
    print('Inizio nuova partita...')

def regole_page(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, regole_text)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == curses.KEY_ENTER or key in [10, 13]:  # Enter
            break
        elif key == curses.KEY_ESC:  # Esc
            return  # Torna al menu principale

def regole(stdscr):
    regole_page(stdscr)

def ruoli():
    # Logica per gestire i ruoli dei giocatori
    print("Gestione dei ruoli dei giocatori!")

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Imposta colori per evidenziare l'opzione selezionata

    current_row = 0
    draw_menu(stdscr, current_row)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_DOWN and current_row < 3:
            current_row += 1
        elif key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == 10:  # Enter
            if current_row == 3:  # Verifica se l'opzione selezionata è "Exit"
                break  # Esci dal ciclo
            elif current_row == 0:  # "Nuova Partita"
                curses.curs_set(1)
                nuova_partita()
            elif current_row == 1:  # "Regole"
                regole(stdscr)
            elif current_row == 2:  # "Ruoli"
                ruoli()

        draw_menu(stdscr, current_row)

curses.wrapper(main)
