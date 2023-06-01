# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# database.py — связь кода Python с базой данных PhpMyAdmin

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import asyncio, random, datetime, aiomysql, re, time

loop = asyncio.get_event_loop()

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

USER = 'root'
PASSWORD = ''
HOST = 'localhost'
DATABASE = 'bot'

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

async def connect_base():  # Подключение к БД
    connected = await aiomysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        db=DATABASE,
        loop=loop
    )
    return connected

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# Регистрация аккаунта на проекте (обновлена в последний раз 08.05.2023)
async def registerNewAccaunt(user_id):  # Создание нового аккаунта в базе данных
    try:
        connection = await connect_base()
        async with connection.cursor() as cursor:
            VIP = ['no vip', 0]
            licenses = ['❌ Отсутствует', '❌ Отсутствует', '❌ Отсутствует', '❌ Отсутствует', '❌ Отсутствует', '❌ Отсутствует', '❌ Отсутствует', '❌ Отсутствует']
            cloths = ['Пусто', 'Пусто', 'Пусто', 'Пусто', 'Пусто', 'Пусто']
            passport = ['❌ Отсутствует', 0, 0]
            military_ticket = ['❌ Отсутствует', 0, 'Нету звания']
            admin_info = ['', '', '', '', '', '', '',  '', '']
            tester_info = ['', '', '', '', '']
            block_report = []
            block_account = []
            inventory = [0, 0, 0, 0, 0, 0, 0]
            new_user = f"INSERT INTO users (tg_id, tg_timeLastMessage, tg_MainMessage, tg_DeleteHelp, tg_answer, tg_Connected, state, nick, mail, lvl, exp, dollars, euro, yen, pounds, bank_dollars, bank_euro, bank_yen, bank_pounds, donate, admin, tester, licenses, cloths, family, fraction, passport, military_ticket, VIP, cars, houses, skills, temporary_int_var, temporary_text_var1, phone, report_wait, block_report, block_account, history_punish, history_nicks, inventory, admin_info, tester_info, age, sex, nationality, mailing_project, mailing_server, miniDesign, work, bank_card) VALUES ({user_id}, '{int(time.time())}', '0', '0', '0', '1', '', 'Не установлено', '❌ Не установлена', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', \"{licenses}\", \"{cloths}\", '-1', '-1', \"{passport}\", \"{military_ticket}\", \"{VIP}\", '[]', '[]', '[]', '0', '', '❌ Отсутствует', '0', \"{block_report}\", \"{block_account}\", '[]', '[]', \"{inventory}\", \"{admin_info}\", \"{tester_info}\", '0', 'Не выбран', 'Не выбрана', '❌ Не подписан', '❌ Не подписан', '0', '❌ Безработный', '❌ Нет банковской карты');"
            await cursor.execute(new_user)
            await connection.commit()
            connection.close()
            print(f'\033[38m[\033[33m!\033[38m][\033[33mDEBUG\033[38m] Встречайте нового пользователя')
            # [{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}]
    except Exception as ex:
        print(f'\033[38m[\033[31m!\033[38m][\033[33mDEBUG\033[38m] Не удалось создать пользователя, причина: {ex}')

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

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

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

async def deleteUserData(user_id):  # Удаление данных пользователя
    connection = await connect_base()
    async with connection.cursor() as cursor:
        delete_row = f"DELETE from `users` WHERE `tg_id` = {user_id}"
        await cursor.execute(delete_row)
        await connection.commit()
        connection.close()

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

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

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

async def yourSQL(sql):  # получение данных пользователя
    connection = await connect_base()
    async with connection.cursor() as cursor:
        select_row = f"{sql}"
        await cursor.execute(select_row)
        rows = await cursor.fetchall()
        connection.close()
    return rows

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

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

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

async def newDataInBase(table, keys, values):  # Новая строчка в базе данных
    try:
        connection = await connect_base()
        async with connection.cursor() as cursor:
            new_data = f"INSERT INTO `{table}` ({keys}) VALUES ({values})"
            await cursor.execute(new_data)
            await connection.commit()
            connection.close()
    except Exception as ex:
        print(f'\033[38m[\033[31m!\033[38m][\033[33mDEBUG\033[38m] Произошла ошибка в базе данных: {ex}')


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# Весь код ниже не относится к вазимодействию кода с БД, однако также выполняют важную роль и много где используются.

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————


async def exitBot():  # делает выход из активной переписки
    return
    # try:
    #     exit(0)
    # except:
    #     pass


async def pretty(num):
    num1 = re.sub(r'\d(?=(?:\d{3})+(?!\d))', r'\g<0> ', str(num))
    return num1