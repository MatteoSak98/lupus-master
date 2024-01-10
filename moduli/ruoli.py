#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Giocatore:
    def __init__(self, ID, nome):
        self.ID = ID
        self.nome = nome
        self.status = 'Vivo'
        self.indicato_da = []
        
class Villico(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Villico'
       self.fazione = 'Buono'
       self.visto_come = 'Buono'
       self.priorita = 999
       self.descrizione = '''
       Sei un semplice villico. 
       Durante la notte devi solo sperare di non essere sbranato dai lupi. 
       Di giorno devi cercare di mandare al rogo i lupi e i loro eventuali complici.
       Non sai nulla degli altri personaggi.
       Vinci se tutti i lupi vengono eliminati.
       '''

class Lupo(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Lupo'
       self.fazione = 'Cattivo'
       self.visto_come = 'Cattivo'
       self.priorita = 50
       self.descrizione = '''
       Sei un lupo. Ogni notte, in accordo con gli altri lupi, decidete chi sbranare. 
       Durante il giorno, dovete cercare di sviare ogni sospetto e non farvi mandare al rogo dai villici.
       La prima notte saprai chi sono gli altri membri del tuo branco e i tuoi eventuali complici.
       Vinci se il numero dei lupi è uguale o superiore al numero dei villici e se sono stati eliminati eventuali giocatori solitari (wendigo, untore, ecc…).
       '''

    def indica(self, villaggio):
        while True:
            altro_giocatore = input(f"{self.ruolo}: ")
            if altro_giocatore:
                altro_giocatore = int(altro_giocatore)
                giocatori_indicabili = [altro_giocatore.ID for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo' and altro_giocatore.ruolo != 'Lupo']
                if altro_giocatore in giocatori_indicabili:
                    indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                    indicato.indicato_da.append('Lupo')
                    break
                else:
                    print("Giocatore indicato non valido")
            else:
                print("I lupi devono indicare un giocatore da uccidere: ")                

class Cavaliere(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Cavaliere'
       self.fazione = 'Buono'
       self.visto_come = 'Buono'
       self.priorita = 40

    def indica(self, villaggio):
        if self.status == 'Vivo':
            while True:
                altro_giocatore = input(f"{self.ruolo}: ")
                if altro_giocatore:
                    altro_giocatore = int(altro_giocatore)
                    giocatori_indicabili = [altro_giocatore.ID for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo' and altro_giocatore.ruolo != 'Cavaliere']
                    if altro_giocatore in giocatori_indicabili:
                        indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                        indicato.indicato_da.append('Cavaliere')
                        break
                    else:
                        print("Giocatore indicato non valido")
                else:
                    print("Il cavaliere deve indicare un giocatore da proteggere:")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

class Veggente(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Veggente'
       self.fazione = 'Buono'
       self.visto_come = 'Buono'
       self.priorita = 30
       
    def indica(self, villaggio):
        if self.status == 'Vivo':
            while True:
                altro_giocatore = input(f"{self.ruolo}: ")
                if altro_giocatore:
                    altro_giocatore = int(altro_giocatore)
                    giocatori_indicabili = [altro_giocatore.ID for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo' and altro_giocatore.ruolo != 'Veggente']
                    if altro_giocatore in giocatori_indicabili:
                        indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                        print(f'  --> {indicato.nome} è {indicato.visto_come}')
                        break
                    else:
                        print("Giocatore indicato non valido")
                else:
                    print("Il veggente deve indicare un giocatore: ")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")
        
class Giustiziere(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Giustiziere'
       self.fazione = 'Buono'
       self.visto_come = 'Buono'
       self.priorita = 150
       self.sparato = False
       
    def indica(self, villaggio):
        if self.status == 'Vivo':
            if self.sparato == False:
                # se il gisutiziere può sparare
                while True:
                    altro_giocatore = input(f"{self.ruolo}: ")
                    if not altro_giocatore:
                        # il giustiziere può decidere di non sparare
                        break
                    else:
                        # se decide di sparare
                        altro_giocatore = int(altro_giocatore)
                        giocatori_indicabili = [altro_giocatore.ID for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo' and altro_giocatore.ruolo != 'Giustiziere']
                        if altro_giocatore in giocatori_indicabili:
                            indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                            indicato.indicato_da.append('Giustiziere')
                            self.sparato = True
                            break
                        else:
                            print("Giocatore indicato non valido")
            else:
                input(f"{self.ruolo}: ---- (Azione già attivata)")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")
