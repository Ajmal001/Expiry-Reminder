import datetime
import os
import smtplib

def convert_to_days(new_date):# Conversion of date to no of days since 1 Jan of that year
    n = 0
    month = int(new_date[0:2])
    day = int(new_date[3:5])
    year = int(new_date[6:8])
    if month == 1:
        n = day
    elif month == 2:
        n = 31 + day
    elif month == 3:
        n = 59 + day
    elif month == 4:
        n = 90 + day
    elif month == 5:
        n = 120 + day
    elif month == 6:
        n = 151 + day
    elif month == 7:
        n = 181 + day
    elif month == 8:
        n = 212 + day
    elif month == 9:
        n = 242 + day
    elif month == 10:
        n = 272 + day
    elif month == 11:
        n = 303 + day
    elif month == 12:
        n = 334 + day
    return n, year


x = datetime.datetime.now()
day1 = x.strftime("%x")
day1 = str(day1)
li = ["expiry.informer@gmail.com"]

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login("expiry.informer@gmail.com", "Simplepassword")

with open("products.txt") as products:
    for line in products:
        date = line[0:8]
        name = line[9:-1]
        today, year1 = convert_to_days(day1)
        good, year2 = convert_to_days(date)
        fo = open("new.txt", 'a')
        if year1 == year2:
            diff = good - today
            if diff >= 1:
                fo.write(line)
                if diff <= 7 and diff >= 0:
                    body = name + " expires on " + date + "."
                    s.sendmail(li, "maninderk06@hotmail.com", body)
        else:
            good = good + 365
            diff = good - today
            if diff >= 1:
                fo.write(line)
                if diff <= 7 and diff >= 0:
                    body = name + " expires on " + date + "."
                    s.sendmail(li, "maninderk06@hotmail.com", body)
                    if diff >= 1:
                        fo.write(line)

s.quit()
products.close()
fo.close()
os.remove("products.txt")
os.rename("new.txt", "products.txt")
