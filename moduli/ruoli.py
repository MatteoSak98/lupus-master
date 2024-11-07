#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Giocatore:
    def __init__(self, ID, nome):
        self.ID = ID
        self.nome = nome
        self.status = 'Vivo'
        self.indicato_da = []
        self.al_rogo = False
        self.contagiato = False
        
class Contadino(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Contadino'
       self.fazione = 'Villaggio'
       self.aura = 'Buono'
       self.priorita = 999
       self.assassini = ['Giustiziere', 'Boia', 'Wendigo', 'Lupo', 'Ammaestratore']
       self.descrizione = '''
       Sei un semplice contadino. 
       Durante la notte devi solo sperare di non essere sbranato dai lupi. 
       Di giorno devi cercare di mandare al rogo i lupi e i loro eventuali complici.
       Non sai nulla degli altri personaggi.
       Vinci se tutti i lupi vengono eliminati.
       '''

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if ('Lupo' in check or 'Ammaestratore' in check) and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False
        
    def vittoria(self, villaggio):
        test = villaggio.condizioni_vittoria()
        print(test)

class Lupo(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Lupo'
       self.fazione = "Creature dell'Ombra"
       self.aura = 'Oscura'
       self.priorita = 50
       self.assassini = ['Giustiziere', 'Wendigo', 'Ammaestratore']
       self.descrizione = '''
       Sei un lupo. Ogni notte, in accordo con gli altri lupi, decidete chi sbranare. 
       Durante il giorno, dovete cercare di sviare ogni sospetto e non farvi mandare al rogo dal Villaggio.
       La prima notte saprai chi sono gli altri membri del tuo branco e i tuoi eventuali complici.
       Vinci se la fazione delle Creature dell'Ombra è l'unica rimasta in gioco.
       '''

    def indica(self, villaggio):
        while True:
            # se sei stato bloccato dall'illusionista o dallo stregone oscuro:
            n_lupi_vivi = [lupi.ID for lupi in villaggio.abitanti if lupi.ruolo == 'Lupo' and lupi.status == 'Vivo']
            if len(n_lupi_vivi) == 1:
                if 'Illusionista' in self.indicato_da or 'Strega' in self.indicato_da:
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

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if 'Ammaestratore' in check and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False
    
    def vittoria(self, villaggio):
        pass

class Cavaliere(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Cavaliere'
       self.fazione = 'Buono'
       self.aura = 'Chiara'
       self.priorita = 40
       self.assassini = ['Giustiziere', 'Boia', 'Wendigo', 'Lupo', 'Ammaestratore']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            while True:
                if 'Illusionista' in self.indicato_da or 'Strega' in self.indicato_da:
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

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if ('Lupo' in check or 'Ammaestratore' in check) and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False
    
    def vittoria(self, villaggio):
        pass

class Veggente(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Veggente'
       self.fazione = 'Villaggio'
       self.aura = 'Chiara'
       self.priorita = 30
       self.assassini = ['Giustiziere', 'Boia', 'Wendigo', 'Lupo', 'Ammaestratore']
       
    def indica(self, villaggio):
        if self.status == 'Vivo':
            while True:
                if 'Illusionista' in self.indicato_da or 'Strega' in self.indicato_da:
                    input(f"{self.ruolo}: ---- (BLOCCATO)")
                    break
                altro_giocatore = input(f"{self.ruolo}: ")
                if altro_giocatore:
                    altro_giocatore = int(altro_giocatore)
                    giocatori_indicabili = [altro_giocatore.ID for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo' and altro_giocatore.ruolo != 'Veggente']
                    if altro_giocatore in giocatori_indicabili:
                        indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                        if 'Insinuo' in indicato.indicato_da:
                            if indicato.aura == 'Chiara':
                                visione = 'Cattivo'
                            else:
                                visione = 'Buono'
                        else:
                            visione = indicato.aura
                        print(f'  --> {indicato.nome} ha aura {visione}')
                        break
                    else:
                        print("Giocatore indicato non valido")
                else:
                    print("Il veggente deve indicare un giocatore: ")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if ('Lupo' in check or 'Ammaestratore' in check) and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False
    
    def vittoria(self, villaggio):
        pass

class Medium(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Medium'
       self.fazione = 'Villaggio'
       self.aura = 'Chiara'
       self.priorita = 35
       self.assassini = ['Giustiziere', 'Boia', 'Wendigo', 'Lupo', 'Ammaestratore']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            while True:
                if 'Illusionista' in self.indicato_da or 'Strega' in self.indicato_da:
                    input(f"{self.ruolo}: ---- (BLOCCATO)")
                    break
                else:
                    if villaggio.turno == 1:
                        altro_giocatore = input(f"{self.ruolo}: ---- (NON ATTIVO)")
                        break
                    else:
                        altro_giocatore = input(f"{self.ruolo}: ")
                        if altro_giocatore:
                            altro_giocatore = int(altro_giocatore)
                            giocatori_indicabili = [altro_giocatore.ID for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Morto']
                            if altro_giocatore in giocatori_indicabili:
                                indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                                print(f'  --> {indicato.nome} aveva aura {indicato.aura}')
                                break
                            else:
                                print("Giocatore indicato non valido")
                        else:
                            print("Il medium deve indicare un giocatore morto del quale vuole conoscere la fazione: ")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")
    
    def vittoria(self, villaggio):
        pass

class Beccamorto(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Beccamorto'
       self.fazione = 'Buono'
       self.aura = 'Chiara'
       self.priorita = 60
       self.assassini = ['Giustiziere', 'Boia', 'Wendigo', 'Lupo', 'Ammaestratore']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            while True:
                if 'Illusionista' in self.indicato_da or 'Strega' in self.indicato_da:
                    input(f"{self.ruolo}: ---- (BLOCCATO)")
                    break
                else:
                    if villaggio.turno <= 0:
                        richiesta = input(f"{self.ruolo}: ---- (NON ATTIVO)")
                        break
                    else:
                        richiesta = input(f"{self.ruolo}: ")
                        if richiesta in villaggio.ruoli.values():
                            risposta = [g.status for g in villaggio.abitanti if g.ruolo == richiesta]
                            if 'Vivo' in risposta:
                                print(f'  --> {richiesta} è vivo')
                            else:
                                print(f'  --> {richiesta} è morto')
                            break
                        else:
                            print("Il beccamorto deve chiedere se un ruolo è ancora in vita. Inserisci un ruolo valido: ")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if ('Lupo' in check or 'Ammaestratore' in check) and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False
    
    def vittoria(self, villaggio):
        pass

class Giustiziere(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Giustiziere'
       self.fazione = 'Buono'
       self.aura = 'Chiara'
       self.priorita = 150
       self.attivato = False
       self.assassini = ['Boia', 'Wendigo', 'Lupo', 'Ammaestratore']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            if self.attivato == False:
                # se il gisutiziere può sparare
                while True:
                    if 'Illusionista' in self.indicato_da or 'Strega' in self.indicato_da:
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

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if ('Lupo' in check or 'Ammaestratore' in check) and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False
    
    def vittoria(self, villaggio):
        pass

class Insinuo(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Insinuo'
       self.fazione = 'Cattivo'
       self.aura = 'Chiara'
       self.priorita = 20
       self.assassini = ['Giustiziere', 'Wendigo', 'Ammaestratore']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            while True:
                if 'Illusionista' in self.indicato_da or 'Strega' in self.indicato_da:
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

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if 'Ammaestratore' and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False
    
    def vittoria(self, villaggio):
        pass

class Illusionista(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Illusionista'
       self.fazione = 'Cattivo'
       self.aura = 'Oscura'
       self.priorita = 15
       self.assassini = ['Giustiziere', 'Wendigo', 'Ammaestratore']

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

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if 'Ammaestratore' and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False
    
    def vittoria(self, villaggio):
        pass

class Strega(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Strega'
       self.fazione = 'Villaggio'
       self.aura = 'Oscura'
       self.priorita = 10
       self.attivato = False
       self.assassini = ['Giustiziere', 'Wendigo', 'Ammaestratore']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            if 'Illusionista' in self.indicato_da:
                input(f"{self.ruolo}: ---- (BLOCCATO)")
            elif self.attivato == False:
                attiva = input(f"{self.ruolo} (y=attiva, ENTER=skip): ")
                if attiva == 'y':
                    giocatori_indicabili = [altro_giocatore for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo' and altro_giocatore.fazione == 'Buono']
                    for giocatore in giocatori_indicabili:
                        giocatore.indicato_da.append('Strega')
                    self.attivato = True
            else:
                input(f"{self.ruolo}: ---- (Azione già attivata)")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if 'Ammaestratore' in check and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False
    
    def vittoria(self, villaggio):
        pass

class Matto(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Matto'
       self.fazione = 'Matto'
       self.aura = 'Chiara'
       self.priorita = 998
       self.assassini = ['Giustiziere', 'Boia', 'Wendigo', 'Lupo', 'Ammaestratore']

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if ('Lupo' in check or 'Ammaestratore' in check) and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False
    
    def vittoria(self, villaggio):
        pass

class Boia(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Boia'
       self.fazione = 'Inquisizione'
       self.aura = 'Oscura'
       self.priorita = 140
       self.attivato = False
       self.assassini = ['Giustiziere', 'Wendigo', 'Ammaestratore', 'Boia']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            if self.attivato == False:
                # se il boia può agire
                condizione_uscita = False
                while not condizione_uscita:
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
                            # itera fino a che viene inserito un ruolo valido
                            ruolo_indovinato = input('  --> Indovina il ruolo: ')
                            while not condizione_uscita:
                                if ruolo_indovinato in villaggio.ruoli.values():
                                    if ruolo_indovinato == indicato.ruolo:
                                        indicato.indicato_da.append('Boia')
                                        self.attivato = True
                                    else:
                                        self.indicato_da.append('Boia')
                                    condizione_uscita = True
                                else:
                                    ruolo_indovinato = input("  --> Ruolo non valido. Indovina il ruolo: ")
                        else:
                            print("Giocatore indicato non valido")
            else:
                input(f"{self.ruolo}: ---- (Azione già attivata)")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if 'Ammaestratore' in check and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False
    
    def vittoria(self, villaggio):
        pass

class Wendigo(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Wendigo'
       self.fazione = 'Rubavittoria'
       self.aura = 'Oscura'
       self.priorita = 130
       self.assassini = ['Giustiziere', 'Boia']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            condizione_uscita = False
            while not condizione_uscita:
                if 'Illusionista' in self.indicato_da or 'Strega' in self.indicato_da:
                    input(f"{self.ruolo}: ---- (BLOCCATO)")
                    break
                altro_giocatore = input(f"{self.ruolo}: ")
                if altro_giocatore:
                    altro_giocatore = int(altro_giocatore)
                    giocatori_indicabili = [altro_giocatore.ID for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo' and altro_giocatore.ruolo != 'Wendigo']
                    if altro_giocatore in giocatori_indicabili:
                        indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                        # itera fino a che viene inserito un ruolo valido
                        ruolo_indovinato = input('  --> Indovina il ruolo: ')
                        while not condizione_uscita:
                            if ruolo_indovinato in villaggio.ruoli.values():
                                if ruolo_indovinato == indicato.ruolo:
                                    indicato.indicato_da.append('Wendigo')
                                condizione_uscita = True
                            else:
                                ruolo_indovinato = input("  --> Ruolo non valido. Indovina il ruolo: ")
                    else:
                        print("Giocatore indicato non valido")
                else:
                    print("Il Wendigo deve indicare un giocatore e può ucciderlo se indovina il suo ruolo:")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if check:
            self.status = 'Morto'
            return True
        else:
            return False
    
    def vittoria(self, villaggio):
        pass

class Ammaestratore(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Ammaestratore'
       self.fazione = 'Buono'
       self.aura = 'Chiara'
       self.priorita = 55
       self.assassini = ['Giustiziere', 'Boia', 'Wendigo', 'Lupo']
       self.attivato = False
       self.descrizione = '''
       '''

    def indica(self, villaggio):
        if self.status == 'Vivo':
            if self.attivato == False:
                while True:
                    # se sei stato bloccato dall'illusionista o dallo stregone oscuro:
                    n_lupi_vivi = [lupi.ID for lupi in villaggio.abitanti if lupi.ruolo == 'Lupo' and lupi.status == 'Vivo']
                    if len(n_lupi_vivi) == 1:
                        if 'Illusionista' in self.indicato_da or 'Strega' in self.indicato_da:
                            input(f"{self.ruolo}: ---- (BLOCCATO)")
                            break
                    altro_giocatore = input(f"{self.ruolo}: ")
                    if not altro_giocatore:
                        # l'ammaestratore può decidere di non agire
                        break
                    if altro_giocatore:
                        altro_giocatore = int(altro_giocatore)
                        giocatori_indicabili = [altro_giocatore.ID for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo' and altro_giocatore.ruolo != 'Ammaestratore']
                        if altro_giocatore in giocatori_indicabili:
                            indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                            indicato.indicato_da.append('Ammaestratore')
                            self.attivato = True
                            break
                        else:
                            print("Giocatore indicato non valido")
            else:
                input(f"{self.ruolo}: ---- (Azione già attivata)")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if check:
            self.status = 'Morto'
            return True
        else:
            return False
    
    def vittoria(self, villaggio):
        pass

class Indemoniato(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Indemoniato'
       self.fazione = 'Buono'
       self.aura = 'Chiara'
       self.priorita = 60
       self.assassini = ['Giustiziere', 'Boia', 'Wendigo']
       self.descrizione = '''
       '''

    def indica(self, villaggio):
        if self.status == 'Vivo':
            if 'Lupo' in self.indicato_da or 'Ammaestratore' in self.indicato_da:
                input(f"{self.ruolo}: ---- (Ti sei trasformato in lupo)")
            else:
                input(f"{self.ruolo}: ---- (Rimani villico)")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if check:
            self.status = 'Morto'
            return True
        elif self.status == 'Vivo' and ('Lupo' in self.indicato_da or 'Ammaestratore' in self.indicato_da):
            print("  --> L'indemoniato si è trasformato in lupo")
            self.cambio_ruolo(villaggio)
            return False
        else:
            return False

    def cambio_ruolo(self, villaggio):
        # Cambia il ruolo da Indemoniato a Lupo
        nuovo_ruolo = Lupo(self.ID, self.nome)
        # Rimuovi l'Indemoniato dalla lista degli abitanti e aggiungi il nuovo Lupo
        villaggio.abitanti.remove(self)
        villaggio.abitanti.append(nuovo_ruolo)
        return True
    
    def vittoria(self, villaggio):
        pass

class Mitomane(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Mitomane'
       self.fazione = 'Buono'
       self.aura = 'Chiara'
       self.priorita = 1
       self.assassini = ['Giustiziere', 'Boia', 'Wendigo', 'Lupo', 'Ammaestratore']
       self.descrizione = '''
       '''

    def indica(self, villaggio):
        pass
        if self.status == 'Vivo':
            while True:
                if 'Illusionista' in self.indicato_da or 'Strega' in self.indicato_da:
                    input(f"{self.ruolo}: ---- (BLOCCATO)")
                    break
                else:
                    if villaggio.turno < 2:
                        altro_giocatore = input(f"{self.ruolo}: ---- (NON ATTIVO)")
                        break
                    else:
                        altro_giocatore = input(f"{self.ruolo}: ")
                        if altro_giocatore:
                            altro_giocatore = int(altro_giocatore)
                            giocatori_indicabili = [altro_giocatore.ID for altro_giocatore in villaggio.abitanti if altro_giocatore.status == 'Vivo']
                            if altro_giocatore in giocatori_indicabili:
                                indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                                if indicato.ruolo == 'Veggente':
                                    nuovo_ruolo = Veggente(self.ID, self.nome)
                                elif indicato.ruolo == 'Lupo':
                                    nuovo_ruolo = Lupo(self.ID, self.nome)
                                else:
                                    nuovo_ruolo = Contadino(self.ID, self.nome)
                                villaggio.abitanti.remove(self)
                                villaggio.abitanti.append(nuovo_ruolo)
                                break
                            else:
                                print("Giocatore indicato non valido")
                        else:
                            print("Il mitomane deve indicare un giocatore per diventare lupo o veggente: ")
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if ('Lupo' in check or 'Ammaestratore' in check) and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False
    
    def vittoria(self, villaggio):
        pass

class Untore(Giocatore):
    def __init__(self, ID, nome):
       super().__init__(ID, nome)
       self.ruolo = 'Untore'
       self.fazione = 'Rubavittoria'
       self.aura = 'Oscura'
       self.priorita = 250
       self.contagiato = True
       self.assassini = ['Giustiziere', 'Wendigo', 'Ammaestratore', 'Lupo', 'Boia']

    def indica(self, villaggio):
        if self.status == 'Vivo':
            while True:
                if 'Illusionista' in self.indicato_da or 'Strega' in self.indicato_da:
                    input(f"{self.ruolo}: ---- (BLOCCATO)")
                    break
                else:
                    giocatori_indicabili = [g.ID for g in villaggio.abitanti if g.status == 'Vivo' and g.contagiato == False and g.ruolo != 'Untore']
                    if giocatori_indicabili:
                        altro_giocatore = input(f"{self.ruolo}: ")
                        if altro_giocatore:
                            altro_giocatore = int(altro_giocatore)
                            if altro_giocatore in giocatori_indicabili:
                                indicato = next((x for x in villaggio.abitanti if x.ID == altro_giocatore), None)
                                indicato.contagiato = True
                                break
                            else:
                                print("Giocatore indicato non valido")
                        else:
                            print("L'untore deve indicare un giocatore da contagiare:")
                    else:
                        input(f"{self.ruolo}: ---- (Non ci sono più giocatori da contagiare)")
                        break
        else:
            input(f"{self.ruolo}: ---- (MORTO)")

    def morte(self, villaggio):
        check = set(self.assassini) & set(self.indicato_da)
        if ('Lupo' in check or 'Ammaestratore' in check) and 'Cavaliere' in self.indicato_da:
            return False
        elif check:
            self.status = 'Morto'
            return True
        else:
            return False
    
    def vittoria(self, villaggio):
        pass