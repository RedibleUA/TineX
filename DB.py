import psycopg2
import random
from config import host, user, password, db_name


def RandomSticker(Category: str):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT MAX(\"ID\") FROM public.\"Stickers\" where \"Category\" = '{Category}'"
        )

        rows = cursor.fetchall()
        for r in rows:
            maxCount = r[0]

        dice = random.randint(1, maxCount)

        cursor.execute(
            f"SELECT \"URL\" FROM public.\"Stickers\" where \"Category\" = '{Category}' and \"ID\" = '{dice}'"
        )

        rows = cursor.fetchall()
        for r in rows:
            sricker = r[0]


    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return sricker


def StickerCheck(URL: str):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT count(*) FROM public.\"Stickers\" where \"URL\" = '{URL}'"
        )

        rows = cursor.fetchall()
        for r in rows:
            count = r[0]

        exist = False
        if (count > 0):
            exist = True

        cursor.execute(
            f"SELECT count(*) FROM public.\"Stickers ADD\" where \"URL\" = '{URL}'"
        )

        rows = cursor.fetchall()
        for r in rows:
            count = r[0]

        if (count > 0):
            exist = True

    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return exist


def StickerRead():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT count(*) FROM public.\"Stickers ADD\""
        )

        rows = cursor.fetchall()
        for r in rows:
            count = r[0]

        exist = False
        if (count > 0):
            exist = True

    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return exist


def StickerInsert(Category: str, URL: str):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(f"DO $do$ BEGIN if EXISTS (SELECT FROM public.\"Stickers ADD\") THEN INSERT INTO public.\"Stickers ADD\"(\"Category\", \"ID\", \"URL\", \"TakenBy\") VALUES('{Category}', (SELECT MAX(\"ID\") FROM public.\"Stickers ADD\") + 1, '{URL}', null); ELSE INSERT INTO public.\"Stickers ADD\"(\"Category\", \"ID\", \"URL\", \"TakenBy\") VALUES('{Category}', 1, '{URL}', null); END IF; END $do$")
        connection.commit()

    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()


def StickerAdd(Category: str, StikerURL: str):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        count = 1
        answer = ''

        if (StickerCheck(StikerURL) == False):
            StickerInsert(Category, StikerURL)
            answer = "Done"
        else:
            answer = "Already exists"


    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return answer
