import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS USERS (
        ID SERIAL PRIMARY KEY,
        IS_ORGANIZATION BOOLEAN DEFAULT FALSE,
        IS_ADMIN BOOLEAN DEFAULT FALSE,
        USERNAME VARCHAR(50) UNIQUE NOT NULL,
        FIRSTNAME VARCHAR(50) NOT NULL,
        LASTNAME VARCHAR(50) NOT NULL,
        EMAIL VARCHAR(100) UNIQUE NOT NULL,
        PASSWORD VARCHAR(100) UNIQUE NOT NULL,
        IMG_ID INTEGER REFERENCES IMAGES(ID) ON DELETE SET NULL,
        DATE_CREATED DATE DEFAULT CURRENT_DATE,
        DATE_UPDATED DATE DEFAULT CURRENT_DATE
    )
    """,
    """CREATE TABLE IF NOT EXISTS ADDRESSES (
        ID SERIAL PRIMARY KEY,
        DISTINCTS VARCHAR(100) NOT NULL,
        STREET VARCHAR(100) NOT NULL,
        NO VARCHAR(100) NOT NULL,
        CITY VARCHAR(100) NOT NULL,
        COUNTRY VARCHAR(100) NOT NULL,
        DATE_CREATED DATE DEFAULT CURRENT_DATE,
        DATE_UPDATED DATE DEFAULT CURRENT_DATE
    )
    """,
    """CREATE TABLE IF NOT EXISTS EVENTTYPES (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(100) UNIQUE NOT NULL,
        INFORMATION VARCHAR(200),
        EVENT_COUNTER INTEGER,
        DATE_CREATED DATE DEFAULT CURRENT_DATE,
        DATE_UPDATED DATE DEFAULT CURRENT_DATE
    )
    """,
    """CREATE TABLE IF NOT EXISTS EVALUATION (
        ID SERIAL PRIMARY KEY,
        USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE,
        EVENT_ID INTEGER REFERENCES EVENTS(ID) ON DELETE CASCADE,
        RATE INTEGER CHECK (RATE > 1 AND RATE < 10),
        DATE_CREATED DATE DEFAULT CURRENT_DATE,
        DATE_UPDATED DATE DEFAULT CURRENT_DATE
    )
    """,
     """CREATE TABLE IF NOT EXISTS IMAGES (
        ID SERIAL PRIMARY KEY,
        FILENAME VARCHAR(100) NOT NULL,
        EXTENSION VARCHAR(20) NOT NULL,
        DATA BYTEA NOT NULL,
        DATE_CREATED DATE DEFAULT CURRENT_DATE,
        DATE_UPDATED DATE DEFAULT CURRENT_DATE
    )
    """,
    """CREATE TABLE IF NOT EXISTS EVENTS (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(200) NOT NULL,
        IS_PRIVATE BOOLEAN NOT NULL,
        ADDRESS INTEGER REFERENCES ADDRESSES(ID) ON DELETE CASCADE,
        TYPE VARCHAR(200) NOT NULL,
        CREATOR INTEGER REFERENCES USERS(ID) ON DELETE CASCADE,
        DATE DATE NOT NULL,
        PLACE INTEGER REFERENCES PLACES(ID) ON DELETE CASCADE,
        IMG_ID INTEGER REFERENCES IMAGES(ID) ON DELETE SET NULL,
        DATE_CREATED DATE DEFAULT CURRENT_DATE,
        DATE_UPDATED DATE DEFAULT CURRENT_DATE
    )
    """,
    """CREATE TABLE IF NOT EXISTS USEREVENTS (
        ID SERIAL PRIMARY KEY,
        USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE,
        EVENT_ID INTEGER REFERENCES EVENTS(ID) ON DELETE CASCADE,
        NOTE VARCHAR(200),
        IS_IMPORTANT BOOLEAN DEFAULT FALSE,
        ATTEND_STATUS BOOLEAN DEFAULT FALSE,
        DATE_CREATED DATE DEFAULT CURRENT_DATE,
        DATE_UPDATED DATE DEFAULT CURRENT_DATE
    )
    """,
    """CREATE TABLE IF NOT EXISTS EVENTATTENDSTATUSES (
        ID SERIAL PRIMARY KEY,
        USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE,
        EVENT INTEGER REFERENCES EVENTS(ID) ON DELETE CASCADE,
        WILL_ATTEND BOOLEAN,
        DATE_CREATED DATE DEFAULT CURRENT_DATE,
        DATE_UPDATED DATE DEFAULT CURRENT_DATE
    )
    """,
    """CREATE TABLE IF NOT EXISTS COMMENTS (
        ID SERIAL PRIMARY KEY,
        USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE,
        EVENT_ID INTEGER REFERENCES EVENTS(ID) ON DELETE CASCADE,
        CONTEXT VARCHAR(500),
        IS_ATTENDED BOOLEAN DEFAULT FALSE,
        IS_SPOILER BOOLEAN DEFAULT FALSE,
        DATE_CREATED DATE DEFAULT CURRENT_DATE,
        DATE_UPDATED DATE DEFAULT CURRENT_DATE
    )
    """,
    """CREATE TABLE IF NOT EXISTS ORGANIZATIONS (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(100),
        ADDRESS INTEGER REFERENCES ADDRESSES(ID) ON DELETE CASCADE,
        EVENT INTEGER REFERENCES EVENTS(ID) ON DELETE CASCADE,
        RATE NUMERIC(3,1),
        INFORMATION VARCHAR(500),
        IMG_ID INTEGER REFERENCES IMAGES(ID) ON DELETE SET NULL,
        DATE_CREATED DATE DEFAULT CURRENT_DATE,
        DATE_UPDATED DATE DEFAULT CURRENT_DATE
    )
    """,
    """CREATE TABLE IF NOT EXISTS PLACES (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(100),
        ADDRESS INTEGER REFERENCES ADDRESSES(ID) ON DELETE CASCADE,
        TYPE VARCHAR(50),
        CAPACITY INTEGER,
        CREATOR INTEGER REFERENCES USERS(ID) ON DELETE CASCADE,
        DATE_CREATED DATE DEFAULT CURRENT_DATE,
        DATE_UPDATED DATE DEFAULT CURRENT_DATE
    )
    """
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
