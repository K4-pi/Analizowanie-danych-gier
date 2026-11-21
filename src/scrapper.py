import sqlite3
import requests
import os
#https://store.steampowered.com/api/appdetails?appids=108600
#?include_dlc=true&include_software=true&include_videos=true&include_hardware=true

def start(api_key):
    print(f"scrapper ")

    conn = sqlite3.connect("../database/database.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS apps (
            appid INTEGER PRIMARY KEY,
            name TEXT
        )
        """)

    last_appid = conn.execute("""
        SELECT appid
        FROM apps
        ORDER BY appid DESC
        LIMIT 1;
        """) or 0

    while True:
        r = requests.get(
            "https://api.steampowered.com/IStoreService/GetAppList/v1/",
            params={"key": api_key, "last_appid": last_appid, "max_results": 50000},
            timeout=15,
        )
        r.raise_for_status()

        response_obj = r.json().get("response") or {}
        apps = response_obj.get("apps") or []

        # warunek przerwania
        if not apps:
            print("koniec scrappowania id")
            break

        rows = [
            (app.get("appid"), app.get("name"))
            for app in apps
            if app.get("appid") is not None
        ]

        with conn:
            conn.executemany("""
                INSERT INTO apps (appid, name)
                VALUES (?, ?)
            """, rows)

        last_appid = apps[-1]["appid"]
        print(f"last_appid={last_appid}")

    conn.close()

if __name__ == "__main__":
    start(os.getenv("STEAM_API_KEY"))