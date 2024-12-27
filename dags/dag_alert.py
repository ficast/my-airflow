"""
DAG Template
"""

from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from twilio.rest import Client
import os


# Twilio credentials (store securely using Airflow connections or environment variables)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # Twilio's sandbox number
RECIPIENTS = ['whatsapp:+553199695717', 'whatsapp:+351912161468']  # Replace with actual numbers

def send_whatsapp_alert(**kwargs):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    for recipient in RECIPIENTS:
        message = client.messages.create(
            body="Olá camarada, tudo bem? Não se esqueça de realizar a sua contribuição mensal. Ajude a construir a Unidade Popular!",
            from_=TWILIO_WHATSAPP_NUMBER,
            to=recipient
        )
        print(f"Message sent to {recipient}: {message.sid}")

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    default_args=default_args,
    schedule_interval='@monthly',  # Monthly schedule
    start_date=datetime(2025, 1, 1),  # Replace with desired start date
    catchup=False,
    description='Sends a WhatsApp alert monthly'
)
def whatsapp_monthly_alert():
    send_alert = PythonOperator(
        task_id='send_whatsapp_alert',
        python_callable=send_whatsapp_alert,
        provide_context=True,
    )

    send_alert

# Instantiate the DAG
dag = whatsapp_monthly_alert()
