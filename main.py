from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
import requests
import time
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN, API_KEY, IDS_ALLOWED


# Définir une fonction de gestionnaire pour la commande /start
def start(update, context):
    message1 = "<b>Mise en Relation - Premium 💎</b>\n\n" \
              "➲ <b>La Commande</b> /go vous permet de prendre connaissance des critères pour pouvoir accéder au VIP. 💸\n\n" \
              "➲ VIP permet d'échanger en privé avec nos équipes, ce qui facilite l'accompagnement.\n\n" \
              "<b>FAQ</b> : <a href='https://t.me/leobrgsFx_group'>@leobrgsFx_group</a> 🕵️‍♂️\n" 

    context.bot.send_message(chat_id=update.effective_chat.id, text=message1, parse_mode=ParseMode.HTML)
   
    # Planifier l'envoi du deuxième message après un délai de 5 secondes
    context.job_queue.run_once(send_second_message, 5, context=update.effective_chat.id)

def send_second_message(context: CallbackContext):
    chat_id = context.job.context
    message2 =  "🛡️ Chat Sécurisé\n"\
                "Développé par <a href='https://t.me/leobrgsFx'>l'admin.</a>"
    context.bot.send_message(chat_id=chat_id, text=message2, parse_mode=ParseMode.HTML)


# Définir une fonction de gestionnaire pour la commande /help
def help(update, context):
    message = "<b>Listes de commandes :</b>\n\n" \
              "- Relancer la discution /start\n" \
              "- Les critères pour rejoindre /go\n" \
              "- Nos services /services\n" \

    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)

# Définir une fonction de gestionnaire pour la commande /go
def go(update, context):
    first_name = update.effective_user.first_name
    message1 = f"<b>Hello {first_name} 💥 !!</b>\n\n" \
              "<b>Envoi-moi ces infos ici </b> \n" \
              "<b>  👉  @leobrgsFx  👈</b> \n\n" \
              "<b>1</b> Ton nom \n" \
              "<b>2</b> Ton age \n" \
              "<b>3</b> Ta ville (facultatif) \n" \
              "<b>4</b> Comment es-tu déjà formé ?\n" \
              "<b>5</b> En quoi cela t'apportera de nous rejoindre ? \n\n" \
              "Découvres les /services \n\n" \

              
    context.bot.send_message(chat_id=update.effective_chat.id, text=message1, parse_mode=ParseMode.HTML)
    
    # Planifier l'envoi du deuxième message après un délai de 2 secondes
    context.job_queue.run_once(send_tree_message, 2, context=update.effective_chat.id)

def send_tree_message(context: CallbackContext):
    chat_id = context.job.context
    message3 = "⚠️ <b>Notez cependant</b> que selon votre ville, nous pourrions vous mettres directement en relation avec des personnes physiques. \n"
    context.bot.send_message(chat_id=chat_id, text=message3, parse_mode=ParseMode.HTML)



# Définir une fonction de gestionnaire pour la commande /services
def services(update, context):
    first_name = update.effective_user.first_name
    message = f"Re {first_name}\n\n" \
              "<b>🚀 | Abordable en 2023.</b> \n\n" \
              "Ces businesses sont apparus en 2020, lors du confinement. Et la facilité d'y accéder s'est nettement développée depuis 2022. \n\n" \
              " ✅ Trading\n" \
              " ✅ Investissement crypto\n" \
              " ✅ MLM (SMMA 2.0) \n" \
              " ☑️ Dropshipping \n" \
              " ☑️ e-Commerce\n\n" \
              "<b>FAQ</b> : <a href='https://t.me/leobrgsFx_group'>@leobrgsFx_group</a> 🕵️‍♂️\n"
              
    keyboard = [
        [
            InlineKeyboardButton("Appel Privé + 📞: Offert 1-3/pers", callback_data='/go')
        ],
        [
            InlineKeyboardButton("Ecole Trading + 💎: Prix sur demande", callback_data='/go')
        ],
        [
            InlineKeyboardButton("Ecole Crypto + 💎: Prix sur demande", callback_data='/go')
        ],
        [
            InlineKeyboardButton("En savoir plus sur le MLM (SMMA 2.0)", callback_data='/go')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

# Définir une fonction de gestionnaire pour les messages texte
def echo(update, context):
    user_id = update.effective_chat.id
    if user_id in IDS_ALLOWED:
        while True:
            try:
                response = requests.get(f"https://api.example.com/data?api_key={API_KEY}")
                if response.status_code == 200:
                    data = response.json()
                    context.bot.send_message(chat_id=user_id, text=f"Voici les données : {data}")
                    break  # Sortir de la boucle en cas de succès
                else:
                    context.bot.send_message(chat_id=user_id, text="Erreur lors de la récupération des données.")
                    break  # Sortir de la boucle en cas d'erreur
            except Exception as e:
                print(f"Erreur lors de la récupération des données : {e}")
                print("Tentative de reconnexion dans 5 secondes...")
                time.sleep(5)
    else:
        context.bot.send_message(chat_id=user_id, text="Ce message n'est pas autorisé 🐊.")

# Définir la fonction principale
def main():
    # Créer un objet Updater et passer le jeton de votre bot
    updater = Updater(token=BOT_TOKEN)

    # Obtenir le gestionnaire du répartiteur pour enregistrer les gestionnaires de commandes et de messages
    dispatcher = updater.dispatcher

    # Ajouter les gestionnaires de commandes
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('go', go))
    dispatcher.add_handler(CommandHandler('services', services))
    dispatcher.add_handler(CallbackQueryHandler(go, pattern='/go'))

    # Ajouter un gestionnaire de messages
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    # Démarrer le bot
    while True:
        try:
            updater.start_polling()
            break  # Sortir de la boucle en cas de succès
        except Exception as e:
            print(f"Erreur lors du démarrage du bot : {e}")
            print("Tentative de reconnexion dans 5 secondes...")
            time.sleep(5)

    # Exécuter le bot jusqu'à ce que vous appuyiez sur Ctrl-C pour arrêter
    updater.idle()


# Appeler la fonction principale pour démarrer le bot
if __name__ == '__main__':
    main()
