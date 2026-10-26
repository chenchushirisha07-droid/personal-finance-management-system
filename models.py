from sqlalchemy import Column, String, BigInteger, Integer
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    cardName = Column(String, index=True)
    cardNumber = Column(String)
    expiryDate = Column(String)
    cvv = Column(Integer)
    amount = Column(BigInteger)
    userName = Column(String)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    accountName = Column(String, index=True)
    goal = Column(String)
    paymentType = Column(String)
    dateOfPayment = Column(String)
    amount = Column(BigInteger)
    userName = Column(String)

class Bill(Base):
    __tablename__ = "bills"
    id = Column(Integer, primary_key=True, index=True)
    billName = Column(String, index=True)
    dueDate = Column(String)
    amount = Column(BigInteger)
    userName = Column(String)

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    goalName = Column(String, index=True)
    targetAmount = Column(BigInteger)
    savedAmount = Column(BigInteger, default=0)
    userName = Column(String)

class ContactMessage(Base):
    __tablename__ = "contact_messages"
    id = Column(Integer, primary_key=True, index=True)
    fullName = Column(String)
    emailAddress = Column(String)
    subject = Column(String)
    message = Column(String)