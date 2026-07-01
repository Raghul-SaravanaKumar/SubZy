from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as auth_router
from app.subscriptions import router as subscription_router
from app.reminder_scheduler import start_scheduler

app = FastAPI(
    title="SubZy API",
    description="Subscription Reminder Application",
    version="1.0.0"
)

# -----------------------------
# CORS Configuration
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],  # React Vite URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Register Routers
# -----------------------------
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    subscription_router,
    prefix="/subscriptions",
    tags=["Subscriptions"]
)

# -----------------------------
# Start Scheduler
# -----------------------------
@app.on_event("startup")
def startup():

    start_scheduler()

    print("SubZy Server Started Successfully")


# -----------------------------
# Home API
# -----------------------------
@app.get("/")
def home():

    return {
        "message": "Welcome to SubZy API 🚀"
    }


# -----------------------------
# Health Check API
# -----------------------------
@app.get("/health")
def health():

    return {
        "status": "Running",
        "application": "SubZy",
        "version": "1.0.0"
    }