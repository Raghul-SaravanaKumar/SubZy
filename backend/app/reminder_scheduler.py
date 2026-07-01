from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from bson import ObjectId

from app.database import db
from app.email_service import send_email


def check_reminders():
    """
    Checks subscriptions every day and sends reminder emails.
    """

    print("Checking subscription reminders...")

    subscriptions = list(
        db.subscriptions.find(
            {
                "reminder_sent": False
            }
        )
    )

    today = datetime.today().date()

    for subscription in subscriptions:

        try:

            renewal_date = datetime.strptime(
                subscription["renewal_date"],
                "%Y-%m-%d"
            ).date()

            reminder_date = renewal_date - timedelta(
                days=subscription["reminder_days"]
            )

            if today != reminder_date:
                continue

            user = db.users.find_one(
                {
                    "_id": ObjectId(subscription["user_id"])
                }
            )

            if not user:
                continue

            subject = f"Reminder: {subscription['subscription_name']}"

            body = f"""
Hello {user['name']},

Your subscription is about to renew.

Subscription : {subscription['subscription_name']}
Category     : {subscription['category']}
Amount       : {subscription['amount']} {subscription['currency']}
Renewal Date : {subscription['renewal_date']}

Please make sure your payment method is active.

Regards,
SubZy Team
"""

            send_email(
                user["email"],
                subject,
                body
            )

            db.subscriptions.update_one(
                {
                    "_id": subscription["_id"]
                },
                {
                    "$set": {
                        "reminder_sent": True
                    }
                }
            )

            print(
                f"Reminder sent to {user['email']}"
            )

        except Exception as e:

            print(
                f"Scheduler Error : {e}"
            )


def start_scheduler():

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        check_reminders,
        trigger="cron",
        hour=9,
        minute=0
    )

    scheduler.start()

    print("Reminder Scheduler Started")