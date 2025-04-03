import subprocess
import smtplib
import os
from email.message import EmailMessage

from parser.report import Report


OUTPUT_MARKDOWN = os.environ['OUTPUT_IN_MARKDOWN'].lower() == "true"
EMAIL_RECIPIENT = os.environ['EMAIL_RECIPIENT']
INPUT_FILENAME = "linkchecker-out.xml"
OUTPUT_FILENAME = "404.md" if OUTPUT_MARKDOWN else "404.txt"
ATTACHMENT_FILENAME = "report.md" if OUTPUT_MARKDOWN else "report.txt"
ATTACHMENT_MIME_SUBTYPE = "markdown" if OUTPUT_MARKDOWN else "plain"
URL = "https://docs.csc.fi/"


subprocess.run(["linkchecker", "--check-extern", "--user-agent", "Mozilla/5.0 (compatible; LinkChecker/9.3; +http://wummel.github.io/linkchecker/)", "-F", "xml", "-q", URL], check=False)

print("BROKEN LINKS REPORT: \n")
report = Report(INPUT_FILENAME)
results = report.results
for url, name, parent_url, result in results:
    print(f"URL: {url}\nName: {name}\nParent URL: {parent_url}\nResult: {result}\n")
print(f"Processed: {len(results)}")
report.to_file(OUTPUT_FILENAME)

msg = EmailMessage()
msg["From"] = "noreply@csc.fi"
msg["Subject"] = "Broken links report"
msg["To"] = os.getenv('EMAIL_RECIPIENT')
msg.set_content("You will find attached the broken links report of docs.csc.fi")
msg.add_attachment(open(OUTPUTFILE, "r", encoding="utf-8").read(), subtype='txt', filename='404.txt')

s = smtplib.SMTP('smtp.pouta.csc.fi')
s.send_message(msg)
print("Email sent")
