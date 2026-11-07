import random
import json

# Hangman
def peida_sona(sona, pakutud_tahed):
  loend = []
  for taht in sona:
    if taht in pakutud_tahed:
      loend.append(taht)
    else:
      loend.append("_")
  sone = " ".join(loend)
  return sone

def loe_valed_pakkumised(sona, pakutud_tahed):
  valed = []
  for taht in pakutud_tahed:
    if taht not in sona:
      valed.append(taht)
  return len(valed)

def kas_voidetud(sona, pakutud_tahed):
  for taht in sona:
    if taht not in pakutud_tahed:
      return False
  return True

def mangi_hangman(sona):
  pakutud_tahed = []
  lubatud_vead = 6
  while True:
    if loe_valed_pakkumised(sona, pakutud_tahed) >= lubatud_vead:
      print(f"Kahjuks kaotasid! Õige sõna oli: {sona}")
      break
    print(peida_sona(sona, pakutud_tahed))
    print("Eksimisvõimalusi alles:", lubatud_vead - loe_valed_pakkumised(sona, pakutud_tahed))
    taht = input("Sisesta üks täht: ").strip().lower()
    if taht in pakutud_tahed:
      print("Oled selle tähe juba pakkunud.")
      continue
    if len(taht) != 1 or not taht.isalpha():
      print("Palun sisesta ainult üks täht.")
      continue
    pakutud_tahed.append(taht)
    if kas_voidetud(sona, pakutud_tahed):
      print(f"Õige! Sõna oli: {sona}")
      break


# Kirjuta pildil oleva asja nimi

def loe_sonavara(failinimi):
  with open(failinimi, encoding='utf-8') as f:
    return json.load(f)

def kontrolli_vastust(vastus, oige_sona):
  if vastus.strip().lower() == oige_sona:
    return True
  else:
    return False

def vali_kusimus(sonavara):
  return random.choice(sonavara)

def mangi_voor(sonavara, kusimuste_arv):
  punktid = 0
  for k in range(kusimuste_arv):
    kusimus = vali_kusimus(sonavara)
    vastus = input(f"Mis on sellel pildil: {kusimus['pilt']}? ")
    if kontrolli_vastust(vastus, kusimus["sona"]):
      punktid += 1
      print("Õige!")
    else:
      print(f"Vale! Õige vastus on: {kusimus['sona']}")
  return punktid

if __name__ == "__main__":
  kusimus = vali_kusimus(loe_sonavara("sonavara.json"))
  mangi_hangman(kusimus["sona"])
