from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

db = SessionLocal()

admin_user = User(
    username="admin",
    hashed_password=get_password_hash("admin123"),
    role="admin",
    is_active=True
)

db.add(admin_user)
db.commit()
db.close()

print("Admin user created!")
