import RPi.GPIO as GPIO
import time
import picamera
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

# Configure GPIO
GPIO.setmode(GPIO.BOARD)
PIR_PIN = 11
GPIO.setup(PIR_PIN, GPIO.IN)

# Email configuration
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
EMAIL_FROM = 'your_email@example.com'
EMAIL_PASSWORD = 'your_email_password'
EMAIL_TO = 'recipient@example.com'
EMAIL_SUBJECT = 'Motion Detected!'
EMAIL_MESSAGE = 'Motion detected. Check the attached photo.'

# Initialize camera
camera = picamera.PiCamera()
camera.resolution = (1024, 768)

def send_email(subject, message, attachment):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    with open(attachment, 'rb') as img:
        img_data = img.read()
        image = MIMEImage(img_data, name="motion.jpg")
        msg.attach(image)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    server.quit()

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion detected!")
            photo_path = "/home/pi/motion.jpg"  # Adjust the path as needed
            camera.capture(photo_path)
            send_email(EMAIL_SUBJECT, EMAIL_MESSAGE, photo_path)
            print("Email sent with attached photo.")
            time.sleep(5)  # Avoid multiple detections in a short time
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
    camera.close()
