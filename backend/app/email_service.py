import os
from dotenv import load_dotenv
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")


def send_email(to_email: str, subject: str, body: str):

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    email = sib_api_v3_sdk.SendSmtpEmail(

        sender={
            "name": "SubZy",
            "email": SENDER_EMAIL
        },

        to=[
            {
                "email": to_email
            }
        ],

        subject=subject,

        html_content=f"""
        <html>
        <body>

        <h2>SubZy Subscription Reminder</h2>

        <p>{body}</p>

        <br>

        <p>Regards,</p>
        <b>SubZy Team</b>

        </body>
        </html>
        """
    )

    try:

        response = api_instance.send_transac_email(email)

        return response

    except ApiException as e:

        print(e)

        raise Exception("Unable to send email")