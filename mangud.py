# Kirjuta pildil oleva asja nimi
import random
import json

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
  sonavara = loe_sonavara("sonavara.json")
  punktid = mangi_voor(sonavara, 5)
  print(f"Tulemus: {punktid}/5")
