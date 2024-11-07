#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
import time
from moduli.ruoli import *

class Villaggio:
    def __init__(self):
        self.turno = 1
        self.abitanti = []
        self.ruoli = []
        self.giocatori = []

    def condizioni_vittoria(self):
        self.vivi = len([g.ID for g in self.abitanti if g.status == 'Vivo'])
        self.lupi_vivi = len([lupi.ID for lupi in self.abitanti if lupi.ruolo == 'Lupo' and lupi.status == 'Vivo'])
        self.wendigo_vivo = bool([w.ID for w in self.abitanti if w.ruolo == 'Wendigo' and w.status == 'Vivo'])
        self.matto_vivo = bool([m.ID for m in self.abitanti if m.ruolo == 'Matto' and m.status == 'Vivo'])
        self.matto_morto_al_rogo = bool([matto.ID for matto in self.abitanti if matto.ruolo == 'Matto' and matto.al_rogo == True])
        self.tutti_contagiati = all(abitante.contagiato for abitante in self.abitanti if abitante.status == 'Vivo')

def read_setup(setup_file):
    ### Inserire controllo N ruoli == N Giocatori!!
    with open(setup_file, 'r') as file:
        setup = yaml.safe_load(file)
    if 'Giocatori' in setup:
        lista_giocatori = setup['Giocatori']
        giocatori = {i + 1: f"{nome}" for i, nome in enumerate(lista_giocatori)}
    else:
        print('Inserisci i nomi dei giocatori nel file di setup')
    if 'Ruoli' in setup:
        lista_ruoli = setup['Ruoli']
    else:
        print('Inserisci i ruoli nel file di setup')  
        
    return lista_ruoli, giocatori
    

def inputID_init(ruolo, giocatori):
    while True:
        # Chiedi all'utente di inserire l'ID del giocatore da assegnare al ruolo
        player_id = input(f"{ruolo}: ")
        if player_id:
            player_id = int(player_id)
            # Verifica se il numero inserito è presente nella lista
            if player_id in giocatori.keys():
                return player_id
            else:
                print(f"ID non valido [{min(giocatori.keys())}-{max(giocatori.keys())}]")
        else:
            print("Inserisci l'ID di un giocatore")

def assegnazione_ruoli(giocatori, lista_ruoli):
    villaggio = Villaggio()
    ruoli = {}

    # Assegnazione ruoli
    for ruolo in lista_ruoli:
        if ruolo == 'Contadino':
            pass
        else:
            while True:
                ID = inputID_init(ruolo, giocatori)
                if ID in ruoli.keys():
                    print("ID già assegnato")
                else:
                    ruoli[ID] = ruolo
                    break

    # assegnazione villici
    for ID in giocatori.keys():
        if ID not in ruoli.keys():
            ruoli[ID] = 'Contadino'

    # assegnazione abitanti al villaggio
    for ID in giocatori.keys():
        if ruoli[ID] == 'Lupo':
            nuovo_ruolo = Lupo(ID, giocatori[ID])   
        if ruoli[ID] == 'Contadino':
            nuovo_ruolo = Contadino(ID, giocatori[ID])
        if ruoli[ID] == 'Cavaliere':
            nuovo_ruolo = Cavaliere(ID, giocatori[ID])
        if ruoli[ID] == 'Veggente':
            nuovo_ruolo = Veggente(ID, giocatori[ID])
        if ruoli[ID] == 'Medium':
            nuovo_ruolo = Medium(ID, giocatori[ID])
        if ruoli[ID] == 'Beccamorto':
            nuovo_ruolo = Beccamorto(ID, giocatori[ID])
        if ruoli[ID] == 'Giustiziere':
            nuovo_ruolo = Giustiziere(ID, giocatori[ID])
        if ruoli[ID] == 'Insinuo':
            nuovo_ruolo = Insinuo(ID, giocatori[ID])
        if ruoli[ID] == 'Illusionista':
            nuovo_ruolo = Illusionista(ID, giocatori[ID])
        if ruoli[ID] == 'Strega':
            nuovo_ruolo = Strega(ID, giocatori[ID])
        if ruoli[ID] == 'Matto':
            nuovo_ruolo = Matto(ID, giocatori[ID])
        if ruoli[ID] == 'Boia':
            nuovo_ruolo = Boia(ID, giocatori[ID])
        if ruoli[ID] == 'Wendigo':
            nuovo_ruolo = Wendigo(ID, giocatori[ID])
        if ruoli[ID] == 'Ammaestratore':
            nuovo_ruolo = Ammaestratore(ID, giocatori[ID])
        if ruoli[ID] == 'Indemoniato':
            nuovo_ruolo = Indemoniato(ID, giocatori[ID])
        if ruoli[ID] == 'Mitomane':
            nuovo_ruolo = Mitomane(ID, giocatori[ID])
        if ruoli[ID] == 'Untore':
            nuovo_ruolo = Untore(ID, giocatori[ID])
        villaggio.abitanti.append(nuovo_ruolo)

    villaggio.giocatori = giocatori
    villaggio.ruoli = ruoli
    return villaggio

def recap(villaggio):
    if 'Untore' in villaggio.ruoli.values():
        for abitante in sorted(villaggio.abitanti, key=lambda x: x.ID):
            print(f"{abitante.ID:<2} {abitante.nome:<10} {abitante.ruolo:<15} {abitante.status:<5} {abitante.contagiato:<5}")
    else:
        for abitante in sorted(villaggio.abitanti, key=lambda x: x.ID):
            print(f"{abitante.ID:<2} {abitante.nome:<10} {abitante.ruolo:<15} {abitante.status:<5}")

def condizioni_vittoria(v):
    v.condizioni_vittoria()
    # condizione vittoria dei personaggi solitari:
    #   ogni personaggio solitario ha delle proprie condizioni di vittoria
    if v.tutti_contagiati:
        print('L\'untore vince la partita!\n')
        return True
    elif v.wendigo_vivo and v.vivi == 2:
        print('Il wendigo vince la partita!\n')
        return True
    elif v.matto_morto_al_rogo:
        print('Il matto vince la partita!\n')
        return True
    # condizione vittoria dei villici:
    #   sono morti tutti i lupi e tutti i personaggi solitari
    elif (not v.lupi_vivi) and (not v.wendigo_vivo) and (not v.matto_vivo) and (not v.matto_morto_al_rogo):
        print('I villici vincono la partita!\n')
        return True
    # condizione vittoria dei lupi:
    #   sono morti tutti i personaggi solitari e il numero di lupi == numero altri giocatori
    elif (v.lupi_vivi == (v.vivi - v.lupi_vivi)) and (not v.wendigo_vivo) and (not v.matto_vivo) and (not v.matto_morto_al_rogo):
        print('I lupi vincono la partita!\n')
        return True
    else:
        return False

def timer(duration):
    start_time = time.time()
    try:
        while True:
            elapsed_time = time.time() - start_time
            remaining_time = max(duration - elapsed_time, 0)

            minutes, seconds = divmod(int(remaining_time), 60)
            timer_display = f"{minutes:02d}:{seconds:02d}"

            print(f"Timer: {timer_display}           skip=CTRL+C", end='\r')

            if elapsed_time >= duration:
                print("\nTempo scaduto!")
                break

    except KeyboardInterrupt:
        print("\nTempo scaduto!")
