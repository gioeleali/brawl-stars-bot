import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext, filters

API_KEY = "YOUR API KEY CODE"
TOKEN = "YOUR TOKEN"
URL = "https://api.brawlstars.com/v1/"
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

player_id = ""

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton(text="Tutti i comandi🛠", callback_data="command")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Ciao *{update.effective_user.first_name}*,\nquesto bot ha il compito di fornirti diverse informazioni sul gioco '*Brawl Stars*', utilizzando le sue [API ufficiali](https://developer.brawlstars.com/#/) comodamente da *Telegram* così che tu possa consultare le statistiche con _più rapidità ed efficienza_.\n\nPer vedere tutta la lista di comandi clicca sul bottone sottostante.🤝", parse_mode='Markdown', disable_web_page_preview = True, reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    if query.data == "command":
        keyboard = [
            [
                InlineKeyboardButton(text="Giocatore👤", callback_data="player"),
                InlineKeyboardButton(text="Club👥", callback_data="club")
            ],
            [
                InlineKeyboardButton(text="Classifica🏆", callback_data="ranked"),
                InlineKeyboardButton(text="Generali📊", callback_data="generic")
            ],
            [
                InlineKeyboardButton(text="◀️", callback_data="backback")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Di seguito una _lista di tutti i comandi_ disponibili, sono divisi per categorie, premi sulla categoria di comandi che desideri utilizzare.\n\nSe vuoi suggerire qualche comando che pensi possa essere utile [scrivimi in privato](https://t.me/gioeleali)!", parse_mode='Markdown', disable_web_page_preview = True, reply_markup=reply_markup)
    elif query.data == "player":
        keyboard = [
            [
                InlineKeyboardButton(text="Profilo👤", callback_data="1"),
                InlineKeyboardButton(text="Brawler🦿", callback_data="2")
            ],
            [
                InlineKeyboardButton(text="Registro Battaglie⚔️", callback_data="3")
            ],
            [
                InlineKeyboardButton(text="◀️", callback_data="back")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="*Comandi per 'Giocatore'*\n\n- *Profilo👤*: statistiche generali sul profilo del giocatore\n- *Brawler🦿*: statistiche generali sui brawler del giocatore\n- *Registro Battaglie⚔️*: registro battaglie del giocatore", parse_mode='Markdown', reply_markup=reply_markup)
    elif query.data == "club":
        keyboard = [
            [
                InlineKeyboardButton(text="Profilo Club🛡", callback_data="4"),
                InlineKeyboardButton(text="Membri👥", callback_data="5")
            ],
            [
                InlineKeyboardButton(text="◀️", callback_data="back")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="*Comandi per 'Club'*\n\n- *Profilo Club🛡*: statistiche generali sul profilo del club\n- *Membri👥*: statistiche generali sui membri del club", parse_mode='Markdown', reply_markup=reply_markup)
    elif query.data == "ranked":
        keyboard = [
            [
                InlineKeyboardButton(text="Giocatori👤", callback_data="6"),
                InlineKeyboardButton(text="Club👥", callback_data="7"),
            ],
            [
                InlineKeyboardButton(text="Brawler🦿", callback_data="8")
            ],
            [
                InlineKeyboardButton(text="◀️", callback_data="back")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="*Comandi per 'Ranked'*\n\n- *Giocatori👤*: classifica dei giocatori\n- *Club👥*: classifica dei club\n- *Brawler🦿*: classifica per brawler", parse_mode='Markdown', reply_markup=reply_markup)
    elif query.data == "generic":
        keyboard = [
            [
                InlineKeyboardButton(text="Tutti i Brawler🦿", callback_data="9")
            ],
            [
                InlineKeyboardButton(text="Eventi Attuali🕹", callback_data="10")
            ],
            [
                InlineKeyboardButton(text="◀️", callback_data="back")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="*Comandi per 'Generali'*\n\n- *Tutti i Brawler🦿*: una lista di tutti i brawler attualmente disponibili in gioco\n- *Eventi Attuali🕹*: una lista di tutti gli eventi attualmente disponibili", parse_mode='Markdown', reply_markup=reply_markup)
    elif query.data == "1":
        keyboard = [
            [
                InlineKeyboardButton(text="◀️", callback_data="back")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("Inserisci il *TAG* giocatore:", parse_mode='Markdown', reply_markup=reply_markup)
        await player(update, context)
    elif query.data == "2":
        keyboard = [
            [
                InlineKeyboardButton(text="◀️", callback_data="back")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("Inserisci il *TAG* giocatore:", parse_mode='Markdown', reply_markup=reply_markup)
        await brawlers_player(update, context)
    elif query.data == "3":
        await brawlers(update, context)
    elif query.data == "4":
        keyboard = [
            [
                InlineKeyboardButton(text="◀️", callback_data="back")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("Inserisci il *TAG* del club:", parse_mode='Markdown', reply_markup=reply_markup)
        await club(update, context)
    elif query.data == "5":
        keyboard = [
            [
                InlineKeyboardButton(text="◀️", callback_data="back")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("Inserisci il *TAG* giocatore:", parse_mode='Markdown', reply_markup=reply_markup)
        await club_members(update, context)
    elif query.data == "6":
        keyboard = [
            [
                InlineKeyboardButton(text="◀️", callback_data="back")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("Inserisci il *TAG* giocatore:", parse_mode='Markdown', reply_markup=reply_markup)
        await battle_log(update, context)
    elif query.data == "7":
        keyboard = [
            [
                InlineKeyboardButton(text="◀️", callback_data="back")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("Inserisci il *TAG* giocatore:", parse_mode='Markdown', reply_markup=reply_markup)
        await ranking_players(update, context)
    elif query.data == "8":
        keyboard = [
            [
                InlineKeyboardButton(text="◀️", callback_data="back")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("Inserisci il *TAG* giocatore:", parse_mode='Markdown', reply_markup=reply_markup)
        await ranking_clubs(update, context)
    elif query.data == "9":
        keyboard = [
            [
                InlineKeyboardButton(text="◀️", callback_data="back")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("Inserisci il *TAG* giocatore:", parse_mode='Markdown', reply_markup=reply_markup)
        await ranking_brawlers(update, context)
    elif query.data == "10":
        await events(update, context)
    elif query.data == "back":
        keyboard = [
            [
                InlineKeyboardButton(text="Giocatore👤", callback_data="player"),
                InlineKeyboardButton(text="Club👥", callback_data="club")
            ],
            [
                InlineKeyboardButton(text="Classifica🏆", callback_data="ranked"),
                InlineKeyboardButton(text="Generali📊", callback_data="generic")
            ],
            [
                InlineKeyboardButton(text="◀️", callback_data="backback")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Di seguito una _lista di tutti i comandi_ disponibili, sono divisi per categorie, premi sulla categoria di comandi che desideri utilizzare.\n\nSe vuoi suggerire qualche comando che pensi possa essere utile [scrivimi in privato](https://t.me/gioeleali)!", parse_mode='Markdown', disable_web_page_preview = True, reply_markup=reply_markup)
    elif query.data == "backback":
        keyboard = [
            [
                InlineKeyboardButton(text="Tutti i comandi🛠", callback_data="command")
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Ciao *{update.effective_user.first_name}*,\nquesto bot ha il compito di fornirti diverse informazioni sul gioco '*Brawl Stars*', utilizzando le sue [API ufficiali](https://developer.brawlstars.com/#/) comodamente da *Telegram* così che tu possa consultare le statistiche con _più rapidità ed efficienza_.\n\nPer vedere tutta la lista di comandi clicca sul bottone sottostante.🤝", parse_mode='Markdown', disable_web_page_preview = True, reply_markup=reply_markup)

async def player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tag = "%23" + update.message.text.upper().replace("#", "")
    response = requests.get(url=URL + "players/" + tag, headers=headers)
    if(response):
        data = response.json()
        if(data['isQualifiedFromChampionshipChallenge']==True):
            esito = "Sì"
        elif(data['isQualifiedFromChampionshipChallenge']==False):
            esito = "No"
        if('club' in data):
            message = f"Nome: *{data['name']}*\nTag: {data['tag']}\nTrofei attuali: *{data['trophies']}*\nRecord trofei: *{data['highestTrophies']}*\nLivello: *{data['expLevel']}*\nVittorie 3v3: *{data['3vs3Victories']}*\nVittore in solo: *{data['soloVictories']}*\nVittorie in duo: *{data['duoVictories']}*\nPunti esperienza: *{data['expPoints']}*\nQualificato per la Brawl Stars Championship? *{esito}*\nClub: *{data['club']['name']}*"
        else:
            message = f"Nome: *{data['name']}*\nTag: {data['tag']}\nTrofei attuali: *{data['trophies']}*\nRecord trofei: *{data['highestTrophies']}*\nLivello: *{data['expLevel']}*\nVittorie 3v3: *{data['3vs3Victories']}*\nVittore in solo: *{data['soloVictories']}*\nVittorie in duo: *{data['duoVictories']}*\nPunti esperienza: *{data['expPoints']}*\nQualificato per la Brawl Stars Championship? *{esito}*"
    else:
        message = f"⚠️*Errore {response.status_code}: {response.reason}*"
    keyboard = [
        [
            InlineKeyboardButton(text="◀️", callback_data="back")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=message, parse_mode='Markdown', reply_markup=reply_markup)

async def brawlers_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tag = "%23" + update.message.text.upper().replace("#", "")
    response = requests.get(url=URL + "players/" + tag, headers=headers)
    if(response):
        data = response.json()
        brawlers = data['brawlers']
        page = 0
        num_pages = (len(brawlers) - 1) // 5 + 1
        while True:
            for brawler in brawlers[page*5 : (page+1)*5]:
                text = f"Brawler: {brawler['name']}\nTrofei attuali: {brawler['trophies']}\nRecord di trofei: {brawler['highestTrophies']}\nLivello: {brawler['power']}\nRank: {brawler['rank']}"
                buttons = []
                if page > 0:
                    buttons.append(InlineKeyboardButton("Indietro", callback_data=f"brawlers_player,{page-1}"))
                if page < num_pages - 1:
                    buttons.append(InlineKeyboardButton("Avanti", callback_data=f"brawlers_player,{page+1}"))
                reply_markup = InlineKeyboardMarkup([buttons])
                await update.message.reply_text(text, reply_markup=reply_markup)
            if num_pages == 1:
                break
            query = await context.bot.answer_callback_query(callback_query_id=update.callback_query.id, text=f"Pagina {page+1} di {num_pages}")
            if query:
                page = int(query.data.split(",")[1])
    else:
        await update.message.reply_text(f"Errore {response.status_code}: {response.reason}")

async def brawlers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(url=URL + "brawlers", headers=headers)
    if(response):
        data = response.json()
        for brawler in data['items']:
            message = f"{brawler['name']}\nAbilità stellare:\n"
            for i in brawler['starPowers']:
                message += f"{i['name']}\n"
            message += "Gadget:\n"
            for i in brawler['gadgets']:
                message += f"{i['name']}\n"
            await update.message.reply_text(message)
    else:
        await update.message.reply_text(f"Errore {response.status_code}: {response.reason}")

async def club(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tag = "%23" + update.message.text.upper().replace("#", "")
    response = requests.get(url=URL + "clubs/" + tag, headers=headers)
    if(response):
        data = response.json()
        message = f"Nome: {data['name']}\nTag: {data['tag']}\nDescrizione: {data['description']}"
        if(data['type']=="open"):
            tipo = "Aperto"
        elif(data['type']=="closed"):
            tipo = "Privato"
        elif(data['type']=="inviteOnly"):
            tipo = "Su invito"
        message += f"\nTipologia: {tipo}\nTrofei: {data['trophies']}\nTrofei richiesti per entrare: {data['requiredTrophies']}"
    else:
        message = f"⚠️*Errore {response.status_code}: {response.reason}*"
    keyboard = [
        [
            InlineKeyboardButton(text="◀️", callback_data="back")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=message, parse_mode='Markdown', reply_markup=reply_markup)

async def club_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tag = "%23" + update.message.text.split("/members ")[1].split()[0].upper().replace("#", "")
    response = requests.get(url=URL + "clubs/" + tag, headers=headers)
    if(response):
        data = response.json()
        for member in data['members']:
                message = f"Nome: {member['name']}\nTrofei: {member['trophies']}\nTag: {member['tag']}"
                if(member['role']=="president"):
                    ruolo = "Presidente"
                elif(member['role']=="vicePresident"):
                    ruolo = "Vicepresidente"
                elif(member['role']=="senior"):
                    ruolo = "Anziano"
                elif(member['role']=="member"):
                    ruolo = "Membro"
                message += f"\nRuolo: {ruolo}"
                await update.message.reply_text(message)
    else:
        await update.message.reply_text(f"Errore {response.status_code}: {response.reason}")

async def battle_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tag = "%23" + update.message.text.split("/battle ")[1].split()[0].upper().replace("#", "")
    response = requests.get(url=URL + "players/" + tag + "/battlelog", headers=headers)
    if(response):
        data = response.json()
        for battle in data['items']:
            if('battle' in battle and 'mode' in battle['battle']):
                if(battle['battle']['mode']=="duoShowdown" or battle['battle']['mode']=="soloShowdown"):
                    message = f"POSIZIONE: {battle['battle']['rank']}"
            if('result' in battle['battle']):
                if(battle['battle']['result']=="victory"):
                    message = "VITTORIA"
                elif(battle['battle']['result']=="defeat"):
                    message = "SCONFITTA"
            message += f"\nModalità: {battle['battle']['mode']}"
            if('map' in battle['event']):
                message += f"\nMappa: {battle['event']['map']}"
            if('trophyChange' in battle['battle']):
                message += f"\nCambiamento trofei: {battle['battle']['trophyChange']}"
            else:
                message += "\nNessun cambiamento di trofei"
            await update.message.reply_text(message)
    else:
        await update.message.reply_text(f"Errore {response.status_code}: {response.reason}")

async def ranking_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tag = update.message.text.split("/rankp ")[1].split()[0].upper()
    response = requests.get(url=URL + "rankings/" + tag + "/players", headers=headers)
    if(response):
        data = response.json()
        for ranked in data['items']:
            message = f"{ranked['rank']}.\nNome: {ranked['name']}\nTag: {ranked['tag']}\nTrofei: {ranked['trophies']}"
            if('club' in ranked):
                message += f"\nClub: {ranked['club']['name']}"
            else:
                message += "\nIn nessun club"
            await update.message.reply_text(message)
    else:
        await update.message.reply_text(f"Errore {response.status_code}: {response.reason}")

async def ranking_clubs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tag = update.message.text.split("/rankc ")[1].split()[0].upper()
    response = requests.get(url=URL + "rankings/" + tag + "/clubs", headers=headers)
    if(response):
        data = response.json()
        for ranked in data['items']:
            message = f"{ranked['rank']}.\nNome: {ranked['name']}\nTag: {ranked['tag']}\nTrofei: {ranked['trophies']}\nMembri: {ranked['memberCount']}"
            await update.message.reply_text(message)
    else:
        await update.message.reply_text(f"Errore {response.status_code}: {response.reason}")

async def ranking_brawlers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tag = update.message.text.split("/rankb ")[1].split()[0].upper()
    brawler = update.message.text.split("/rankb ")[1].split()[1].upper()
    br = requests.get(url=URL + "brawlers", headers=headers)
    if(br):
        data = br.json()
        for ranked in data['items']:
            if(brawler==ranked['name']):
                brawler_id = ranked['id']
    response = requests.get(url=URL + "rankings/" + tag + "/brawlers/" + str(brawler_id), headers=headers)
    if(response):
        data = response.json()
        for ranked in data['items']:
            message = f"{ranked['rank']}.\nNome: {ranked['name']}\nTag: {ranked['tag']}\nTrofei: {ranked['trophies']}"
            if('club' in ranked):
                message += f"\nClub: {ranked['club']['name']}"
            else:
                message += "\nIn nessun club"
            await update.message.reply_text(message)
    else:
        await update.message.reply_text(f"Errore {response.status_code}: {response.reason}")

async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            await update.message.reply_text(f"{mode}: {event['event']['map']}")
    else:
        await update.message.reply_text(f"Errore {response.status_code}: {response.reason}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, player))
    app.add_handler(MessageHandler(filters.TEXT, brawlers_player))
    app.add_handler(MessageHandler(filters.TEXT, brawlers))
    app.add_handler(MessageHandler(filters.TEXT, club))
    app.add_handler(MessageHandler(filters.TEXT, club_members))
    app.add_handler(MessageHandler(filters.TEXT, battle_log))
    app.add_handler(MessageHandler(filters.TEXT, ranking_players))
    app.add_handler(MessageHandler(filters.TEXT, ranking_clubs))
    app.add_handler(MessageHandler(filters.TEXT, ranking_brawlers))
    app.add_handler(MessageHandler(filters.TEXT, events))
    app.add_handler(CallbackQueryHandler(button))
    print("Loading...")
    app.run_polling()

if __name__ == "__main__":
    main()
