import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Animali"
)
mycursor = mydb.cursor()


def inserisci_animale():
    try:
        id = int(input("Inserisci ID: "))
        nome_proprio = input("Inserisci il nome proprio: ")
        razza = input("Inserisci la razza: ")
        peso = int(input("Inserisci il peso (in kg): "))
        eta = int(input("Inserisci l'età: "))
        
        sql = "INSERT INTO Mammiferi (id, Nome_Proprio, Razza, Peso, Eta) VALUES (%s, %s, %s, %s, %s)"
        val = (id, nome_proprio, razza, peso, eta)
        
        mycursor.execute(sql, val)
        mydb.commit()
        print(f"{mycursor.rowcount} animale inserito con successo.")
    except ValueError:
        print("Errore: Inserire valori interi validi per ID, Peso ed Età.")


def visualizza_animali():
    mycursor.execute("SELECT * FROM Mammiferi")
    result = mycursor.fetchall()
    for animale in result:
        print(animale)

def visualizza_animali_grandi():
    mycursor.execute("SELECT * FROM Mammiferi WHERE Peso > 2")
    result = mycursor.fetchall()
    for animale in result:
        print(animale)

def elimina_animale():
    id = int(input("Inserisci l'ID dell'animale da eliminare: "))
    sql = "DELETE FROM Mammiferi WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()
    print(f"Animale con ID {id} eliminato con successo.")


def modifica_animale():
    id = int(input("Inserisci l'ID dell'animale da modificare: "))
    nome_proprio = input("Inserisci il nuovo nome proprio: ")
    razza = input("Inserisci la nuova razza: ")
    peso = int(input("Inserisci il nuovo peso (in kg): "))
    eta = int(input("Inserisci la nuova età: "))

    sql = "UPDATE Mammiferi SET Nome_Proprio = %s, Razza = %s, Peso = %s, Eta = %s WHERE id = %s"
    val = (nome_proprio, razza, peso, eta, id)
    mycursor.execute(sql, val)
    mydb.commit()
    print(f"Animale con ID {id} modificato con successo.")


def menu():
    while True:
        print("\nMenu:")
        print("1 - Inserisci un nuovo animale")
        print("2 - Visualizza tutti gli animali")
        print("3 - Elimina un animale")
        print("4 - Modifica un animale")
        print("5 - Visualizza animali che pesano più di 2 kg")
        print("0 - Esci")

        scelta = input("Seleziona un'opzione: ")

        if scelta == '1':
            n = int(input("Quanti animali vuoi inserire? "))
            for _ in range(n):
                inserisci_animale()
                if input("Vuoi continuare ad aggiungere animali? (s/n): ").lower() != 's':
                    break
        elif scelta == '2':
            visualizza_animali()
        elif scelta == '3':
            elimina_animale()
        elif scelta == '4':
            modifica_animale()
        elif scelta == '5':
            visualizza_animali_grandi()
        elif scelta == '0':
            print("Uscita dal programma.")
            break
        else:
            print("Opzione non valida, riprova.")


menu()


mycursor.close()
mydb.close()
