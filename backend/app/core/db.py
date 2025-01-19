from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import User, UserCreate
from .DBHelper import DBHelper

db_helper = DBHelper()

POSTGRES_URL = settings.POSTGRES_URL
engine = create_engine(POSTGRES_URL)

def get_session():
    with Session(engine) as session:
        yield session

# Database initialization function
def init_db(session: Session) -> None:
    """
    Initializes the database and creates a superuser if it doesn't exist.
    """
    # Check if the superuser exists
    user = session.exec(select(User).where(User.email == "admin@example.com")).first()
    if not user:
        # Create the superuser
        user_in = UserCreate(
            email= settings.FIRST_SUPERUSER,
            password= settings.FIRST_SUPERUSER_PASSWORD,
        )
        crud.create_user(session=session, user_create=user_in)
        print(f"Superuser {settings.FIRST_SUPERUSER} created.")
    else:
        print(f"Superuser {settings.FIRST_SUPERUSER} already exists.")