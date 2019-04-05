import datetime

x = datetime.datetime.now()
x = x.strftime("%x")
print(x)

products = open("products.txt", "a+")
date = input("Enter a date: ")
print(products.read())
products.close()

if date == x:
    print("Yes")
