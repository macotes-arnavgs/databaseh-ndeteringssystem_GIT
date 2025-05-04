import mysql.connector
def initialisere_database():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Pass1234",
        database = "CyFskole"
    )
    mycursor = mydb.cursor()
    return (mydb, mycursor)             # funksjonen returnerer én tuppel med to objekt

def hente_ut_ansatte():                                 # returnerer en liste over ansatte
    mydb, mycursor = initialisere_database()
    
    mycursor.execute("SELECT brukernavn FROM ansatte") 

    list_av_tupler = mycursor.fetchall()

    liste = []
    for felt in list_av_tupler:
        liste.append(felt[0])
    print("Datatypen av liste er", type(liste))
    return liste                                         # vi returnerer en liste over ansatte

def hent_ut_data(brukernavn): # Også i filen «database_funksjoner.py»
    mydb, mycursor = initialisere_database()
    print("Her har du en liste over tabellene i denne databasen")
    mycursor.execute("show tables")

    myresult = mycursor.fetchall()
    for rad in myresult:
        print(rad[0]) # vi viser alle tabellene i databasen

    tabell = input("Hvilken tabell vil du hente ut dataene fra? ")

    # Her må vi sjekke at brukeren har rettigheter til å hente data ...    
    if brukernavn == "admin":
        mycursor.execute("SELECT * FROM " + tabell)
        # Dette er ikke komplett. Jeg burde lage en spørring som kobler flere tabeller
    else:
        mycursor.execute("SELECT brukernavn FROM " + tabell) # samme som før

    myresult = mycursor.fetchall()
    for rad in myresult:
        print(rad) # dette kan forbedres

def hent_laptoper_etter_bruker(): # Her viser vi laptoper etter bruker
    mydb, mycursor = initialisere_database()
    print("Her har du en liste over tabellene i denne databasen")
    mycursor.execute("show tables")
    
    myresult = mycursor.fetchall()
    for rad in myresult:
        print(rad[0]) # vi viser alle tabellene i databasen

    tabell = input("Hvilken tabell vil du hente ut informasjon fra? ")
    mycursor.execute("select * from " + tabell)
    
    myresult = mycursor.fetchall()
    for rad in myresult:
        print(rad) # vi viser alle tabellene i databasen

    idbruker = input("ID-en til brukeren du vil hente ut informasjon om laptopene? ")
    if tabell == "ansatte":
        mycursor.execute("SELECT laptoper.modell, laptoper.alder, laptoper.pris FROM laptoper, bruker_og_laptoper \
                         where bruker_og_laptoper.ansatte_idAnsatte = " + idbruker + \
                            " and laptoper.idlaptoper = bruker_og_laptoper.laptoper_idlaptoper;")
    elif tabell == "ledere":
        mycursor.execute("SELECT laptoper.modell, laptoper.alder, laptoper.pris FROM laptoper, bruker_og_laptoper \
                         where bruker_og_laptoper.ledere_idLedere = " + idbruker + \
                            " and laptoper.idlaptoper = bruker_og_laptoper.laptoper_idlaptoper;")
    # tabellen gjester kan også implementeres
    myresult = mycursor.fetchall()
    for rad in myresult:
        print(rad) # vi viser alle tabellene i databasen
    return 0

def legg_til_data(): # her burde vi gjøre noe om brukeren er admin eller ...
    mydb, mycursor = initialisere_database()
    mycursor.execute("show tables")

    print("Her må vi vise listen over tabellene i databasen ...")
    myresult = mycursor.fetchall()
    for rad in myresult:
        print(rad[0]) # vi viser alle tabellene i databasen

    tabell = str(input("Hvilken tabell vil du lagre informasjon i (hele navn)? "))
    if tabell == "laptoper":
        legg_til_ny_laptop(mydb, mycursor)
    else: #vi antar at de andre tabellene har samme struktur (felt og datatyper)
        legg_til_ny_bruker(mydb, mycursor, tabell)

def legg_til_ny_laptop(mydb, mycursor):
    laptop = {}
    laptop['id'] = str(input("Hva er ID-en til datamaskinen du vil lagre? "))
    laptop['alder'] = str(input("Hva er alderen til datamaskinen du vil lagre? "))
    laptop['modell'] = str(input("Hva er modellen til datamaskinen du vil lagre? "))
    laptop['pris'] = str(input("Hva er prisen på datamaskinen du vil lagre? "))

    sql = "INSERT INTO laptoper(idLaptoper, Modell, Alder, Pris) VALUES (%s,%s,%s,%s)"
    val = (laptop['id'], laptop['modell'], laptop['alder'], laptop['pris'])
    mycursor.execute(sql, val)

    mydb.commit()
    return 0

