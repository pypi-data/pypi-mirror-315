import secrets

def IndovinaLaParola():
    # Lista di parole da indovinare
    parole = ["python", "computer", "gioco", "programmazione", "matematica",
              "informatica", "programmatore", "banana", "università", "malphite",
              "roccia", "coperta"]
    parola_segreta = secrets.choice(parole)
    lettere_indovinate = ["_"] * len(parola_segreta)  # Sostituisce "" con "_"
    tentativi = 6

    print("Benvenuto al gioco 'Indovina la parola'!")
    print("La parola segreta è: ", " ".join(lettere_indovinate))

    while tentativi > 0 and "_" in lettere_indovinate:  # Controlla "_"
        lettera = input("Inserisci una lettera: ").lower()

        if len(lettera) != 1 or not lettera.isalpha():
            print("Per favore, inserisci una sola lettera valida!")
            continue

        if lettera in parola_segreta:
            print(f"Bravo! La lettera '{lettera}' è nella parola.")
            for i, carattere in enumerate(parola_segreta):
                if carattere == lettera:
                    lettere_indovinate[i] = lettera  # Aggiorna la lettera indovinata
        else:
            tentativi -= 1
            print(f"Sbagliato! Ti restano {tentativi} tentativi.")

        print("Parola attuale:", " ".join(lettere_indovinate))

    if "_" not in lettere_indovinate:  # Se non ci sono più "_"
        print(f"Complimenti! Hai indovinato la parola: {parola_segreta}")
    else:
        print(f"Peccato! Hai finito i tentativi. La parola era: {parola_segreta}")

    # Restituisce la parola e il numero di tentativi usati
    return parola_segreta, 6 - tentativi