from getpass import getpass
from database_funksjoner import hente_ut_ansatte

def hvem_er_du():
    bruker = str(input("Hva er brukernavnet ditt? "))
    if bruker == "admin": # brukeren må bevise at hen har admin rettigheter 
        passord = getpass("Passordet ditt er? ") # Her har vi en liten fordel :)
        if not passord == "Pass1234":
            print("Bare ett forsøk! ;)")
            bruker = -1
    else:
        # Hvis brukeren ikke er admin, må brukeren tilhøre tabellen «ansatte»
        ansatte = hente_ut_ansatte()
        if not bruker in ansatte:
            print(bruker, "er ikke i tabellen ansatte. Ha det! :)")
            bruker = -1 
    return bruker # Hvis bruker er lik -1 skal hovedsløyfen avslutte programmet

def meny():
    print("------------------------------")
    print("1. Legge til data i en tabell")
    print("2. Hente ut data fra en tabell")
    print("3. Vis laptopen til en vis bruker") # kan denne setningen forbedres?
    print("4. Oppdatere en tabell")    
    print("5. Slette data fra en tabell")
    print("6. Slutt programmet")
    print("------------------------------")
    tall = int(input("Valget ditt er: "))
    return tall
