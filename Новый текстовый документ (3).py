from urllib import request
print("Введите ссылку сайта по которому будем искать:")
url = input()
otvet = request.urlopen(url)
print("Введите что будем искать:")
vera = input()

for line in otvet:
    print(line)
    if vera in str(line):
        print("ВОТ ОНО ТУТ ЕСТЬ")
        break
else:
    print("Нет такого на сайте")

kk=1
while kk:
    escape = input("Выйти?(y/n)")
    if escape == "y":
        kk=0
    elif escape =="n":
        kk=1
    else: print("Введите \"y\" или \"n\"")

    
