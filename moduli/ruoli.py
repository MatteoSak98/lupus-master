#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Giocatore:
    def __init__(self, ID, nome):
        self.ID = ID
        self.nome = nome
        self.status = 'Vivo'
        self.indicato_da = []
        self.al_rogo = False
        
class Villico(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Villico'
       self.fazione = 'Buono'
       self.visto_come = 'Buono'
       self.priorita = 999
       self.assassini = ['Giustiziere', 'Boia', 'Wendigo', 'Lupo']
       self.descrizione = '''
       Sei un semplice villico. 
       Durante la notte devi solo sperare di non essere sbranato dai lupi. 
       Di giorno devi cercare di mandare al rogo i lupi e i loro eventuali complici.
       Non sai nulla degli altri personaggi.
       Vinci se tutti i lupi vengono eliminati.
       '''

    def morte(self):
        check = set(self.assassini) & set(self.indicato_da)
        if 'Lupo' in check and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False

class Lupo(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Lupo'
       self.fazione = 'Cattivo'
       self.visto_come = 'Cattivo'
       self.priorita = 50
       self.assassini = ['Giustiziere', 'Wendigo']
       self.descrizione = '''
       Sei un lupo. Ogni notte, in accordo con gli altri lupi, decidete chi sbranare. 
       Durante il giorno, dovete cercare di sviare ogni sospetto e non farvi mandare al rogo dai villici.
       La prima notte saprai chi sono gli altri membri del tuo branco e i tuoi eventuali complici.
       Vinci se il numero dei lupi è uguale o superiore al numero dei villici e se sono stati eliminati eventuali giocatori solitari (wendigo, untore, ecc…).
       '''

    def indica(self, villaggio):
        while True:
            # se sei stato bloccato dall'illusionista o dallo stregone oscuro:
            n_lupi_vivi = [lupi.ID for lupi in villaggio.abitanti if lupi.ruolo == 'Lupo' and lupi.status == 'Vivo']
            if len(n_lupi_vivi) == 1:
                if 'Illusionista' in self.indicato_da or 'Stregone' in self.indicato_da:
                    input(f"{self.ruolo}: ---- (BLOCCATO)")
                    break
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

    def morte(self):
        check = set(self.assassini) & set(self.indicato_da)
        if check:
            self.status = 'Morto'
            return True
        else:
            return False

class Cavaliere(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Cavaliere'
       self.fazione = 'Buono'
       self.visto_come = 'Buono'
       self.priorita = 40
       self.assassini = ['Giustiziere', 'Boia', 'Wendigo', 'Lupo']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            while True:
                if 'Illusionista' in self.indicato_da or 'Stregone' in self.indicato_da:
                    input(f"{self.ruolo}: ---- (BLOCCATO)")
                    break
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

    def morte(self):
        check = set(self.assassini) & set(self.indicato_da)
        if 'Lupo' in check and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False

class Veggente(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Veggente'
       self.fazione = 'Buono'
       self.visto_come = 'Buono'
       self.priorita = 30
       self.assassini = ['Giustiziere', 'Boia', 'Wendigo', 'Lupo']
       
    def indica(self, villaggio):
        if self.status == 'Vivo':
            while True:
                if 'Illusionista' in self.indicato_da or 'Stregone' in self.indicato_da:
                    input(f"{self.ruolo}: ---- (BLOCCATO)")
                    break
                altro_giocatore = input(f"{self.ruolo}: ")
                if altro_giocatore:
                    altro_giocatore = int(altro_giocatore)
                    giocatori_indicabili = [altro_giocatore.ID for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo' and altro_giocatore.ruolo != 'Veggente']
                    if altro_giocatore in giocatori_indicabili:
                        indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                        if 'Insinuo' in indicato.indicato_da:
                            if indicato.visto_come == 'Buono':
                                visione = 'Cattivo'
                            else:
                                visione = 'Buono'
                        else:
                            visione = indicato.visto_come
                        print(f'  --> {indicato.nome} è {visione}')
                        break
                    else:
                        print("Giocatore indicato non valido")
                else:
                    print("Il veggente deve indicare un giocatore: ")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self):
        check = set(self.assassini) & set(self.indicato_da)
        if 'Lupo' in check and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False

class Giustiziere(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Giustiziere'
       self.fazione = 'Buono'
       self.visto_come = 'Buono'
       self.priorita = 150
       self.attivato = False
       self.assassini = ['Boia', 'Wendigo', 'Lupo']
       
    def indica(self, villaggio):
        if self.status == 'Vivo':
            if self.attivato == False:
                # se il gisutiziere può sparare
                while True:
                    if 'Illusionista' in self.indicato_da or 'Stregone' in self.indicato_da:
                        input(f"{self.ruolo}: ---- (BLOCCATO)")
                        break
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
                            self.attivato = True
                            break
                        else:
                            print("Giocatore indicato non valido")
            else:
                input(f"{self.ruolo}: ---- (Azione già attivata)")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self):
        check = set(self.assassini) & set(self.indicato_da)
        if 'Lupo' in check and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False

class Insinuo(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Insinuo'
       self.fazione = 'Cattivo'
       self.visto_come = 'Buono'
       self.priorita = 20
       self.assassini = ['Giustiziere', 'Wendigo']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            while True:
                if 'Illusionista' in self.indicato_da or 'Stregone' in self.indicato_da:
                    input(f"{self.ruolo}: ---- (BLOCCATO)")
                    break
                altro_giocatore = input(f"{self.ruolo}: ")
                if altro_giocatore:
                    altro_giocatore = int(altro_giocatore)
                    giocatori_indicabili = [altro_giocatore.ID for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo' and altro_giocatore.ruolo != 'Insinuo']
                    if altro_giocatore in giocatori_indicabili:
                        indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                        indicato.indicato_da.append('Insinuo')
                        break
                    else:
                        print("Giocatore indicato non valido")
                else:
                    print("L'insinuo deve indicare un giocatore da insinuare:")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self):
        check = set(self.assassini) & set(self.indicato_da)
        if check:
            self.status = 'Morto'
            return True
        else:
            return False

class Illusionista(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Illusionista'
       self.fazione = 'Cattivo'
       self.visto_come = 'Cattivo'
       self.priorita = 15
       self.assassini = ['Giustiziere', 'Wendigo']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            while True:
                altro_giocatore = input(f"{self.ruolo}: ")
                if altro_giocatore:
                    altro_giocatore = int(altro_giocatore)
                    giocatori_indicabili = [altro_giocatore.ID for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo' and altro_giocatore.ruolo != 'Illusionista']
                    if altro_giocatore in giocatori_indicabili:
                        indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                        indicato.indicato_da.append('Illusionista')
                        break
                    else:
                        print("Giocatore indicato non valido")
                else:
                    print("L'illusionista deve indicare un giocatore da bloccare per questo turno:")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self):
        check = set(self.assassini) & set(self.indicato_da)
        if check:
            self.status = 'Morto'
            return True
        else:
            return False

class Stregone(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Stregone'
       self.fazione = 'Cattivo'
       self.visto_come = 'Cattivo'
       self.priorita = 10
       self.attivato = False
       self.assassini = ['Giustiziere', 'Wendigo']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            if 'Illusionista' in self.indicato_da:
                input(f"{self.ruolo}: ---- (BLOCCATO)")
            elif self.attivato == False:
                attiva = input(f"{self.ruolo} (y=attiva, ENTER=skip): ")
                if attiva == 'y':
                    giocatori_indicabili = [altro_giocatore for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo' and altro_giocatore.fazione == 'Buono']
                    for giocatore in giocatori_indicabili:
                        giocatore.indicato_da.append('Stregone')
                    self.attivato = True
            else:
                input(f"{self.ruolo}: ---- (Azione già attivata)")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self):
        check = set(self.assassini) & set(self.indicato_da)
        if check:
            self.status = 'Morto'
            return True
        else:
            return False

class Matto(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Matto'
       self.fazione = 'Rubavittoria'
       self.visto_come = 'Buono'
       self.priorita = 998
       self.assassini = ['Giustiziere', 'Boia', 'Wendigo', 'Lupo']

    def morte(self):
        check = set(self.assassini) & set(self.indicato_da)
        if 'Lupo' in check and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False

class Boia(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Boia'
       self.fazione = 'Cattivo'
       self.visto_come = 'Cattivo'
       self.priorita = 140
       self.attivato = False
       self.assassini = ['Giustiziere', 'Wendigo']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            if self.attivato == False:
                # se il boia può agire
                while True:
                    if 'Illusionista' in self.indicato_da:
                        input(f"{self.ruolo}: ---- (BLOCCATO)")
                        break
                    altro_giocatore = input(f"{self.ruolo}: ")
                    if not altro_giocatore:
                        # il boia può decidere di non agire
                        break
                    else:
                        # se decide di agire
                        altro_giocatore = int(altro_giocatore)
                        giocatori_indicabili = [altro_giocatore.ID for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo' and altro_giocatore.ruolo != 'Boia']
                        if altro_giocatore in giocatori_indicabili:
                            indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                            ruolo_indovinato = input('  --> Indovina il ruolo: ')
                            if ruolo_indovinato == indicato.ruolo:
                                indicato.indicato_da.append('Boia')
                                self.attivato = True
                            else:
                                self.indicato_da.append('Boia')
                            break
                        else:
                            print("Giocatore indicato non valido")
            else:
                input(f"{self.ruolo}: ---- (Azione già attivata)")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self):
        check = set(self.assassini) & set(self.indicato_da)
        if check:
            self.status = 'Morto'
            return True
        else:
            return False

class Wendigo(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Wendigo'
       self.fazione = 'Rubavittoria'
       self.visto_come = 'Cattivo'
       self.priorita = 130
       self.assassini = ['Giustiziere', 'Boia']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            while True:
                if 'Illusionista' in self.indicato_da or 'Stregone' in self.indicato_da:
                    input(f"{self.ruolo}: ---- (BLOCCATO)")
                    break
                altro_giocatore = input(f"{self.ruolo}: ")
                if altro_giocatore:
                    altro_giocatore = int(altro_giocatore)
                    giocatori_indicabili = [altro_giocatore.ID for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo' and altro_giocatore.ruolo != 'Wendigo']
                    if altro_giocatore in giocatori_indicabili:
                        indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                        ruolo_indovinato = input('  --> Indovina il ruolo: ')
                        if ruolo_indovinato == indicato.ruolo:
                            indicato.indicato_da.append('Wendigo')
                        break
                    else:
                        print("Giocatore indicato non valido")
                else:
                    print("Il Wendigo deve indicare un giocatore e può ucciderlo se indovina il suo ruolo:")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self):
        check = set(self.assassini) & set(self.indicato_da)
        if check:
            self.status = 'Morto'
            return True
        else:
            return False