import os
import logging
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from groq import Groq

import config
import database

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
database.init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command. Shows persistent menu buttons."""
    
    keyboard = [
        [KeyboardButton(config.BTN_SETTINGS)],
        [KeyboardButton(config.BTN_HELP), KeyboardButton(config.BTN_ABOUT)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 <b>Welcome!</b>\n\n"
        "I am an Advanced AI Summarizer.\n"
        "Send me any <b>Text</b>, and I will summarize it for you.\n"
        "Use the buttons below to configure the bot.",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Main router: decides if input is a Menu Button or Text to summarize.
    """
    text = update.message.text
    user_id = update.effective_user.id

    # 1. Check for Menu Buttons
    if text == config.BTN_SETTINGS:
        await settings_menu(update, context)
        return
    elif text == config.BTN_HELP:
        await update.message.reply_text(config.HELP_TEXT, parse_mode=ParseMode.HTML)
        return
    elif text == config.BTN_ABOUT:
        await update.message.reply_text(config.ABOUT_TEXT, parse_mode=ParseMode.HTML)
        return

    # 2. Treat as Text to Summarize
    context.user_data['last_text'] = text
    wait_msg = await update.message.reply_text("⏳ Processing summary...")
    await process_summary(user_id, text, wait_msg, context)

async def settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = database.get_user_settings(user_id)
    
    model_name = next((k for k, v in config.AVAILABLE_MODELS.items() if v == settings['model']), settings['model'])

    text = (
        f"⚙️ <b>Configuration</b>\n\n"
        f"🧠 <b>Model:</b> <code>{model_name}</code>\n"
        f"🌐 <b>Language:</b> <code>{settings['language']}</code>\n"
        f"📏 <b>Length:</b> <code>{settings['length']}</code>\n"
        f"🎭 <b>Tone:</b> <code>{settings['tone']}</code>\n"
        f"🌡️ <b>Creativity:</b> <code>{settings['creativity']}</code>\n\n"
        "Select an option to change:"
    )

    keyboard = [
        [InlineKeyboardButton("🧠 Model", callback_data="menu_model"),
         InlineKeyboardButton("🌐 Language", callback_data="menu_lang")],
        [InlineKeyboardButton("📏 Length", callback_data="menu_len"),
         InlineKeyboardButton("🎭 Tone", callback_data="menu_tone")],
        [InlineKeyboardButton("🌡️ Creativity", callback_data="menu_creat")],
        [InlineKeyboardButton("❌ Close", callback_data="close")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

async def process_summary(user_id, text, message_obj, context):
    try:
        s = database.get_user_settings(user_id)
        
        lang_instr = "Keep original language" if s['language'] == "Auto" else f"Translate and write output in {s['language']}"
        length_instr = config.LENGTH_OPTIONS.get(s['length'], "standard summary")
        tone_desc = config.TONE_OPTIONS.get(s['tone'], "professional")
        
        system_content = config.SYSTEM_PROMPT_TEMPLATE.format(
            tone=tone_desc,
            length_instruction=length_instr,
            language_instruction=lang_instr
        )

        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"Text to summarize:\n\n{text}"}
        ]

        temp_val = config.CREATIVITY_LEVELS.get(s['creativity'], 0.5)

        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model=s['model'],
            temperature=temp_val,
            max_tokens=1500,
        )

        response_text = chat_completion.choices[0].message.content

        keyboard = [[InlineKeyboardButton("🔄 Redo / Regenerate", callback_data="redo")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await message_obj.edit_text(
            text=f"📝 <b>Summary:</b>\n\n{response_text}",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    except Exception as e:
        logging.error(f"Error: {e}")
        await message_obj.edit_text(text="❌ An error occurred while contacting the AI provider.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id

    if data == "close":
        await query.delete_message()
        return

    if data == "menu_main":
        await settings_menu(update, context)
        return

    if data == "redo":
        last_text = context.user_data.get('last_text')
        if last_text:
            await query.edit_message_text("⏳ Regenerating summary...", parse_mode=ParseMode.HTML)
            await process_summary(user_id, last_text, query.message, context)
        else:
            await query.edit_message_text("❌ Session expired. Please send the text again.", parse_mode=ParseMode.HTML)
        return

    # --- SUBMENUS ---
    settings = database.get_user_settings(user_id)

    async def show_selection_menu(title, options_dict, prefix, current_value, use_keys_as_value=False):
        keyboard = []
        for key, value in options_dict.items():
            is_selected = False
            if use_keys_as_value:
                if current_value == key: is_selected = True
            else:
                if current_value == value: is_selected = True

            label = f"✅ {key}" if is_selected else key
            callback_val = key 
            
            keyboard.append([InlineKeyboardButton(label, callback_data=f"{prefix}{callback_val}")])
            
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="menu_main")])
        
        await query.edit_message_text(
            f"<b>{title}</b>",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )

    if data == "menu_model":
        await show_selection_menu("Select AI Model:", config.AVAILABLE_MODELS, "set_model_", settings['model'], use_keys_as_value=False)
        return
    
    if data == "menu_lang":
        lang_dict = {l: l for l in config.SUPPORTED_LANGUAGES}
        await show_selection_menu("Select Output Language:", lang_dict, "set_lang_", settings['language'], use_keys_as_value=True)
        return

    if data == "menu_len":
        await show_selection_menu("Select Summary Length:", config.LENGTH_OPTIONS, "set_len_", settings['length'], use_keys_as_value=True)
        return

    if data == "menu_tone":
        await show_selection_menu("Select Tone:", config.TONE_OPTIONS, "set_tone_", settings['tone'], use_keys_as_value=True)
        return
    
    if data == "menu_creat":
        await show_selection_menu("Select Creativity Level:", config.CREATIVITY_LEVELS, "set_creat_", settings['creativity'], use_keys_as_value=True)
        return

    # --- SAVING SETTINGS ---
    if data.startswith("set_model_"):
        selected_name = data.replace("set_model_", "")
        model_id = config.AVAILABLE_MODELS.get(selected_name)
        database.update_user_setting(user_id, "model", model_id)
        await settings_menu(update, context)
        return

    if data.startswith("set_lang_"):
        database.update_user_setting(user_id, "language", data.replace("set_lang_", ""))
        await settings_menu(update, context)
        return

    if data.startswith("set_len_"):
        database.update_user_setting(user_id, "length", data.replace("set_len_", ""))
        await settings_menu(update, context)
        return

    if data.startswith("set_tone_"):
        database.update_user_setting(user_id, "tone", data.replace("set_tone_", ""))
        await settings_menu(update, context)
        return

    if data.startswith("set_creat_"):
        database.update_user_setting(user_id, "creativity", data.replace("set_creat_", ""))
        await settings_menu(update, context)
        return

if __name__ == '__main__':
    if not os.getenv("TELEGRAM_BOT_TOKEN") or not os.getenv("GROQ_API_KEY"):
        print("Error: .env file missing API keys.")
        exit(1)

    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('settings', settings_menu))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is running...")
    application.run_polling()