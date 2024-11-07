#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from moduli.funzioni import read_setup, recap, assegnazione_ruoli, condizioni_vittoria, timer

# -----------------------------------------------------------------------------
# Menu principale
# -----------------------------------------------------------------------------

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

os.system('clear')
print(title)
input('Premi ENTER per iniziare una nuova partita...')

# -----------------------------------------------------------------------------
# Inizializzazione
# -----------------------------------------------------------------------------

os.system('clear')
print('----------------------------------')
print("TURNO 0")
print('----------------------------------')

ruoli, giocatori = read_setup('setup.yml')
for numero, nome in giocatori.items():
    print(f"{numero} - {nome}", end="\n")

print('----------------------------------')
print('NOTTE')
print('----------------------------------')

villaggio = assegnazione_ruoli(giocatori, ruoli)

print('----------------------------------')
print('GIORNO')
print('----------------------------------')
input('Nominate un sindaco del villaggio...')
print('----------------------------------')

input("\nPremi ENTER per passare alla notte successiva...")

# -----------------------------------------------------------------------------
# Inizio partita
# -----------------------------------------------------------------------------
vittoria = False
villaggio.turno = 1

os.system('clear')
while not vittoria:

    print('----------------------------------')
    print(f'TURNO {villaggio.turno}')
    print('----------------------------------')

    recap(villaggio)

    print('----------------------------------')
    print('NOTTE')
    print('----------------------------------')

    # durante la notte chiama i ruoli in ordine di priorità. Escludi i Villici
    lupi_già_chiamati = False
    for abitante in sorted(villaggio.abitanti, key=lambda x: x.priorita):
        if abitante.ruolo == 'Contadino':
            continue
        if abitante.ruolo == 'Matto':
            continue
        if abitante.ruolo == 'Lupo':
            if abitante.status == 'Vivo':
                # l'intera fazione dei lupi va chiamata una sola volta
                if not lupi_già_chiamati:
                    # controllo se entrambi i lupi sono morti
                    lupi_vivi = [lupi.status for lupi in villaggio.abitanti if lupi.ruolo == 'Lupo' and lupi.status == 'Vivo']
                    if lupi_vivi:
                        abitante.indica(villaggio)
                        lupi_già_chiamati = True
                    else:
                        while True:
                            prompt = input(f"{abitante.ruolo}: ---- (MORTO)")
                            if prompt:
                                print('Entrambi i lupi sono morti e non possono indicare nessuno, premi ENTER e basta!')
                            else:
                                break
        else:
            abitante.indica(villaggio)

    # risultato della notte
    nessun_morto = True
    for abitante in villaggio.abitanti:
        if abitante.morte(villaggio):
            nessun_morto = False
            print(f'  --> {abitante.nome} è morto!')
        # reset azione della notte appena trascorsa
        abitante.indicato_da = []
    if nessun_morto:
        print('  --> Non è morto nessuno!')

    # verifica le condizioni di vittoria:
    if condizioni_vittoria(villaggio):
        break

    # Votazione del giorno
    print('----------------------------------')
    print('GIORNO')
    print('----------------------------------')

    timer(600)

    while True:
        rogo = input("Giocatore da mandare al rogo: ")
        if rogo:
            rogo = int(rogo)
            abitante_al_rogo = next((x for x in villaggio.abitanti if x.ID == rogo), None)
            if abitante_al_rogo.status == 'Morto':
                print('Giocatore non valido, è già morto!!')
            else:
                abitante_al_rogo.status = 'Morto'
                abitante_al_rogo.al_rogo = True
                break
        else:
            print("Inserisci l'ID di un giocatore da mandare al rogo: ")
    
    print(f'  --> {abitante_al_rogo.nome} è stato mandato al rogo')
    print('----------------------------------')

    input("\nPremi ENTER per passare alla notte successiva...")

    # verifica le condizioni di vittoria:
    for personaggio in villaggio.abitanti:
        if personaggio.vittoria(villaggio):
            break
    # if condizioni_vittoria(villaggio):
    #     break

    villaggio.turno += 1

# in caso di vittoria:
input('Premi ENTER per visualizzare il recap...')
print('----------------------------------')
recap(villaggio)
print('----------------------------------')