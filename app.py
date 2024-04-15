import subprocess
import smtplib
import os
from email.message import EmailMessage

EMAIL_RECIPIENT = os.environ['EMAIL_RECIPIENT']
FILENAME = "linkchecker-out.txt"
OUTPUTFILE = "404.txt"
URL = "https://docs.csc.fi/"
subprocess.run(["linkchecker", "--check-extern", "--user-agent", "Mozilla/5.0 (compatible; LinkChecker/9.3; +http://wummel.github.io/linkchecker/)", "-F", "text", "-q", URL], check=False)

with open(FILENAME, "r", encoding="utf-8") as f_in:
    file = f_in.read()
    result = "Result     Error: 404 Not Found"
    counter = 0

    with open("404.txt", "w+", encoding="utf-8") as f_out:
        print("BROKEN LINKS REPORT: \n")
        for line in file.split('\n\n'):
            if result in line:
                url = line.split('\n')[0].split('        ')[-1]
                name = line.split('\n')[1].split('       ')[-1]
                parent_url = line.split('\n')[2].split(' ')[-5].strip(',')
                counter += 1
                print(f"URL: {url}\nName: {name}\nParent URL: {parent_url}\n{result}\n")
                f_out.write(f"URL: {url}\nName: {name}\nParent URL: {parent_url}\n{result}\n\n")
        print(f"Processed: {counter}")
        f_out.write(f"Processed: {counter}")

msg = EmailMessage()
msg["From"] = "noreply@csc.fi"
msg["Subject"] = "Broken links report"
msg["To"] = os.getenv('EMAIL_RECIPIENT')
msg.set_content("You will find attached the broken links report of docs.csc.fi")
msg.add_attachment(open(OUTPUTFILE, "r", encoding="utf-8").read(), subtype='txt', filename='404.txt')

s = smtplib.SMTP('smtp.pouta.csc.fi')
s.send_message(msg)
print("Email sent")
