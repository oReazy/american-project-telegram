import asyncio
import json, re
import random, datetime

import aiomysql

loop = asyncio.get_event_loop()

# ---------------------------------------------------------------------------------------

USER = 'oreazyic_bot'
PASSWORD = 'Cloud9d'
HOST = 'oreazyic.beget.tech'
DATABASE = 'oreazyic_bot'

# ---------------------------------------------------------------------------------------

async def connect_base():  # Подключение к БД
    connected = await aiomysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        db=DATABASE,
        loop=loop
    )
    return connected



async def registerNewAccaunt(user_id):  # Создание нового аккаунта в базе данных
    try:
        connection = await connect_base()
        async with connection.cursor() as cursor:
            new_user = "INSERT INTO `users` (tg_id, tg_main_message, state, is_answer, is_connected, nick, mail, lvl, exp) VALUES " \
                       f"({user_id}, " \
                       f"'0', " \
                       f"'registration_1_check', " \
                       f"'0', " \
                       f"'0', " \
                       f"'Не установлен', " \
                       f"'Не установлена', " \
                       f"'1', " \
                       f"'0'" \
                       f")"
            await cursor.execute(new_user)
            await connection.commit()
            connection.close()
            print(f'\033[38m[\033[33m!\033[38m][\033[33mDEBUG\033[38m] Встречайте нового пользователя')
            # [{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}]
    except Exception as ex:
        print(f'\033[38m[\033[31m!\033[38m][\033[33mDEBUG\033[38m] Не удалось создать пользователя, причина: {ex}')



async def getUserData(user_id):  # получение данных пользователя
    connection = await connect_base()
    async with connection.cursor() as cursor:
        select_row = f"SELECT * FROM `users` WHERE `tg_id` = {user_id}"
        await cursor.execute(select_row)
        rows = await cursor.fetchall()
        for row in rows:
            data = row
        connection.close()
    return data


async def setUserData(user_id, key, value):  # Изменение переменных у пользователя (по одной переменной)
    connection = await connect_base()
    async with connection.cursor() as cursor:
        update_row = f"UPDATE `users` SET {key} = {value} WHERE tg_id = {user_id}"
        await cursor.execute(update_row)
        await connection.commit()
        connection.close()


async def setMultiUserData(user_id, value):  # Изменение переменных у пользователя (несколько переменных)
    connection = await connect_base()
    async with connection.cursor() as cursor:
        update_row = f"UPDATE `users` SET {value} WHERE tg_id = {user_id}"
        await cursor.execute(update_row)
        await connection.commit()
        connection.close()


async def deleteUserData(user_id):  # Удаление данных пользователя
    connection = await connect_base()
    async with connection.cursor() as cursor:
        delete_row = f"DELETE from `users` WHERE `tg_id` = {user_id}"
        await cursor.execute(delete_row)
        await connection.commit()
        connection.close()


async def findBaseData(key, value):  # найти значения в базе данных. Выводит их количестве в БД
    count_row = 0
    connection = await connect_base()
    async with connection.cursor() as cursor:
        select_row = f"SELECT * FROM `users` WHERE `{key}` = {value}"
        await cursor.execute(select_row)
        rows = await cursor.fetchall()
        for row in rows:
            count_row = count_row + 1
        connection.close()
    return count_row




async def findBaseDataSetting(table, where_key, where_value):  # найти значения в базе данных. Выводит их количестве в БД
    count_row = 0
    connection = await connect_base()
    async with connection.cursor() as cursor:
        select_row = f"SELECT * FROM `{table}` WHERE `{where_key}` = {where_value}"
        await cursor.execute(select_row)
        rows = await cursor.fetchall()
        for row in rows:
            count_row = count_row + 1
        connection.close()
    return count_row



async def yourSQL(sql):  # получение данных пользователя
    connection = await connect_base()
    async with connection.cursor() as cursor:
        select_row = f"{sql}"
        await cursor.execute(select_row)
        rows = await cursor.fetchall()
        connection.close()
    return rows


# --------------------------------------------------------------------------------------------------

async def getBdData(table, key, value):  # получение данных (выводит только последнее)
    connection = await connect_base()
    async with connection.cursor() as cursor:
        select_row = f"SELECT * FROM `{table}` WHERE {key} = {value}"
        await cursor.execute(select_row)
        rows = await cursor.fetchall()
        for row in rows:
            data = row
        connection.close()
    return data


async def getMultiBdData(table, key, value):  # получение данных (выводит все)
    connection = await connect_base()
    async with connection.cursor() as cursor:
        select_row = f"SELECT * FROM `{table}` WHERE {key} = {value}"
        await cursor.execute(select_row)
        rows = await cursor.fetchall()
        connection.close()
    return rows


async def getMultiProgramBdData(table, where):  # получение данных (программное)
    connection = await connect_base()
    async with connection.cursor() as cursor:
        select_row = f"SELECT * FROM `{table}` WHERE {where}"
        await cursor.execute(select_row)
        rows = await cursor.fetchall()
        connection.close()
    return rows


async def setBdData(table, where_key, where_value, key, value):  # Изменение переменных (по одной переменной)
    connection = await connect_base()
    async with connection.cursor() as cursor:
        update_row = f"UPDATE `{table}` SET {key} = {value} WHERE {where_key} = {where_value}"
        await cursor.execute(update_row)
        await connection.commit()
        connection.close()


async def setMultiDbData(table, where_key, where_value, value):  # Изменение переменных (несколько переменных)
    connection = await connect_base()
    async with connection.cursor() as cursor:
        update_row = f"UPDATE `{table}` SET {value} WHERE {where_key} = {where_value}"
        await cursor.execute(update_row)
        await connection.commit()
        connection.close()


async def addMultiBdData(table, keys, values):  # Изменение переменных (по одной переменной)
    connection = await connect_base()
    async with connection.cursor() as cursor:
        update_row = f"INSERT INTO `{table}` ({keys}) VALUES ({values})"
        await cursor.execute(update_row)
        await connection.commit()
        connection.close()