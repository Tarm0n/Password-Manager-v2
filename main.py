import secrets
import sqlite3
import string
import getpass
import pyperclip
import db_manager as db
import crypto_manager as crypto

session_pw = None
print("---------------------------------------")
print("Welcome to your local password manager!")
print("---------------------------------------\n\n")

# check if table exists, if not, then this is the first login
with sqlite3.connect(db.DB) as con:
    cursor = con.cursor()

    sql = "select count(*) from sqlite_master where type = 'table' and name = 'secrets'"

    cursor.execute(sql)
    response = cursor.fetchone()[0]
    print(response)

    con.close()

#this is the first login
if response == 0:
    db.initialize_db()

    master_password = getpass.getpass("Please input your Master Password: ")

    encrypted = crypto.encrypt(master_password, "VALID")
    db.add_password("login", "canary", encrypted)

    session_pw = master_password

# this is not the first login
while session_pw is None:
    master_password = getpass.getpass("Please input your Master Password: ")
    result = db.get_password("login")[0]
    decrypted = crypto.decrypt(master_password, result[1])

    if decrypted is None:
        print("Your Master Password is wrong, access denied\n")
    else:
        session_pw = master_password

print("Successfully logged in!\n")

while True:
    mode = input("""
How can I help you today?
[1] Add a new password
[2] Get an existing password
[3] Generate a new password (a-z, A-Z, 0-9)
[4] Quit
""").strip()

    # add
    if mode == "1":
        service = input("Enter the name of the service for your new password: ")
        username = input("Enter your username for this service: ")
        password = getpass.getpass("Enter your password: ")
        encrypted = crypto.encrypt(session_pw, password)

        if db.add_password(service, username, encrypted):
            print(f"Successfully added password for {service} to database!\n")
            continue
        else:
            print("A password for given service and username already exists!\n")
            continue

    #get
    elif mode == "2":
        service = input("Which password do you need? Enter the name of the service: ")
        resp = db.get_password(service)

        if len(resp) == 0:
            print("No password was found for given service!\n")
        elif len(resp) == 1:
            user_acc = resp[0][0]
            decrypted_pw = crypto.decrypt(session_pw, resp[0][1])
            pyperclip.copy(decrypted_pw)
            print(f"User: {user_acc} | Password copied to clipboard!")
        else:
            print("Multiple accounts found!\n")
            for i, row in enumerate(resp):
                print(f"[{i + 1}] {row[0]}")

            sel = int(input("Select number: ")) - 1
            target = resp[sel]
            pw = crypto.decrypt(session_pw, target[1])
            pyperclip.copy(pw)

            print(f"Your username: {target[0]}\nYour password has been copied to your clipboard\n")

    #generate
    elif mode == "3":
        alphabet = string.ascii_letters + string.punctuation
        length = int(input("How long should your password be? "))
        password = "".join(secrets.choice(alphabet) for i in range(length))
        print(f"Here is your new password: {password}")

    #quit
    elif mode == "4":
        print("Goodbye!\n")
        exit(0)

    #invalid input
    else:
        print("Your input does not match any of the options. Please try again.\n")
        continue
