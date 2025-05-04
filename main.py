from tillegg_funksjoner import hvem_er_du, meny
from database_funksjoner import legg_til_data, hent_ut_data, hent_laptoper_etter_bruker, oppdatere_data, slette_data

if __name__ == "__main__": # Dette lagres i filen dbhs.py
    brukernavn = hvem_er_du() # bruker skal være enten admin eller en ansatte
    if brukernavn == -1:
        exit()
    else:
        print("Velkommen", brukernavn,"!")

    while True:
        valg = meny()
        if valg == 1:
            print("Du valgte å legge til data")
            legg_til_data()
        elif valg == 2: 
            print("Du valgte å hente ut data")
            hent_ut_data(brukernavn) # fordi brukere har begrenset tilgang
        elif valg == 3:
            print("Du valgte å vise laptoper per bruker")
            hent_laptoper_etter_bruker() 
        elif valg == 4:
            print("Du valgte å oppdatere en tabell")
            oppdatere_data()
        elif valg == 5:
            print("Du valgte å slette data.")
            slette_data()
        elif valg == 6:
            print("Du valgte å avslutte programmet.")
            exit()            
        else:
            print("Valget ditt er ikke gyldig, prøv igjen.")

