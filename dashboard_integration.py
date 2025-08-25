import os
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template

# Load Firebase
cred = credentials.Certificate("firebase_credentials.json")  # Place your Firebase JSON here
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

@app.route("/")
def index():
    bots_stats = {}
    # List of your bot collection names in Firebase
    bot_collections = [
        "MexiceGOd_Bot", "Eyesteb_bot", "EyeOfTheVault_bot",
        "Chronos_Bot", "Icehunter_Bot", "IceGodWatcher_Bot",
        "icegodstracker_bot", "ScamSweeper_bot", "MEX_Tracker_Bot",
        "ChinoSecureBot", "IceGodsBoost_Bot", "MEX_ProtectorBot",
        "ICEBOYSIBS_bot", "Mex_fixer_bot", "PhoenixReign_bot",
        "ICEGODS_value_bot", "ICEHack_Bot", "PhoenixReign_bot_2",
        "Mex_Sub_BoT", "Ice_ChainPilot_bot", "IcegodsEchoEyes_bot",
        "IcegodsVaultEyes_bot", "IcegodsPulseEyes_bot", "Icegods_vier_bot",
        "IceGodssecurityfocused_bot", "IcegodsBridgeEyes_bot", "trial_checker_bot"
    ]

    for bot_name in bot_collections:
        users_ref = db.collection("telegram_users").where("bot_name", "==", bot_name)
        users = list(users_ref.stream())
        bots_stats[bot_name] = len(users)

    return render_template("dashboard.html", bots_stats=bots_stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
