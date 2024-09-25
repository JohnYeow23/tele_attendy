import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# Replace 'YOUR_BOT_TOKEN' with the actual token you receive from BotFather
TOKEN = 'YOUR_BOT_TOKEN'

# Define states
NAME, EMAIL, REASON = range(3)

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Welcome to the Club Absence Reporting Bot! "
        "Please provide your name."
    )
    return NAME

# Handler for receiving name
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text(
        "Thank you. Now, please provide your school email address."
    )
    return EMAIL

# Handler for receiving email
async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['email'] = update.message.text
    await update.message.reply_text(
        "Got it. Lastly, please provide the reason for your absence."
    )
    return REASON

# Handler for receiving reason and completing the report
async def get_reason(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['reason'] = update.message.text
    
    # Here you would typically save this information to a database
    # For this example, we'll just print it and send a confirmation message
    print(f"Absence Report:\nName: {context.user_data['name']}\n"
          f"Email: {context.user_data['email']}\n"
          f"Reason: {context.user_data['reason']}")
    
    await update.message.reply_text(
        "Thank you for your absence report. It has been recorded."
    )
    return ConversationHandler.END

# Handler for canceling the conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Absence report cancelled. Use /start to begin a new report."
    )
    return ConversationHandler.END

def main() -> None:
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Set up the ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reason)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()