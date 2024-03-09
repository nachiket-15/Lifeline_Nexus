'''
pymysql is python library that provides a pure Python MySQL client. It allows python programs to connect to a MySQL Server , execute SQL Queries , and interact with database 

pymysql.connect() is used to establish connectiuon with MySQL server 

connection=pymysql.connect(
    host="",
    user="",
    password="",
    database="",
    cursorclass=pymysql.cursors.DictCursor
)

A cursor is created using "connection.cursor()" to execute SQL Queries 

query=******sql query******

An SQL query is executed using "cursor.execute(query)"

'''



import pymysql
from datetime import datetime, date

# DATABASE CONNECTION
def get_db_connection():
    try:
        con = pymysql.connect(
            host='localhost',
            user='root',
            password='********',
            database='PLASMABANK',
            cursorclass=pymysql.cursors.DictCursor
        )

        return con
    except Exception as e:
        print(f"Error: {e}")
        return None


con = get_db_connection()

def excepting(e):
	con.rollback()
	print("Failed to insert/delete/update/find database")
	print (">>>>>>>>>>>>>", e)
	return


def executeQueryWithLastID(query, values):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(query, values)

        # Get the last inserted ID
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]

        connection.commit()

        return last_id
    except Exception as e:
        print(f"Error: {e}")
    





def fetchOne(query, values):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(query, values)
    result = cur.fetchone()

    cur.close()
    conn.close()

    return result

















# AUTHENTICATE ADMIN
def authenticate_admin(username, password):
    con = get_db_connection()
    if con:
        try:
            with con.cursor() as cur:
                query = f"SELECT * FROM ADMIN_ACCOUNTS WHERE username = '{username}' AND password = '{password}'"
                cur.execute(query)
                result = cur.fetchone()
                return result is not None
        except Exception as e:
            print(f"Error: {e}")
        finally:
            con.close()
    return False


'''

The query is executed using cursors's "execute()" method.
The result is fetched using "fetchone()" method.
fetchone() method retrieves first row of query result as tuple and stores it into result variable

If matching admin account is found then function returns true , else false.
If an error occurs during execution of SQL Query or any other part of function , exception is caught and database connection is closed whether an exception occurs or not.


'''













# AUTHENTICATE USERS
def authenticate_user(username, password):
    con = get_db_connection()
    if con:
        try:
            with con.cursor() as cur:
                query = f"SELECT * FROM USER_ACCOUNTS WHERE username = '{username}' AND password = '{password}'"
                cur.execute(query)
                result = cur.fetchone()
                return result is not None
        except Exception as e:
            print(f"Error: {e}")
        finally:
            con.close()
    return False









# CREATE NEW ACCOUNT
def create_user_account(username,email,password):
    con = get_db_connection()
    if con:
        try:
            with con.cursor() as cur:
                check_query = f"SELECT * FROM USER_ACCOUNTS WHERE username = '{username}'"
                cur.execute(check_query)
                existing_user = cur.fetchone()

                if existing_user:
                    print("Username already exists. Please choose a different username.")
                    return False
                else:
                    insert_query = f"INSERT INTO USER_ACCOUNTS (username,email,password) VALUES ('{username}','{email}','{password}')"
                    cur.execute(insert_query)
                    con.commit()
                    print("Account created successfully!")
                    return True

        except Exception as e:
            print(f"Error creating account: {e}")
        finally:
            con.close()
    return False











def fetch_user_email_from_db(username):
    try:
        con = get_db_connection()
        cursor = con.cursor()

        # Fetch user email based on the username
        query = "SELECT email FROM USER_ACCOUNTS WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            return result['email']
        else:
            return None

    except Exception as e:
        print(f"Error fetching user email: {e}")
        return None

    finally:
        if con:
            con.close()






import logging
def executeQuery(query, values=None):
    con = get_db_connection()
    try:
        with con.cursor() as cur:
            if values:
                cur.execute(query, values)
            else:
                cur.execute(query)
            result = cur.fetchall()  # Fetch all rows from the result set
            con.commit()
            return result
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        return None  # Indicate failure
    finally:
        con.close()






def calculate_age(dob):
    dob_datetime = datetime.combine(dob, datetime.min.time())
    current_date = datetime.now()
    age = current_date.year - dob_datetime.year - ((current_date.month, current_date.day) < (dob_datetime.month, dob_datetime.day))

    return age








def is_donor_id_unique(donor_id):
    db_connection = get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM DONORS WHERE donor_id = %s", (donor_id,))
    result = cursor.fetchone()
    db_connection.close()

    return result is None



