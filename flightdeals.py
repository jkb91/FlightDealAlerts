import re, requests, bs4, smtplib

destinations = ['London', 'Austin'] # destinations of interest
url = 'http://www.theflightdeal.com/category/flight-deals/sfo' # flying out of SFO
page = requests.get(url).text
soup = bs4.BeautifulSoup(page, 'html.parser')
results = soup.select('div > div > h1 > a')
titleRegex = re.compile(r'Permanent Link:(.*?)">')  # text of offer
res = titleRegex.findall(str(results))
offers = [res[0], res[1], res[2]]             # extracts 3 most recent offers
priceRegex = re.compile(r'\d+')               # check price
price = priceRegex.findall(str(res[0]))      
price = int(price[0])
alert = ""


def send_email(text):
    text = """"
From: myflightdealalerts@gmail.com
Subject: Deal Alert!

{0} """.format(text.encode('utf-8'))  # have to encode
    
    server = smtplib.SMTP_SSL('smtp.gmail.com') # connect to gmail
    server.login('myflightdealalerts', 'takeflight123') # login to gmail
    server.sendmail("myflightdealalerts@gmail.com", "JoshuaBrown91@gmail.com", text)  # [sender, receiver, msg]
    
for offer in offers:    # checks price and destinations of recent 3 offers
    price = priceRegex.findall(str(offer))
    price = int(price[0])
    if int(price) <= 150:
        p_alert = """ Cheap Price Alert!!: {0} """.format(offer) + (" "*250) # trouble with incorporatng newlines since it gets encoded
        alert += p_alert + "\n"
    for dest in destinations:
        if dest in offer:
            d_alert = """Preferred destination available:{0} """ .format(dest) + (" "*300)
            alert += d_alert + "\n"
if len(alert) > 1: # if there is an alert, send the email
    send_email(alert)

