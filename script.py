from selenium import webdriver
import time
import smtplib
from email.mime.text import MIMEText
from email.header    import Header

adres = "https://logowanie.wat.edu.pl/cas/login?service=https%3A%2F%2Fusos.wat.edu.pl%2Fkontroler.php%3F_action%3Dlogowaniecas%2Findex&locale=pl"
adres2 = "https://usos.wat.edu.pl/kontroler.php?_action=dla_stud/studia/oceny/index"
login = "example@student.wat.edu.pl"
haslo = "example"

def wyslijMaila():
    smtp_host = 'poczta.o2.pl'  
    login, password = 'example@o2.pl', 'example'
    recipients_emails = ['reciver1@student.wat.edu.pl','reciver2@student.wat.edu.pl']

    msg = MIMEText('Zmienila sie ocena na usos!', 'plain', 'utf-8')
    msg['Subject'] = Header('subject…', 'utf-8')
    msg['From'] = login
    msg['To'] = ", ".join(recipients_emails)

    s = smtplib.SMTP(smtp_host, 587, timeout=10)
    s.set_debuglevel(1)
    try:
        s.starttls()
        s.login(login, password)
        s.sendmail(msg['From'], recipients_emails, msg.as_string())
    finally:
        s.quit()


driver = webdriver.Firefox()
driver.get(adres)
driver.find_element_by_id('username').send_keys(login)
driver.find_element_by_id('password').send_keys(haslo)
time.sleep(2)
try:
    driver.find_element_by_name('submit').click()
except:
    time.sleep(1)

time.sleep(2)
driver.get(adres2)

source = driver.page_source
oldNumber = source.count("(brak ocen)")
time.sleep(5)

while True:
    driver.get(adres2)
    source = driver.page_source
    newNumber = source.count("(brak ocen)")
    if newNumber != oldNumber:
        wyslijMaila()
        oldNumber = newNumber
    else:
        print("Nothing")
    time.sleep(60)