from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from secure import hash_password ,verify_password

DATABASE_URL = "postgresql://postgres:PASSWORD@127.0.0.1:5432/DATABASENAME"

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    

def insert_user(email, password):
    session = SessionLocal()
    try:
        hashed_password = hash_password(password)
        user = session.query(User).filter(User.email == email).first()
        if user:
            user.password = hashed_password
        else:
            new_user = User(email=email, password=hashed_password)
            session.add(new_user)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
    finally:
        session.close()
        
def get_user_password(email):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == email).first()
        if user:
            return user.password
        else:
            return None
    finally:
        session.close()
