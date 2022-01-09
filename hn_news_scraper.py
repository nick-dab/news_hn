"""
Uses web scraping to extract the news on the front page while providing links directly to each piece of content.
Also formats the content and automatically emails it to self for viewing through email.

smtplib for authentication
used a task scheduler to automatically perform this once every morning without having to do anything.
"""

# http requests
import requests

# web scraping
from bs4 import BeautifulSoup

# sending mail
import smtplib

# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# system date and time manipulation
import datetime
now = datetime.datetime.now()

# email content placeholder

content = ''

# extracting Hacker News Stories





def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt += ('<b>HN Top Stories: </b>\n' + '<br>' + '-' * 50 + '<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class':'title','valign':''})) :
        cnt += ((str(i+1) + ' :: ' + tag.text + "\n" + '<br>')
        if tag.text != 'More' else '')
        # print(tag.prettify) # find all ('span'.attrs={'class':'sitestr'}))
    return (cnt)

cnt = extract_news('https://www.reddit.com/r/Kappa/')
content += cnt
content += ('<br>------<br>')
content += ('<br><br>End of Message')

# sending the email

print('Creating Email...')

# email details

SERVER = 'smtp.gmail.com' # smtp server
PORT = 587 # port number for google
FROM = 'email' # email id
TO = 'email' # self to email to self - can be a python list to send to multiple ppl
PASS = 'pw' # email's pw

# creating message body
# fp = open(file_name, 'rb')
# Create a text/plain message
# msg = MIMEText('')
msg = MIMEMultipart()

# msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
msg['Subject'] = 'Top News Stories HN [Automated Email' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
# fp.close()

print('Initializing Server...')

server = smtplib.SMTP(SERVER, PORT)
# server = smtplib.SMTP SSL ('stmp.gmail.com', 465)

server.set_debuglevel(1)
# set to 0 if you dont want to see error messages

server.ehlo()
server.starttls()
#server.ehlo
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass