from IndovinaLaParola import IndovinaLaParola

def main():
    miglior_risultato = None  # Struttura per salvare la parola e i tentativi minimi
    print("Benvenuto a 'Indovina la Parola'!")

    while True:
        print("\nMenu:")
        print("1. Gioca")
        print("2. Mostra miglior risultato")
        print("3. Esci")
        scelta = input("Inserisci la tua scelta: ")

        if scelta == "1":
            # Esegui il gioco e ottieni il risultato
            risultato = IndovinaLaParola()
            parola, tentativi = risultato  # Risultato dovrebbe restituire (parola, tentativi)
            # Aggiorna il miglior risultato se necessario
            if tentativi != 0:
                if miglior_risultato is None or tentativi < miglior_risultato['tentativi']:
                    miglior_risultato = {"parola": parola, "tentativi": tentativi}
                    print(f"Complimenti! Nuovo miglior risultato: {parola} indovinata con ancora {tentativi} tentativi!")
        elif scelta == "2":
            if miglior_risultato:
                print(f"Miglior risultato: {miglior_risultato['parola']} indovinata con ancora {miglior_risultato['tentativi']} tentativi.")
            else:
                print("Nessun risultato registrato finora.")
        elif scelta == "3":
            print("Grazie per aver giocato! Alla prossima!")
            break
        else:
            print("Scelta non valida. Riprova.")

if __name__ == "__main__":
    main()
