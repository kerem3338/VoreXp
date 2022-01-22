import os
import sys
import datetime
import time
import threading
import json
from pathlib import Path
import getpass
import wget
from zipfile import ZipFile
start=datetime.datetime.now()

class Tasks:
  def __init__(self):
    self._tasks={}
  def new_task(self,taskname):
    self._tasks[taskname]={"runner":getpass.getuser()}
  def tasks(self):
    return self._tasks
class Errors:
  def __init__(self):
    self._errors={
      "001":"Dosya Bulunumadı",
      "002": "Klasör Bulunamdı",
      "003": "Dosya Zaten Var",
      "004": "Klasör Zaten Var",
      "005": "Argüman Hatası",
      "006": "Komut fonksiyonu bulunamadı",
      "007": "Komut Bulunamadı"
    }

  def error(self,errcode,message="",err=None):
    if errcode in self._errors:
      if err is None:
        print(f"Error Code:({errcode}): {message}")
      if err is True:
        print(f"Error Code:({errcode}): {self._errors[errcode]}")
    else:
      print("Error!")

def onay(evet,hayir):
  onay=input(f"({evet}/{hayir})")
  if onay == evet:
    return True
  elif onay == hayir:
    return False
  else:
    return None
Errors=Errors()
Tasks=Tasks()
try:
  with open("config.json","r+") as f:
    config=json.load(f)
    try:
      if config["ilk"] == "ilk":
        f.seek(0)
        f.truncate()
        config["ilk"]="no"
        json.dump(config,f)
        print("""Vore Xp 2022
[Bilgi] İlk giriş tespit edildi

Kurulum)""")
    
        ad=str(input("Kullanıcı Adı:"))
        cihaz=str(input("Cihaz Adı:"))

        kul_json={"ad":ad,"cihaz":cihaz}

        if os.path.isdir(os.getcwd()+"/vore"):
          Errors.error("004", "Vore Klasörü Zaten Bulunuyor")
          print("Vore Klasörü silinerek İşleme Devam edilsin mi? (kullanıcılar ile ilgili bütün veriler silinir)")

          b=onay(evet="evet, onaylıyorum",hayir="hayir, onaylamıyorum")
          if b:
            if os.name=="nt":
              os.system("rmdir /s /q vore")
            else:
              os.system("rm -rf vore")
        if os.name=="nt":
          #os.system("cd "+ os.getcwd())
          os.system(f"mkdir vore && nul>vore/config.json && mkdir vore/users && mkdir vore/users/{ad}")
        else:
          #os.system("cd "+ os.getcwd())
          os.system(f"mkdir vore && touch vore/config.json && mkdir vore/users && mkdir vore/users/{ad} && mkdir vore/commands")
        
        try:
          with open("vore/config.json","w",encoding="utf8") as f:
            json.dump(kul_json,f)
          
        except FileNotFoundError:
          Errors.error("001",f" config.json dosyası {os.getcwd()}konumunda bulunamdı")
        
        print("""Komut Kurulumu
        
        1) Komutları indir
        2) Komutları İndirme""")

        girdi=input("?")
        if girdi == "1":
          print("Komutlar İndiriliyor")

          wget.download("https://raw.githubusercontent.com/dios-project/joker/master/komutlar.zip","vore/commands/commands.zip")

          
          
          with ZipFile('vore/commands/commands.zip') as fileobj:
            fileobj.extractall(os.getcwd()+"/vore/commands/")
          
          
          os.remove("vore/commands/commands.zip")
    except KeyError:
      pass
    
    
except FileNotFoundError as e:
  print(e)
  Errors.error("001",f" config.json dosyası {os.getcwd()} konumunda bulunamdı")

print("""Vore Xp 2022
Kullanıcı Girişi

Kullanıcılar""")
kullanicilar={}

try:
  p = Path(os.getcwd() + '/vore/users')
  p=[f for f in p.iterdir() if f.is_dir()]
except FileNotFoundError:
  Errors.error("002",f"vore/users Klasörü bulunamadı")

for x in range(len(p)):
  kullanicilar[x]=str(p[x])

kullanicilar_list=list(kullanicilar)
for x in range(len(kullanicilar_list)):
  print(f"{x}:{kullanicilar[x]}")



vore_config={"runuser":"root","started":start,"platform":os.name}
try:
  kul=int(input("kullanici>"))
except ValueError:
  print("Sadece sayı giriniz.")
  sys.exit()
if kul in list(kullanicilar.keys()):
  vore_config["runuser"]=kullanicilar[kul]
else:
  print("User Not Found")
print(f"""Vore Xp 2022

Hoşgeldin, {vore_config["runuser"]}""")

while True:
  try:
    command=input(">")
  except KeyboardInterrupt:
    print("Exited")
    sys.exit()
  
  if command=="":
    pass
  
  try:
    if command.split()[0]+".py" in os.listdir("vore/commands/"):
      args=command.split()[1::]
      sys.path.append("vore/commands")
      command_import=__import__(command.split()[0])
      command_import.vore_config=vore_config
      try:
        command_import.command(args)
      except AttributeError:
        Errors.error("006","ilgili komutta ana fonksiyon bulunamadı.")
    else:
      Errors.error("007",f"komut '{command.split()[0]}' bulunamadı")
  except IndexError:
    pass
