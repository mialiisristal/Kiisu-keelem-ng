# Kiisu keelemäng
# Mia-Liis Ristal ja Sheril Chrislyn Saar
# Kasutaja saab mängida kahte erinevat mängu: Hangman ja Pildimäng. Hangmanis peab kasutaja tähti pakkudes ära arvama sõna. Pildimängus peab kasutaja ära arvama, mis on pildil.
# sonavara.json peab olema samas kaustas, pildimäng kuvab praegu ainult pildifaili nime, mitte pilte, kuna pildid praegu puuduvad.

import random
import json

# Hangman
def peida_sona(sona, pakutud_tahed):
  """Tagastab sõne, kus pakkumata tähed on asendatud alakriipsudega."""
  loend = []
  for taht in sona:
    if taht in pakutud_tahed:
      loend.append(taht)
    else:
      loend.append("_")
  sone = " ".join(loend)
  return sone

def loe_valed_pakkumised(sona, pakutud_tahed):
  """Tagastab valede pakkumiste arvu."""
  valed = []
  for taht in pakutud_tahed:
    if taht not in sona:
      valed.append(taht)
  return len(valed)

def kas_voidetud(sona, pakutud_tahed):
  """Tagastab True, kui sõna on ära arvatud, muidu False."""
  for taht in sona:
    if taht not in pakutud_tahed:
      return False
  return True

def mangi_hangman(sona):
  """Käivitab Hangmani mängu terminalis."""
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


# Pildimäng
def loe_sonavara(failinimi):
  """Tagastab sõnavara, mis on salvestatud JSON-failis."""
  with open(failinimi, encoding='utf-8') as f:
    return json.load(f)

def kontrolli_vastust(vastus, oige_sona):
  """Tagastab True, kui vastus on õige, muidu False."""
  if vastus.strip().lower() == oige_sona:
    return True
  else:
    return False

def vali_kusimus(sonavara):
  """Valib juhusliku küsimuse sõnavarast."""
  return random.choice(sonavara)

def mangi_voor(sonavara, kusimuste_arv):
  """Käivitab pildimängu vooru terminalis, tagastab punktisumma."""
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
  sonavara = loe_sonavara("sonavara.json")
  while True:
    print("1. Hangman")
    print("2. Pildimäng")
    print("0. Välju")
    valik = input("Vali mäng: ").strip()
    if valik == "1":
        sona = random.choice(sonavara)["sona"]
        mangi_hangman(sona)
    elif valik == "2":
        punktid = mangi_voor(sonavara, 5)
        print(f"Said {punktid}/5 punkti.")
    elif valik == "0":
        break
    else:
        print("Palun vali 1, 2 või 0.")
