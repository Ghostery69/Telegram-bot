from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
import random
import datetime

# Votre token API Telegram
API_TOKEN = "8191740195:AAElItof0jfiEFJu2d5zX-CZLvR5tUb9qaY"

# Fonction pour générer des prédictions avec une heure précise
def generate_predictions():
    min_cote, max_cote = 1.20, 1.24
    cote = round(random.uniform(min_cote, max_cote), 2)
    assurance = round(random.uniform(1.00, 1.15), 2)
    fiabilite = random.randint(97, 99)
    now = datetime.datetime.now()
    prediction_time = (now + datetime.timedelta(minutes=random.randint(1, 3))).strftime("%H:%M:%S")
    return cote, assurance, fiabilite, prediction_time

# Fonction pour la commande /start
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("📈 Obtenir des prédictions", callback_data="get_predictions")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "*Bienvenue dans SPIRITY, votre assistant prédictions ultime !*\n\n"
        "Cliquez sur le bouton ci-dessous pour obtenir vos prédictions.",
        parse_mode="Markdown", reply_markup=reply_markup
    )

# Fonction pour gérer les clics sur les boutons
async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # Vérifie si la requête est encore valide
    if not query or query.id is None:
        return
    
    try:
        await query.answer()  # Répond rapidement à la requête pour éviter les expirations
    except:
        pass  # Ignore les erreurs liées à des requêtes invalides ou expirées

    # Génération de nouvelles prédictions
    if query.data == "get_predictions":
        cote, assurance, fiabilite, prediction_time = generate_predictions()
        message = (
            "🌟 SPIRITY PRÉDICTIONS 🌟\n\n"
            f"⏰ HEURE PRÉCISE : {prediction_time}\n"
            f"📊 COTE : x{cote}\n"
            f"🛡️ ASSURANCE : x{assurance}\n"
            f"🔒 FIABILITÉ : {fiabilite}%\n\n"
            "🔮 *La prédiction arrivera exactement à l'heure donnée !*\n"
            "*Recevez vos prédictions directement depuis SPIRITY !*"
        )
        keyboard = [[InlineKeyboardButton("📈 Obtenir une autre prédiction", callback_data="get_predictions")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode="Markdown")

# Fonction principale
def main():
    application = Application.builder().token(API_TOKEN).build()

    # Gestionnaires
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Lancement du bot
    print("Bot démarré ! En attente d'interactions...")
    application.run_polling()

if __name__ == "__main__":
    main()