def legg_til_ny_bruker(mydb, mycursor, tabell):
    nybruker = {}
    nybruker['id'] = str(input("Hva er id-en til brukeren du vil lagre? "))
    nybruker['fornavn'] = str(input("Hva er fornavnet til brukeren du vil lagre? "))
    nybruker['etternavn'] = str(input("Hva er etternavnet til brukeren? "))
    nybruker['telefonnummer'] = str(input("Hva er telefonnummeret til brukeren? "))
    # vi lager brukernavnet fra fornavn og etternavn
    nybruker['brukernavn'] = nybruker['fornavn'][:2] + nybruker['etternavn'][:2] 
    id = 'id' + tabell # vi bygger id-en fra tabellens navn

    sql = "INSERT INTO " +  tabell + "(" + id + ", navn, telefonnummer, brukernavn) VALUES (%s,%s,%s,%s)" 
    val = (nybruker['id'], nybruker['fornavn'] + " " + nybruker['etternavn'], nybruker['telefonnummer'], nybruker['brukernavn'])
    mycursor.execute(sql, val)
    
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    return 0 # dette betyr vanligvis "alt i orden"
    
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    return 0 # dette betyr vanligvis "alt i orden"

def oppdatere_data(): # her burde vi gjøre noe om brukeren er admin eller ...
    mydb, mycursor = initialisere_database()
    mycursor.execute("show tables")

    print("Her må vi vise listen over tabellene i databasen ...")
    myresult = mycursor.fetchall()
    for rad in myresult:
        print(rad[0]) # vi viser alle tabellene i databasen

    tabell = str(input("Hvilken tabell vil du oppdatere informasjon i (hele navn)? "))
    if tabell == "laptoper":
        oppdatere_laptop(mydb, mycursor)
    else: #vi antar at de andre tabellene har samme struktur (felt og datatyper)
        oppdatere_ansatte(mydb, mycursor, tabell)

def oppdatere_laptop(mydb, mycursor):
    laptop = {}
    laptop['id'] = str(input("Hva er ID-en til datamaskinen du vil oppdatere? "))
    laptop['alder'] = str(input("Hva er den nye alderen til datamaskinen du vil oppdatere? "))
    laptop['modell'] = str(input("Hva er den nye modellen til datamaskinen du vil oppdatere? "))
    laptop['pris'] = str(input("Hva er den nye prisen på datamaskinen du vil oppdatere? "))

    sql = "UPDATE laptoper SET alder = %s, modell = %s, pris = %s WHERE idlaptoper = %s" 
    val = (laptop['alder'], laptop['modell'], laptop['pris'], laptop['id'])
    mycursor.execute(sql, val)
    
    mydb.commit()
    print(mycursor.rowcount, "record updated.")
    return 0 # dette betyr vanligvis "alt i orden"

def oppdatere_ansatte(mydb, mycursor, tabell):
    nybruker = {}
    nybruker['id'] = str(input("Hva er id-en til brukeren du vil oppdatere? "))
    nybruker['fornavn'] = str(input("Hva er det nye fornavnet til brukeren du vil oppdatere? "))
    nybruker['etternavn'] = str(input("Hva er det nye etternavnet til brukeren? "))
    nybruker['telefonnummer'] = str(input("Hva er det nye telefonnummeret til brukeren? "))
    # vi lager brukernavnet fra fornavn og etternavn
    nybruker['brukernavn'] = nybruker['fornavn'][:2] + nybruker['etternavn'][:2] 
    id = 'id' + tabell # vi bygger id-en fra tabellens navn

    sql = "UPDATE " +  tabell + " SET navn = %s, telefonnummer = %s, brukernavn = %s WHERE " + id + " = %s" 
    val = (nybruker['fornavn'] + " " + nybruker['etternavn'], nybruker['telefonnummer'], nybruker['brukernavn'], nybruker['id'])
    mycursor.execute(sql, val)
    
    mydb.commit()
    print(mycursor.rowcount, "record updated.")
    return 0 # dette betyr vanligvis "alt i orden"

def slette_data(): # her burde vi gjøre noe om brukeren er admin eller ...
    mydb, mycursor = initialisere_database()
    mycursor.execute("show tables")

    print("Her må vi vise listen over tabellene i databasen ...")
    myresult = mycursor.fetchall()
    for rad in myresult:
        print(rad[0]) # vi viser alle tabellene i databasen

    tabell = str(input("Hvilken tabell vil du slette informasjon fra (hele navn)? "))
    if tabell == "laptoper":
        slette_laptop(mydb, mycursor)
    elif tabell == "ansatte": #vi antar at de andre tabellene har samme struktur (felt og datatyper)
        slette_ansatte(mydb, mycursor)
    else: # vi burde fortsette her med de andre tabellene
        pass

def slette_laptop(mydb, mycursor):
    laptop = {}
    laptop['id'] = str(input("Hva er ID-en til datamaskinen du vil slette? "))

    sql = "DELETE FROM laptoper WHERE idlaptoper = %s" 
    val = (laptop['id'],)
    mycursor.execute(sql, val)
    
    mydb.commit()
    print(mycursor.rowcount, "record deleted.")
    return 0 # dette betyr vanligvis "alt i orden"

def slette_ansatte(mydb, mycursor):
    nybruker = {}
    nybruker['id'] = str(input("Hva er id-en til brukeren du vil slette? "))

    sql = "DELETE FROM ansatte WHERE idAnsatte = %s" 
    val = (nybruker['id'],)
    mycursor.execute(sql, val)
    
    mydb.commit()
    print(mycursor.rowcount, "record deleted.")
    return 0 # dette betyr vanligvis "alt i orden"
