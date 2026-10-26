from fastapi import FastAPI, Request, Form, Response, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# Create tables automatically on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fintrack Application")

# Mount static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Helper function
def get_current_user(request: Request):
    return request.cookies.get("auth_token")

# ==========================================
# PUBLIC ROUTES
# ==========================================

@app.get("/")
async def home(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "user": user})

@app.get("/about")
async def about(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="about.html", context={"request": request, "user": user})

@app.get("/services")
async def services(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="services.html", context={"request": request, "user": user})

@app.get("/contact")
async def contact_get(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="contact.html", context={"request": request, "user": user, "success": False})

@app.post("/contact")
async def contact_post(
    request: Request,
    fullName: str = Form(...),
    emailAddress: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    new_contact = models.ContactMessage(
        fullName=fullName,
        emailAddress=emailAddress,
        subject=subject,
        message=message
    )
    db.add(new_contact)
    db.commit()
    
    user = get_current_user(request)
    return templates.TemplateResponse(
        request=request, 
        name="contact.html", 
        context={"request": request, "user": user, "success": True}
    )

# ==========================================
# AUTHENTICATION ROUTES
# ==========================================

@app.get("/login")
async def login_page(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request, "user": None, "error": None})

@app.post("/login")
async def login_submit(
    request: Request,
    email: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    
    if not db_user or db_user.password != password:
        return templates.TemplateResponse(
            request=request, 
            name="login.html", 
            context={"request": request, "user": None, "error": "Invalid email or password"}
        )
    
    username = email.split('@')[0]
    redirect_response = RedirectResponse(url="/dashboard", status_code=302)
    redirect_response.set_cookie(key="auth_token", value=username)
    return redirect_response

@app.post("/signup")
async def signup(
    request: Request,
    email: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        return templates.TemplateResponse(
            request=request, 
            name="login.html", 
            context={"request": request, "user": None, "error": "Email is already registered"}
        )
        
    new_user = models.User(email=email, password=password)
    db.add(new_user)
    db.commit()
    
    username = email.split('@')[0]
    redirect_response = RedirectResponse(url="/dashboard", status_code=302)
    redirect_response.set_cookie(key="auth_token", value=username)
    return redirect_response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="auth_token", path="/")
    return response

# ==========================================
# DASHBOARD & DATA ENTRY ROUTES
# ==========================================

@app.get("/dashboard")
async def dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    user_accounts = db.query(models.Account).filter(models.Account.userName == user).all()
    user_transactions = db.query(models.Transaction).filter(models.Transaction.userName == user).all()
    user_bills = db.query(models.Bill).filter(models.Bill.userName == user).all()
    user_goals = db.query(models.Goal).filter(models.Goal.userName == user).all()
    
    total_balance = sum(account.amount for account in user_accounts)
    total_expenses = sum(txn.amount for txn in user_transactions if txn.paymentType == "Debit")
    
    ai_advice = "Welcome to Fintrack! Add your accounts and transactions to receive personalized AI financial insights."
    if total_balance > 0 or total_expenses > 0:
        if total_expenses > total_balance:
            ai_advice = "⚠️ **Budget Alert:** Your total expenses exceed your total account balance. Try reducing non-essential debit transactions this week."
        elif total_balance > 50000:
            ai_advice = "💡 **Growth Insight:** You are maintaining a healthy balance! Consider putting surplus funds toward your active savings goals."
        elif len(user_bills) > 0:
            ai_advice = f"📅 **Bill Reminder:** You have {len(user_bills)} upcoming bill(s) pending. Ensure your balances cover these payments to avoid penalties."
        else:
            ai_advice = "✨ **Great Job:** Your spending is currently balanced relative to your accounts. Keep up the consistent financial tracking!"

    return templates.TemplateResponse(
        request=request, 
        name="dashboard.html", 
        context={
            "request": request, 
            "user": user, 
            "accounts": user_accounts, 
            "transactions": user_transactions,
            "bills": user_bills,
            "goals": user_goals,
            "total_balance": total_balance,
            "total_expenses": total_expenses,
            "ai_advice": ai_advice
        }
    )

@app.post("/add-account")
async def add_account(
    request: Request, cardNumber: str = Form(...), cardName: str = Form(...),
    expiryDate: str = Form(...), cvv: int = Form(...), amount: int = Form(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(request)
    new_account = models.Account(cardNumber=cardNumber, cardName=cardName, expiryDate=expiryDate, cvv=cvv, amount=amount, userName=user)
    db.add(new_account)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=302)

@app.post("/add-transaction")
async def add_transaction(
    request: Request, accountName: str = Form(...), goal: str = Form(...),
    paymentType: str = Form(...), dateOfPayment: str = Form(...), amount: int = Form(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(request)
    new_transaction = models.Transaction(accountName=accountName, goal=goal, paymentType=paymentType, dateOfPayment=dateOfPayment, amount=amount, userName=user)
    db.add(new_transaction)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=302)

@app.post("/add-bill")
async def add_bill(
    request: Request, billName: str = Form(...), dueDate: str = Form(...),
    amount: int = Form(...), db: Session = Depends(get_db)
):
    user = get_current_user(request)
    new_bill = models.Bill(billName=billName, dueDate=dueDate, amount=amount, userName=user)
    db.add(new_bill)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=302)

@app.post("/add-goal")
async def add_goal(
    request: Request, goalName: str = Form(...), targetAmount: int = Form(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(request)
    new_goal = models.Goal(goalName=goalName, targetAmount=targetAmount, savedAmount=0, userName=user)
    db.add(new_goal)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=302)

@app.post("/update-goal/{goal_id}")
async def update_goal(
    goal_id: int,
    addAmount: int = Form(...),
    db: Session = Depends(get_db)
):
    goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if goal:
        goal.savedAmount += addAmount
        db.commit()
    return RedirectResponse(url="/dashboard", status_code=302)