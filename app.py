from flask import Flask, render_template, request, session, redirect, url_for
from mangud import (
    peida_sona, loe_valed_pakkumised, kas_voidetud,
    loe_sonavara, vali_kusimus, kontrolli_vastust,
)

app = Flask(__name__)
app.secret_key = "mingi-juhuslik-tekst-siia"

#  Menüü 
@app.route("/")
def menuu():
    return render_template("menuu.html")

# Kirjuta nimi 
@app.route("/nimi")
def nimi():
    if "nimi_kusimus" not in session:
        session["nimi_kusimus"] = vali_kusimus(loe_sonavara("sonavara.json"))
    return render_template(
        "kirjuta_nimi.html",
        kusimus=session["nimi_kusimus"],
        tulemus=session.pop("nimi_tulemus", None),
    )

@app.route("/nimi/vasta", methods=["POST"])

def nimi_vasta():
    kusimus = session.get("nimi_kusimus")
    if kusimus:
        oige = kontrolli_vastust(request.form["vastus"], kusimus["sona"])
        session["nimi_tulemus"] = {"oige": oige, "sona": kusimus["sona"]}
    return redirect(url_for("nimi"))

@app.route("/nimi/uus") #kustutab mängu info et saaks järgmisele lehele värske infoga minna
def nimi_uus():
    session.pop("nimi_kusimus", None)
    session.pop("nimi_tulemus", None)
    return redirect(url_for("nimi"))

# Hangman 
@app.route("/hangman")
def hangman():
    if "sona" not in session or "pilt" not in session: #AI
        kusimus = vali_kusimus(loe_sonavara("sonavara.json"))
        session["sona"] = kusimus["sona"]
        session["pilt"] = kusimus["pilt"]
        session["pakutud"] = []

    sona = session["sona"]
    pakutud = session["pakutud"]
    valesid = loe_valed_pakkumised(sona, pakutud)

    return render_template(
        "hangman.html",
        kusimus={"pilt": session["pilt"]},
        peidetud=peida_sona(sona, pakutud),
        alles=max(0, 6 - valesid),
        voit=kas_voidetud(sona, pakutud),
        kaotus=valesid >= 6,
        sona=sona,
        pakutud=pakutud,
    )

@app.route("/hangman/paku", methods=["POST"])
def hangman_paku():
    taht = request.form["taht"].strip().lower()
    if len(taht) == 1 and taht.isalpha() and taht not in session["pakutud"]:
        session["pakutud"] = session["pakutud"] + [taht]
    return redirect(url_for("hangman"))

@app.route("/hangman/uus")
def hangman_uus():
    session.pop("sona", None)
    session.pop("sona", None)
    session.pop("pilt", None)
    return redirect(url_for("hangman"))

# Teised lehed mida praegu veel pole
@app.route("/memory")
def memory():
    return render_template("memory.html")

@app.route("/uhendamine")
def uhendamine():
    return render_template("uhendamine.html")

if __name__ == "__main__":
    app.run(debug=True)