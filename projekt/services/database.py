import sqlite3
from datetime import datetime


class Database:


    def __init__(self):

        self.connection = sqlite3.connect(
            "data/decisions.db",
            check_same_thread=False
        )

        self.create_table()



    def create_table(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS decisions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                moderator TEXT,

                question TEXT,

                response TEXT,

                date TEXT

            )
            """
        )

        self.connection.commit()



    def save_decision(
        self,
        moderator,
        question,
        response
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO decisions
            (
                moderator,
                question,
                response,
                date
            )

            VALUES (?, ?, ?, ?)

            """,

            (
                moderator,
                question,
                response,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )

        self.connection.commit()



    def get_history(
        self,
        limit=5,
        page=1
    ):

        offset = (page - 1) * limit


        cursor = self.connection.cursor()


        cursor.execute(
            """
            SELECT
                id,
                moderator,
                question,
                response,
                date

            FROM decisions

            ORDER BY id DESC

            LIMIT ?
            OFFSET ?

            """,

            (
                limit,
                offset
            )
        )


        return cursor.fetchall()



    def search_history(
        self,
        text,
        limit=5
    ):

        cursor = self.connection.cursor()


        cursor.execute(
            """
            SELECT
                id,
                moderator,
                question,
                response,
                date

            FROM decisions

            WHERE question LIKE ?

            ORDER BY id DESC

            LIMIT ?

            """,

            (
                f"%{text}%",
                limit
            )
        )


        return cursor.fetchall()



    def close(self):

        self.connection.close()