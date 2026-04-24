from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modelo de Usuário
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_interaction = Column(DateTime, default=datetime.utcnow)

# Modelo de Pedido
class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    category = Column(String(50))
    product_description = Column(Text)
    status = Column(String(20), default='pendente')
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """Inicializa o banco de dados"""
    Base.metadata.create_all(engine)
    print("✅ Banco de dados inicializado!")

def get_db():
    """Retorna uma sessão do banco"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_or_create_user(db, telegram_id, username=None, first_name=None, last_name=None):
    """Busca ou cria um usuário"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    
    if not user:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✅ Novo usuário: {first_name} (@{username})")
    else:
        user.username = username or user.username
        user.first_name = first_name or user.first_name
        user.last_name = last_name or user.last_name
        user.last_interaction = datetime.utcnow()
        db.commit()
    
    return user

def create_order(db, user_id, category, product_description):
    """Cria um novo pedido"""
    order = Order(
        user_id=user_id,
        category=category,
        product_description=product_description
    )
    db.add(order)
    db.commit()
    print(f"🛒 Novo pedido: {category} - User ID: {user_id}")
    return order

def get_user_orders(db, user_id):
    """Retorna pedidos de um usuário"""
    return db.query(Order).filter(Order.user_id == user_id).all()

def get_all_users(db):
    """Retorna todos os usuários"""
    return db.query(User).all()

def get_pending_orders(db):
    """Retorna pedidos pendentes"""
    return db.query(Order).filter(Order.status == 'pendente').all()