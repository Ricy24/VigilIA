"""
Script para crear el usuario administrador inicial.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.db.models.user import User, UserRole
from app.core.security import get_password_hash

def init_db():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "admin@vigilia.com").first()
        if not user:
            print("Creando usuario admin@vigilia.com ...")
            user = User(
                email="admin@vigilia.com",
                full_name="Administrador VigilIA",
                hashed_password=get_password_hash("admin1234"),
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(user)
            db.commit()
            print("Usuario creado exitosamente.")
        else:
            print("El usuario admin ya existe.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
