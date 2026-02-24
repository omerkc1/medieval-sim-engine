from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import random
import os
import psycopg2

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

def simulate_day():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # günü al
    cur.execute("select current_day from world_state where id=1;")
    day = cur.fetchone()[0]

    # krallıkları çek
    cur.execute("select id, population, food_stock, stability from kingdoms;")
    kingdoms = cur.fetchall()

    for k in kingdoms:
        k_id, pop, food, stability = k

        births = int(pop * 0.02 / 365)
        deaths = int(pop * 0.01 / 365)

        pop += births - deaths

        food -= pop * 0.001

        if food < 0:
            stability -= 0.5

        cur.execute("""
        update kingdoms
        set population=%s, food_stock=%s, stability=%s
        where id=%s
        """, (pop, food, stability, k_id))

    day += 1
    cur.execute("update world_state set current_day=%s where id=1;", (day,))
    conn.commit()
    conn.close()

scheduler = BackgroundScheduler()
scheduler.add_job(simulate_day, 'interval', hours=24)
scheduler.start()

@app.get("/")
def read_root():
    return {"status": "Simulation running"}
