#Eklenecek: Çalıştırıcı değiştirebilecek
import os
import sys
import locale
import datetime
import time as t
import threading
import json
import importlib.util
from pathlib import Path
import getpass
try:
  import wget
except ModuleNotFoundError:
  print("Python 'wget' modülü bulunamdı. Bu yüzden komutlar indirilemeyecek.")

import shutil
from zipfile import ZipFile


def have(com):
  try:
    com
  except: return False

  return True
start=datetime.datetime.now()
v_path=os.getcwd()+"/vore"
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
      "007": "Komut Bulunamadı",
      "008": "Görev Yanıt vermiyor."
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

if not os.path.exists("config.json"):
  with open("config.json","w",encoding="utf8") as f:
    json.dump({"ilk":"ilk"},f)

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
[Bilgi] Kurulum Başlatılıyor...

Kurulum""")
    
        ad=str(input("Kullanıcı Adı:"))
        cihaz=str(input("Cihaz Adı:"))

        kul_json={"ad":ad,"cihaz":cihaz,"yetki":"exc"}

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
          with open(v_path+"/config.json","w",encoding="utf8") as f:
            json.dump(kul_json,f)
          
        except FileNotFoundError:
          Errors.error("001",f" config.json dosyası {os.getcwd()}konumunda bulunamdı")
        
        print("""Komut Kurulumu
        
        1) Komutları indir
        2) Komutları İndirme""")

        girdi=input("?")
        if girdi == "1":
          print("Komutlar İndiriliyor")

          wget.download("https://raw.githubusercontent.com/dios-project/VoreXp-depo/master/commands.zip","vore/commands/commands.zip")

          
          
          with ZipFile(v_path+'/commands/commands.zip') as fileobj:
            fileobj.extractall(os.getcwd()+"/vore/commands/")

          os.remove(v_path+"/commands/commands.zip")
        else:
          print("Kurulum Komutlar indirilmeden tamamlandı.")
          
          
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



vore_config={"runuser":"root","started":start,"platform":os.name,"vorepath":os.getcwd()+"/vore","commandspath": os.getcwd()+"/vore/commands/","lang":locale.getdefaultlocale()[0]}

sys.path.append(vore_config["commandspath"])
try:
  kul=int(input("kullanici>"))
except ValueError:
  print("Geçersiz Giriş!")
  sys.exit()
if kul in list(kullanicilar.keys()):
  vore_config["runuser"]=kullanicilar[kul]
else:
  print("User Not Found")
  sys.exit()
print(f"""Vore Xp 2022

Hoşgeldin, {vore_config["runuser"]}""")
os.chdir(vore_config["runuser"])
while True:
  try:
    command=input(">")
  except KeyboardInterrupt:
    print("Exited")
    sys.exit()

  try:
    if command.split()[0] == "vsp":
      try:
        file=command.split()[1]
      except IndexError:
        print("argument <file> required")
      if os.path.isfile(file):
        file_content=open(file,"r",encoding="utf8").read()
        line_count=file_content.count("\n")
        if line_count==0:
          line_count=1

        for i in range(line_count):
          satir=file_content.splitlines()
          try:
            if satir[i].split()[0]+".py" in os.listdir(vore_config["commandspath"]):
              args=satir[i].split()[1::]
              command_import=__import__(satir[i].split()[0])
              command_import.vore_config=vore_config
              try:
                command_import.command(args)
              except AttributeError:
                Errors.error("006","ilgili komutta ana fonksiyon bulunamadı.")
            else:
              Errors.error("007",f"komut '{satir[i].split()[0]}' bulunamadı")
          except IndexError:
            pass
  
    elif command=="service-reset":
      print("""VoreXp Servisi Sıfırlama Kaldırma Aracı

By işlemi Gerçekleştirmek istiyor musunuz? (Bütün Kullanıcılar ve komutlar silinecek)""")
      b=onay("evet, vorexp sıfırlansın","hayır, vorexp sıfırlanmasın")
      if b:
        shutil.rmtree(v_path)
        with open(v_path+"/config.json","r+",encoding="utf8") as f:
          f.seek(0)
          f.truncate()
          config["ilk"]="ilk"
          json.dump(config,f)
        sys.exit()
    elif command=="":
      pass
    else:
      try:
        if command.split()[0]+".py" in os.listdir(vore_config["commandspath"]):
          args=command.split()[1::]
          spec = importlib.util.spec_from_file_location("module.name", vore_config["commandspath"]+"/"+command.split()[0]+".py")
          command_import = importlib.util.module_from_spec(spec)
          spec.loader.exec_module(command_import)
          #command_import=__import__(command.split()[0])
          command_import.vore_config=vore_config
          try:
            command_import.command(args)
          except KeyboardInterrupt:
            pass
          except AttributeError as e:
            
            Errors.error("006","ilgili komutta ana fonksiyon bulunamadı veya komutta bir hata oluştu tip:AttributeError")
        else:
          Errors.error("007",f"komut '{command.split()[0]}' bulunamadı")
      except IndexError:
        pass
  except IndexError:
    pass
#Son satır XD