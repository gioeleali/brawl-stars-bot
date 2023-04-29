import requests
#import webcolors

API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjM0YmYwMDNkLTQ2OGYtNDg3Yi1hM2ZiLWNlNmYwMWM4ZTU0OSIsImlhdCI6MTY3OTkzODYxNSwic3ViIjoiZGV2ZWxvcGVyLzQ5NTg3ZjliLTMwYjMtOTNhYy03MDc1LTM0NDY2OWYyYzFmMiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNzkuNTIuMjAzLjE0OSJdLCJ0eXBlIjoiY2xpZW50In1dfQ._ZkCDg6uFZv1NElW82Qkm_i4A5skhyEn8rXAff5AosIMxr5MeqzozM1h9HtQVJ9d5g56rnzu3Pf72wUdly0tqQ"
URL = "https://api.brawlstars.com/v1/"
#URL2 = "https://api.brawlapi.com/v1/"
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}

def main():
    scelta = 1
    while(scelta!=0):
        scelta = menu()
        match scelta:
            case 0:
                quit()
            case 1:
                player()
            case 2:
                brawlers_player()
            case 3:
                brawlers()
            case 4:
                club()
            case 5:
                club_members()
            case 6:
                battle_log()
            case 7:
                ranking_players()
            case 8:
                ranking_clubs()
            case 9:
                ranking_brawlers()
            case 10:
                events()
            case 11:
                test()
            case other:
                print("Inserisci un valore valido!")

def menu():
    print("-"*20)
    print("MENU'")
    print("1. Cerca un giocatore")
    print("2. Mostra brawlers di un giocatore")
    print("3. Mostra tutti i brawler")
    print("4. Cerca un club")
    print("5. Mostra membri di un club")
    print("6. Registro battaglie")
    print("7. Mostra classifica giocatori")
    print("8. Mostra classifica club")
    print("9. Mostra classifica brawler")
    print("10. Eventi attuali")
    print("11. Stampa json")
    print("Premi 0 per uscire")
    scelta = int(input("Che azione vuoi fare? (1-11): "))
    print("-"*20)
    return scelta

def player():
    tag = "%23" + input("Inserisci il tag del giocatore da cercare: ").upper().replace("#", "")
    response = requests.get(url=URL + "players/" + tag, headers=headers)
    if(response):
        data = response.json()
        #hex = data['nameColor'][4:]
        #colore = webcolors.hex_to_name("#" + hex, spec='css3')
        if(data['isQualifiedFromChampionshipChallenge']==True):
            esito = "Sì"
        elif(data['isQualifiedFromChampionshipChallenge']==False):
            esito = "No"
        print(f"Nome: {data['name']}")
        #print(f"Colore nome: {colore}")
        print(f"Tag: {data['tag']}")
        print(f"Trofei attuali: {data['trophies']}")
        print(f"Record trofei: {data['highestTrophies']}")
        print(f"Livello: {data['expLevel']}")
        print(f"Vittorie 3v3: {data['3vs3Victories']}")
        print(f"Vittore in solo: {data['soloVictories']}")
        print(f"Vittorie in duo: {data['duoVictories']}")
        print(f"Punti esperienza: {data['expPoints']}")
        print(f"Qualificato per la Brawl Stars Championship? {esito}")
        if('club' in data):
            print(f"Club: {data['club']['name']}")
    else:
        print(f"Errore {response.status_code}: {response.reason}")

def brawlers_player():
    tag = "%23" + input("Inserisci il tag del giocatore di cui mostrare i brawler: ").upper().replace("#", "")
    response = requests.get(url=URL + "players/" + tag, headers=headers)
    print("-"*10)
    if(response):
        data = response.json()
        for brawler in data['brawlers']:
            print(f"Brawler: {brawler['name']}")
            print(f"Trofei attuali: {brawler['trophies']}")
            print(f"Record di trofei: {brawler['highestTrophies']}")
            print(f"Livello: {brawler['power']}")
            print(f"Rank: {brawler['rank']}")
            print("-"*10)
    else:
        print(f"Errore {response.status_code}: {response.reason}")

def brawlers():
    response = requests.get(url=URL + "brawlers", headers=headers)
    if(response):
        data = response.json()
        for brawler in data['items']:
            print(brawler['name'])
            print("Abilità stellare:")
            for i in brawler['starPowers']:
                print(i['name'])
            print("Gadget:")
            for i in brawler['gadgets']:
                print(i['name'])
            print("-"*10)
    else:
        print(f"Errore {response.status_code}: {response.reason}")

def club():
    tag = "%23" + input("Inserisci il tag del club da cercare: ").upper().replace("#", "")
    response = requests.get(url=URL + "clubs/" + tag, headers=headers)
    if(response):
        data = response.json()
        print(f"Nome: {data['name']}")
        print(f"Tag: {data['tag']}")
        print(f"Descrizione: {data['description']}")
        if(data['type']=="open"):
            tipo = "Aperto"
        elif(data['type']=="closed"):
            tipo = "Privato"
        elif(data['type']=="inviteOnly"):
            tipo = "Su invito"
        print(f"Tipologia: {tipo}")
        print(f"Trofei: {data['trophies']}")
        print(f"Trofei richiesti per entrare: {data['requiredTrophies']}")
    else:
        print(f"Errore {response.status_code}: {response.reason}")

