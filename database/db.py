from app import dp, bot
import datetime
from config import admin_id
import psycopg2

conn = psycopg2.connect(dbname='green_atom', user='postgres', password="12345", host="localhost")
cur = conn.cursor()


async def user_exists(message) -> bool:
    try:
        cur.execute("select exists(select * from users where id=%s)", (str(message.from_user.id),))
        return cur.fetchone()[0]
    except Exception as e:
        print(e, "db 15")


async def get_user_info(message) -> tuple:
    try:
        cur.execute("select * from users where id=%s", (str(message.from_user.id), ))
        return cur.fetchall()[0]
    except Exception as e:
        print(e, "db 23")


async def user_create(message) -> None:
    try:
        if message.from_user.id not in admin_id:
            status = "user"
        else:
            status = "admin"

        cur.execute("insert into users values(%s, %s, %s, %s, %s)", (str(message.from_user.id), status, 0, "", 0))
        conn.commit()
    except Exception as e:
        print(e, "db, 36")


async def update_referals(slave_id, master_id) -> None:
    #  Берем текущий список id рефералов юзера, который пригласи
    if str(master_id) != str(slave_id):
        cur.execute("select exists(select id from users where id=%s)", (str(master_id),))
        if cur.fetchone()[0]:
            cur.execute("select referals, green_cash from users where id=%s", (str(master_id),))
            result = cur.fetchall()[0]
            print(result)
            refs = result[0] + 1
            coins = result[1] + 5
            cur.execute("update users set referals=%s, green_cash=%s where id=%s", (refs, coins, str(master_id)))
            conn.commit()


async def save_question(user_id, sms) -> None:
    try:
        cur.execute("insert into mail values(%s, %s)", (str(user_id), str(sms)))
        conn.commit()
    except Exception as e:
        print(e)


async def is_ban(user_id) -> bool:
    try:
        cur.execute("select exists(select id from bans where id=%s)", (str(user_id)))
        return cur.fetchone()[0]
    except Exception as e:
        print(e)


async def get_sms(count) -> list:
    cur.execute("select * from mail limit %s", (count, ))
    return cur.fetchall()


async def ban_user(user_id) -> None:
    if not await is_ban(user_id):
        cur.execute("insert into bans values(%s)", (str(user_id),))
        conn.commit()