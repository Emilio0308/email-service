import pika
import json
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

load_dotenv()
email_html = """
<section>
  <h2 style="font-size: 16px">

    <strong>Hello world</strong>
  </h2>
  <p>Access Lancer relaunch</p>

  <section style="display: flex; gap: 15px; flex-wrap: wrap">
    <img
      style="width: 100px; height: 100px"
      src="https://res.cloudinary.com/danjwp1pg/image/upload/v1689731280/ab/developers/Aron.jpg"
      alt=""
    />
    <img
      style="width: 100px; height: 100px"
      src="https://res.cloudinary.com/danjwp1pg/image/upload/v1690148378/ab/developers/Emilio.jpg"
      alt=""
    />
    <img
      style="width: 100px; height: 100px"
      src="https://res.cloudinary.com/danjwp1pg/image/upload/v1689731280/ab/developers/Fabricio.jpg"
      alt=""
    />
    <img
      style="width: 100px; height: 100px"
      src="https://res.cloudinary.com/danjwp1pg/image/upload/v1689731279/ab/developers/Luisa.jpg"
      alt=""
    />
    <img
      style="width: 100px; height: 100px"
      src="https://res.cloudinary.com/danjwp1pg/image/upload/v1689731280/ab/developers/Sergio.jpg"
      alt=""
    />
  </section>
</section>
"""


amqpUrl = os.getenv('AMQPURL')


params = pika.URLParameters(amqpUrl)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='email-service')


def send_email(ch, method, properties, body):
    print('is channel close', channel.is_closed)

    data = json.loads(body)
    if properties.content_type == 'send-message':
        password = os.getenv('PASSWORD')
        email_sender = 'emiliorivasruiz@gmail.com'
        email_receiver = data['email']
        subject = data['subject']
        message = data['message']

        email_message = EmailMessage()
        email_message['From'] = email_sender
        email_message['To'] = email_receiver
        email_message['Subject'] = subject
        # email_message.add_alternative(email_html, subtype='html')
        email_message.set_content(message)

        context = ssl.create_default_context()
        print(context)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, password)
            # smtp.send_message(email_message)
            smtp.sendmail(email_sender, email_receiver,
                          email_message.as_string())

    if properties.content_type == 'message-text':
        print('mensaje recibido en la cola message-text', data)

    print('is channel close', channel.is_closed)


channel.basic_consume(
    'email-service', on_message_callback=send_email, auto_ack=True)

print('consumer iniciado')


# channel.start_consuming()
# channel.close()


def start_consuming():
    channel.start_consuming()
