import sqlite3
DB = "passwords.db"


def initialize_db():
    """Initializes the table if not already done."""
    with sqlite3.connect(DB) as con:

        cursor = con.cursor()

        cursor.execute("CREATE TABLE if not exists secrets (id integer primary key, service_name text, username text, encrypted blob)")

        con.commit()


def add_password(service, username, pw):
    """Adds password to the database, if not already added.\n
    Parameters:\n
    service: The name of the service (e.g. "Google")\n
    username: The username belonging to given service\n
    pw: The password after encryption\n
    Returns false if password already exists, true if process was successful
    """

    with sqlite3.connect(DB) as con:
        cursor = con.cursor()

        #check if a password for given service and username already exists
        sql = "select * from secrets where service_name = ? and username = ?"
        cursor.execute(sql, (service, username))
        data = cursor.fetchone()
        if data:
            return False

        #no password exists for given service and username, we can add it to the table
        sql = "insert into secrets (service_name, username, encrypted) values (?, ?, ?)"
        data = (service, username, pw)


        cursor.execute(sql,data)

        #Save database before closing
        con.commit()
        return True


def get_password(service):
    """Fetches password from the database, if any password exists for given service.\n
    Returns the list of tuples, if no matching password is stored, an empty list will be returned."""

    with sqlite3.connect(DB) as con:
        cursor = con.cursor()

        sql = "select username, encrypted from secrets where service_name = ?"

        cursor.execute(sql, (service,))

        data = cursor.fetchall()
        return data

#with sqlite3.connect(DB) as con:
#    cursor = con.cursor()
#
#    cursor.execute("drop table secrets")
#
#    con.commit()