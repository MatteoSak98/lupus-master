# Introduzione
`lupus-master` è un software di supporto per giocare a *Lupus in Tabula*.

Tiene traccia di tutto quello che succede e aiuta il master a dirigere la partita.
Sono implementate tutte le regole del gioco, le condizioni di vittoria, le caratteristiche dei diversi ruoli e le loro interazioni.

I ruoli implementati nella versione 1.0 sono:
- Buoni
  - Contadino
  - Veggente
  - Cavaliere
  - Giustiziere
  - Ammaestratore
  - Mitomane
  - Medium
  - Beccamorto
- Cattivi
  - Lupo
  - Indemoniato
  - Insinuo
  - Illusionista
  - Boia
  - Strega
- Rubavittoria
  - Matto
  - Wendigo
  - Untore

## Installazione
1. Verificare che sia installato python3
2. da terminale digitare `git clone https://github.com/ncldlbn/lupus-master.git`
3. da terminale digitare `pip install requirements.txt`

## Uso
1. Compilare il file `setup.yml` con i ruoli e i nomi dei giocatori che partecipano. 
Il numero di ruoli deve coincidere con il numero dei giocatori.
2. Avviare il software con il comando `python lupus-master.py` e seguire le istruzioni da terminale.