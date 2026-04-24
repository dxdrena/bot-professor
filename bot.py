#!/usr/bin/env python3
"""
🌟 Professor | Shop - Bot Telegram
Loja virtual com catálogo interativo
"""

from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import BOT_TOKEN, BOT_NAME
from database import init_db
from handlers import start, button_handler, admin_command, handle_message
import logging

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Função principal"""
    print("=" * 50)
    print(f"🌟 {BOT_NAME}")
    print("=" * 50)
    print("Iniciando bot...")
    
    # Inicializar banco de dados
    init_db()
    
    # Criar aplicação
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Adicionar handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Iniciar bot
    print("✅ Bot pronto!")
    print(f"🚀 {BOT_NAME} está rodando!")
    print("Pressione Ctrl+C para parar.")
    print("=" * 50)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()