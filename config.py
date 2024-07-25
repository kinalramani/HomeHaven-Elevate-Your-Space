from dotenv import load_dotenv
import os,stripe

load_dotenv()

db_url=os.environ.get("DB_URL")

sender_email=os.environ.get("sender_email")
password=os.environ.get("password")
stripe.api_key=os.environ.get("STRIPE_SECRET_KEY")