from telegram import Update
from telegram.ext import ContextTypes
from database import SessionLocal, get_or_create_user, create_order, get_user_orders, get_all_users, get_pending_orders
from keyboards import main_menu_keyboard, product_keyboard, back_to_menu_keyboard, admin_keyboard
from datetime import datetime
from config import ADMIN_IDS, BOT_NAME

# Catálogo de produtos
PRODUCTS = {
    'consultavel': {
        'title': 'CONSULTÁVEL',
        'description': (
            '📱 *Material com acesso ao app do banco*\n'
            'Saldo verificado direto no aplicativo.\n\n'
            '✅ *Vantagens:*\n'
            '• Acesso completo ao app do banco\n'
            '• Verificação de saldo em tempo real\n'
            '• Material premium e exclusivo\n'
            '• Suporte dedicado\n\n'
            '💰 *Preço:* Sob consulta\n\n'
            '📞 *Entrega:* Manual pelo suporte'
        ),
        'emoji': '🔺'
    },
    'consultada': {
        'title': 'CONSULTADA',
        'description': (
            '📞 *Sem acesso ao app*\n'
            'Saldo consultado por ligação gravada na\n'
            'central do banco com atendente informando\n'
            'o limite disponível.\n\n'
            '✅ *Vantagens:*\n'
            '• Ligação gravada com o banco\n'
            '• Atendente confirma o limite\n'
            '• Processo seguro e verificado\n\n'
            '💰 *Preço:* Sob consulta\n\n'
            '📞 *Entrega:* Manual pelo suporte'
        ),
        'emoji': '📞'
    },
    'info_cc': {
        'title': 'INFO CC',
        'description': (
            '💳 *Dados de cartão testados (live)*\n'
            'Sem informação de saldo.\n\n'
            '✅ *Inclui:*\n'
            '• Dados completos do cartão\n'
            '• Cartão testado e verificado (live)\n'
            '• PACKS de INFO CC disponíveis\n\n'
            '💰 *Preço:* Sob consulta\n\n'
            '📞 *Entrega:* Manual pelo suporte'
        ),
        'emoji': '💳'
    },
    'info_cc_premium': {
        'title': 'INFO CC PREMIUM',
        'description': (
            '⭐ *Material exclusivo premium*\n'
            'Qualidade superior garantida.\n\n'
            '✅ *Diferenciais:*\n'
            '• Material selecionado e verificado\n'
            '• Alta qualidade garantida\n'
            '• Exclusividade no mercado\n'
            '• Suporte prioritário\n\n'
            '💰 *Preço:* Sob consulta\n\n'
            '📞 *Entrega:* Manual pelo suporte'
        ),
        'emoji': '⭐'
    },
    'lista_consul': {
        'title': 'LISTA DE CONSUL',
        'description': (
            '📋 *Acesso à lista exclusiva*\n'
            'Materiais verificados e atualizados.\n\n'
            '✅ *Contém:*\n'
            '• Lista completa e atualizada\n'
            '• Materiais verificados diariamente\n'
            '• Atualizações frequentes\n'
            '• Acesso à área VIP\n\n'
            '💰 *Preço:* Sob consulta\n\n'
            '📞 *Entrega:* Manual pelo suporte'
        ),
        'emoji': '📋'
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Mostra o catálogo principal"""
    user = update.effective_user
    db = SessionLocal()
    
    # Salvar usuário no banco
    get_or_create_user(
        db,
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    welcome_text = f"""
🌟 *{BOT_NAME}*

━━━━━━━━━━━━━━━━━━
⚡ *Rápido, simples e direto!*
📅 {datetime.now().strftime('%d de %B de %Y')}
━━━━━━━━━━━━━━━━━━

📋 *CATÁLOGO*

Escolha uma categoria abaixo:
    """
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=main_menu_keyboard()
    )
    db.close()

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manipula todos os cliques nos botões"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    db = SessionLocal()
    db_user = get_or_create_user(
        db,
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name
    )
    
    data = query.data
    
    # Menu principal
    if data == "menu_start":
        welcome_text = f"""
🌟 *{BOT_NAME}*

━━━━━━━━━━━━━━━━━━
⚡ *Rápido, simples e direto!*
📅 {datetime.now().strftime('%d de %B de %Y')}
━━━━━━━━━━━━━━━━━━

📋 *CATÁLOGO*

Escolha uma categoria abaixo:
        """
        await query.edit_message_text(
            welcome_text,
            parse_mode='Markdown',
            reply_markup=main_menu_keyboard()
        )
    
    # Categorias de produtos
    elif data.startswith("cat_"):
        category = data.replace("cat_", "")
        product = PRODUCTS.get(category)
        
        if product:
            category_text = f"""
{product['emoji']} *{product['title']}*

━━━━━━━━━━━━━━━━━━

{product['description']}

━━━━━━━━━━━━━━━━━━
💬 *O que deseja fazer?*
            """
            
            await query.edit_message_text(
                category_text,
                parse_mode='Markdown',
                reply_markup=product_keyboard(category)
            )
    
    # Comprar produto
    elif data.startswith("buy_"):
        category = data.replace("buy_", "")
        product = PRODUCTS.get(category)
        
        if product:
            # Criar pedido no banco
            create_order(
                db,
                db_user.id,
                category,
                product['title']
            )
            
            buy_text = f"""
✅ *PEDIDO REALIZADO!*

━━━━━━━━━━━━━━━━━━

{product['emoji']} Produto: *{product['title']}*
👤 Cliente: *{user.first_name}*
🆔 ID: `{user.id}`
📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

━━━━━━━━━━━━━━━━━━

📞 *SUPORTE*
Entre em contato para finalizar:

👤 @ProfessorShopSuporte

━━━━━━━━━━━━━━━━━━

⚡ *Seu pedido foi registrado!*
O suporte entrará em contato em breve.
            """
            
            await query.edit_message_text(
                buy_text,
                parse_mode='Markdown',
                reply_markup=back_to_menu_keyboard()
            )
    
    # Suporte
    elif data == "support":
        support_text = f"""
📞 *SUPORTE*

━━━━━━━━━━━━━━━━━━

👤 *Contato direto:*
@ProfessorShopSuporte

⏰ *Horário:*
Segunda a Sábado
09:00 às 22:00

━━━━━━━━━━━━━━━━━━

📩 Envie uma mensagem para:
@ProfessorShopSuporte

Nossa equipe responderá em instantes!
        """
        
        await query.edit_message_text(
            support_text,
            parse_mode='Markdown',
            reply_markup=back_to_menu_keyboard()
        )
    
    # Meus pedidos
    elif data == "my_orders":
        orders = get_user_orders(db, db_user.id)
        
        if orders:
            orders_text = f"""
📊 *MEUS PEDIDOS*

━━━━━━━━━━━━━━━━━━

👤 Cliente: *{user.first_name}*
📦 Total de pedidos: {len(orders)}

"""
            for i, order in enumerate(orders[-5:], 1):
                status_emoji = "✅" if order.status == "concluido" else "⏳"
                orders_text += f"{status_emoji} *Pedido {i}:*\n"
                orders_text += f"   📦 {order.product_description}\n"
                orders_text += f"   📅 {order.created_at.strftime('%d/%m/%Y')}\n"
                orders_text += f"   📌 Status: {order.status}\n\n"
            
            orders_text += "━━━━━━━━━━━━━━━━━━"
        else:
            orders_text = f"""
📊 *MEUS PEDIDOS*

━━━━━━━━━━━━━━━━━━

Você ainda não tem pedidos.

Volte ao catálogo e faça seu primeiro pedido! 🛒
            """
        
        await query.edit_message_text(
            orders_text,
            parse_mode='Markdown',
            reply_markup=back_to_menu_keyboard()
        )
    
    # Admin - Painel
    elif data == "admin":
        if user.id in ADMIN_IDS:
            await query.edit_message_text(
                "🔐 *PAINEL ADMINISTRATIVO*\n\nEscolha uma opção:",
                parse_mode='Markdown',
                reply_markup=admin_keyboard()
            )
        else:
            await query.answer("⛔ Acesso negado!", show_alert=True)
    
    # Admin - Ver usuários
    elif data == "admin_users":
        if user.id in ADMIN_IDS:
            users = get_all_users(db)
            users_text = f"👥 *USUÁRIOS CADASTRADOS*\n\nTotal: {len(users)}\n\n"
            
            for u in users[-10:]:
                users_text += f"• {u.first_name} (@{u.username or 'sem username'})\n"
                users_text += f"  ID: `{u.telegram_id}`\n"
                users_text += f"  Desde: {u.created_at.strftime('%d/%m/%Y')}\n\n"
            
            await query.edit_message_text(
                users_text,
                parse_mode='Markdown',
                reply_markup=admin_keyboard()
            )
    
    # Admin - Ver pedidos
    elif data == "admin_orders":
        if user.id in ADMIN_IDS:
            orders = get_pending_orders(db)
            orders_text = f"📦 *PEDIDOS PENDENTES*\n\nTotal: {len(orders)}\n\n"
            
            for order in orders[-10:]:
                orders_text += f"• Pedido #{order.id}\n"
                orders_text += f"  📦 {order.product_description}\n"
                orders_text += f"  👤 User ID: {order.user_id}\n"
                orders_text += f"  📅 {order.created_at.strftime('%d/%m/%Y')}\n"
                orders_text += f"  📌 Status: {order.status}\n\n"
            
            await query.edit_message_text(
                orders_text,
                parse_mode='Markdown',
                reply_markup=admin_keyboard()
            )
    
    # Admin - Estatísticas
    elif data == "admin_stats":
        if user.id in ADMIN_IDS:
            total_users = len(get_all_users(db))
            total_orders = len(get_pending_orders(db))
            
            stats_text = f"""
📊 *ESTATÍSTICAS*

━━━━━━━━━━━━━━━━━━

👥 Total de usuários: {total_users}
📦 Pedidos pendentes: {total_orders}
📅 Data: {datetime.now().strftime('%d/%m/%Y')}

━━━━━━━━━━━━━━━━━━
            """
            
            await query.edit_message_text(
                stats_text,
                parse_mode='Markdown',
                reply_markup=admin_keyboard()
            )
    
    db.close()

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /admin - Painel administrativo"""
    user = update.effective_user
    
    if user.id in ADMIN_IDS:
        admin_text = f"""
🔐 *PAINEL ADMINISTRATIVO*

━━━━━━━━━━━━━━━━━━
👤 Admin: {user.first_name}
📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}
━━━━━━━━━━━━━━━━━━

Selecione uma opção:
        """
        
        await update.message.reply_text(
            admin_text,
            parse_mode='Markdown',
            reply_markup=admin_keyboard()
        )
    else:
        await update.message.reply_text("⛔ Você não tem permissão para acessar o painel admin.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde mensagens normais"""
    user = update.effective_user
    
    response = f"""
👋 Olá {user.first_name}!

Use /start para ver nosso catálogo
ou /admin para o painel (se autorizado).

📞 Suporte: @ProfessorShopSuporte
    """
    
    await update.message.reply_text(response)