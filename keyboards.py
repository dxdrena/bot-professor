from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    """Teclado principal do catálogo"""
    keyboard = [
        [
            InlineKeyboardButton("🔺 CONSULTÁVEL", callback_data="cat_consultavel"),
        ],
        [
            InlineKeyboardButton("📞 CONSULTADA", callback_data="cat_consultada"),
        ],
        [
            InlineKeyboardButton("💳 INFO CC", callback_data="cat_info_cc"),
        ],
        [
            InlineKeyboardButton("⭐ INFO CC PREMIUM", callback_data="cat_info_cc_premium"),
        ],
        [
            InlineKeyboardButton("📋 Lista de Consul", callback_data="cat_lista_consul"),
        ],
        [
            InlineKeyboardButton("📞 Suporte", callback_data="support"),
            InlineKeyboardButton("📊 Meus Pedidos", callback_data="my_orders"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def product_keyboard(category):
    """Teclado para produtos de uma categoria"""
    keyboard = [
        [
            InlineKeyboardButton("🛒 COMPRAR", callback_data=f"buy_{category}"),
        ],
        [
            InlineKeyboardButton("📞 Falar com Suporte", callback_data="support"),
        ],
        [
            InlineKeyboardButton("🔙 Voltar ao Catálogo", callback_data="menu_start"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_to_menu_keyboard():
    """Teclado para voltar ao menu"""
    keyboard = [
        [
            InlineKeyboardButton("🔙 Voltar ao Catálogo", callback_data="menu_start"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def admin_keyboard():
    """Teclado do painel admin"""
    keyboard = [
        [
            InlineKeyboardButton("👥 Usuários", callback_data="admin_users"),
            InlineKeyboardButton("📦 Pedidos", callback_data="admin_orders"),
        ],
        [
            InlineKeyboardButton("📊 Estatísticas", callback_data="admin_stats"),
        ],
        [
            InlineKeyboardButton("🔙 Menu Principal", callback_data="menu_start"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)