def club_members():
    tag = "%23" + input("Inserisci il tag del club di cui mostrare i membri: ").upper().replace("#", "")
    response = requests.get(url=URL + "clubs/" + tag, headers=headers)
    print("-"*10)
    if(response):
        data = response.json()
        print("Membri del Club:")
        for member in data['members']:
                print(f"Nome: {member['name']}")
                print(f"Trofei: {member['trophies']}")
                print(f"Tag: {member['tag']}")
                if(member['role']=="president"):
                    ruolo = "Presidente"
                elif(member['role']=="vicePresident"):
                    ruolo = "Vicepresidente"
                elif(member['role']=="senior"):
                    ruolo = "Anziano"
                elif(member['role']=="member"):
                    ruolo = "Membro"
                print(f"Ruolo: {ruolo}")
                print("-"*10)
    else:
        print(f"Errore {response.status_code}: {response.reason}")

def battle_log():
    tag = "%23" + input("Inserisci il tag del giocatore di cui mostrare il registro battaglie: ").upper().replace("#", "")
    response = requests.get(url=URL + "players/" + tag + "/battlelog", headers=headers)
    print("-"*10)
    if(response):
        data = response.json()
        for battle in data['items']:
            if('battle' in battle and 'mode' in battle['battle']):
                if(battle['battle']['mode']=="duoShowdown" or battle['battle']['mode']=="soloShowdown"):
                    print(f"POSIZIONE: {battle['battle']['rank']}")
            if('result' in battle['battle']):
                if(battle['battle']['result']=="victory"):
                    print("VITTORIA")
                elif(battle['battle']['result']=="defeat"):
                    print("SCONFITTA")
            print(f"Modalità: {battle['battle']['mode']}")
            if('map' in battle['event']):
                print(f"Mappa: {battle['event']['map']}")
            if('trophyChange' in battle['battle']):
                print(f"Cambiamento trofei: {battle['battle']['trophyChange']}")
            else:
                print("Nessun cambiamento di trofei")
            print("-"*10)
    else:
        print(f"Errore {response.status_code}: {response.reason}")

def ranking_players():
    tag = input("Inserisci il paese (due lettere) di cui vedere la classifica dei giocatori. Per la classifica globale inserire 'global': ").upper()
    response = requests.get(url=URL + "rankings/" + tag + "/players", headers=headers)
    print("-"*10)
    if(response):
        data = response.json()
        print(f"Classifica {tag}:")
        for ranked in data['items']:
            print(f"{ranked['rank']}.")
            print(f"Nome: {ranked['name']}")
            print(f"Tag: {ranked['tag']}")
            print(f"Trofei: {ranked['trophies']}")
            if('club' in ranked):
                print(f"Club: {ranked['club']['name']}")
            else:
                print("In nessun club")
            print("-"*10)
    else:
        print(f"Errore {response.status_code}: {response.reason}")

def ranking_clubs():
    tag = input("Inserisci il paese (due lettere) di cui vedere la classifica dei club. Per la classifica globale inserire 'global': ").upper()
    response = requests.get(url=URL + "rankings/" + tag + "/clubs", headers=headers)
    print("-"*10)
    if(response):
        data = response.json()
        print(f"Classifica {tag}:")
        for ranked in data['items']:
            print(f"{ranked['rank']}.")
            print(f"Nome: {ranked['name']}")
            print(f"Tag: {ranked['tag']}")
            print(f"Trofei: {ranked['trophies']}")
            print(f"Membri: {ranked['memberCount']}")
            print("-"*10)
    else:
        print(f"Errore {response.status_code}: {response.reason}")

def ranking_brawlers():
    tag = input("Inserisci il paese (due lettere) di cui vedere la classifica dei brawler. Per la classifica globale inserire 'global': ").upper()
    brawler = str(input(f"Inserisci il nome del brawler di cui vedere la classifica {tag} (in inglese): ").upper())
    br = requests.get(url=URL + "brawlers", headers=headers)
    if(br):
        data = br.json()
        for ranked in data['items']:
            if(brawler==ranked['name']):
                brawler_id = ranked['id']
    response = requests.get(url=URL + "rankings/" + tag + "/brawlers/" + str(brawler_id), headers=headers)
    print("-"*10)
    if(response):
        data = response.json()
        print(f"Classifica {brawler}:")
        for ranked in data['items']:
            print(f"{ranked['rank']}.")
            print(f"Nome: {ranked['name']}")
            print(f"Tag: {ranked['tag']}")
            print(f"Trofei: {ranked['trophies']}")
            if('club' in ranked):
                print(f"Club: {ranked['club']['name']}")
            else:
                print("In nessun club")
            print("-"*10)
    else:
        print(f"Errore {response.status_code}: {response.reason}")

def events():
    response = requests.get(url=URL + "events/rotation", headers=headers)
    if(response):
        data = response.json()
        for event in data:
            if(event['event']['mode']=="gemGrab"):
                mode = "Arraffagemme"
            elif(event['event']['mode']=="soloShowdown"):
                mode = "Sopravvivenza Solo"
            elif(event['event']['mode']=="duoShowdown"):
                mode = "Sopravvivenza Duo"
            elif(event['event']['mode']=="brawlBall"):
                mode = "Footbrawl"
            elif(event['event']['mode']=="hotZone"):
                mode = "Dominio"
            elif(event['event']['mode']=="knockout"):
                mode = "K.O."
            elif(event['event']['mode']=="bigGame"):
                mode = "Pezzo Grosso"
            elif(event['event']['mode']=="heist"):
                mode = "Rapina"
            elif(event['event']['mode']=="bounty"):
                mode = "Ricercati"
            elif(event['event']['mode']=="basketBrawl"):
                mode = "Basket Brawl"
            print(f"{mode}: {event['event']['map']}")
    else:
        print(f"Errore {response.status_code}: {response.reason}")

def test():
    tag = "%23" + input("TAG: ").upper().replace("#", "")
    response = requests.get(url=URL + "players/" + tag, headers=headers)
    data = response.json()
    print(data)

if __name__ == "__main__":
    main()