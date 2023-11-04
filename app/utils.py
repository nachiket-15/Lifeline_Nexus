import pymysql
from datetime import datetime, date

# DATABASE CONNECTION
def get_db_connection():
    try:
        con = pymysql.connect(
            host='localhost',
            user='root',
            password='Nachiket@4545',
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
def create_user_account(username, password):
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
                    insert_query = f"INSERT INTO USER_ACCOUNTS (username, password) VALUES ('{username}', '{password}')"
                    cur.execute(insert_query)
                    con.commit()
                    print("Account created successfully!")
                    return True
        except Exception as e:
            print(f"Error creating account: {e}")
        finally:
            con.close()
    return False


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



def calculate_age(birth_date):
    days_in_year = 365.2425
    age = int((date.today() - birth_date).days / days_in_year)
    return age





# ADMIN FUNCTIONALITIES

# 1) ADD DONOR 
# Python function to add a donor
def addDonor():
    try:
        row = {}
        print("Enter new donation details: ")
        # No need to ask for donor_id input, it will be auto-incremented
        row["date_of_donation"] = input("Date of donation (YYYY-MM-DD): ")
        query = "INSERT INTO DONORS(date_of_donation) VALUES('%s')" % (row["date_of_donation"])
        print(query)
        executeQuery(query)

        print("Inserted Into Database")

    except Exception as e:
        excepting(e)

    return

# 2) ADD RECEPIENT 
def addRecipient():
	try:
		row = {}
		print("Enter new recipient's details: ")
		rawname = input("Name (Fname Lname): ")
		name = (rawname).split(' ')
		row["fname"] = name[0]
		row["lname"] = name[1]
		var3 = input("Rec_id: ")
		row["rec_id"] = int(var3)
		row["blood_type"]=input("Plasma Blood_type: ")
		var0 = input("Quantity_needed: ")
		row["quantity_needed"] = int(var0)
		row["date_of_request"] = input("Date of request (YYYY-MM-DD): ")
		dob = (input("DOB (YYYY-MM-DD): ")).split('-')
		row["dOB"] = dob[0]+'-'+dob[1]+'-'+dob[2]
		print("Age:", calculateAge(date(int(dob[0]), int(dob[1]), int(dob[2]))), "years")
		row["age"] = calculateAge(date(int(dob[0]), int(dob[1]), int(dob[2])))
		row["sex"] = input("Sex: ")
		var5 = input("Address: ")
		row["address"] = var5
		query = "INSERT INTO RECIPIENT(rec_id,blood_type,quantity_needed,date_of_request,fname,lname,dOB,sex,age,address) VALUES('%d', '%s', '%d','%s','%s','%s','%s','%s','%d','%s')" %(row["rec_id"], row["blood_type"], row["quantity_needed"], row["date_of_request"],row["fname"],row["lname"],row["dOB"],row["sex"],row["age"],row["address"])
		executeQuery(query)

		print("Inserted Into Database")

	except Exception as e:
		excepting(e)
		
	return


# 3) ADD BLOOD DETAILS 
def addBlood():
	try:
		# Takes emplyee details as input
		row = {}
		print("Enter new Plasma details: ")
		var0 = input("plasma_bag_number: ")
		row["plasma_bag_number"] = int(var0)
		row["blood_type"] = input("Plasma blood_type: ")
		var1 = input("blood_amount: ")
		row["blood_amount"] = int(var1)
		var2 = input("platelets_count (in thousands): ")
		row["platelets_count"] = float(var2)
		query = "INSERT INTO BLOOD(plasma_bag_number,blood_type,blood_amount,platelets_count) VALUES('%d', '%s', '%d', '%0.1f')" %(row["plasma_bag_number"],row["blood_type"], row["blood_amount"], row["platelets_count"])
		executeQuery(query)
		print("Inserted Into Database")

	except Exception as e:
		excepting(e)
		
	return


# 4) ADD BLOOD COST
def AddBloodCost():
	try :
		row={}
		print("Enter following details: ")
		var0 = input("Plasma bag number: ")
		row["plasma_bag_number"] = int(var0)
		row["cost"] = int(input("Plasma Cost: "))
		query = "INSERT INTO BLOOD_COST(plasma_bag_number,cost) VALUES('%d', '%d')" %(row["plasma_bag_number"],row["cost"])
		executeQuery(query)
		print("Inserted Into Database")

	except Exception as e:
		excepting(e)

	return

# 5) ADD PAYMENT TRANSACTION 

def addPaymentTnx():
	try:
		row = {}
		print("Enter transaction details: ")
		var0 = input("rec_id: ")
		row["rec_id"] = int(var0)
		var1 = input("Payment Amount: ")
		row["payment_amt"] = int(var1)
		timenow = datetime.now()
		current_time = timenow.strftime("%d/%m/%Y %H:%M:%S")
		print("Time of Txn =", current_time)
		row["payment_time"] = current_time
		query = "INSERT INTO PAYMENT_TRANSACTION(rec_id,payment_amt,payment_time) VALUES('%d', %d', '%s')" %(row["rec_id"],row["payment_amt"], row["payment_time"])
		executeQuery(query)
		print("Inserted Into Database")

	except Exception as e:
		excepting(e)
		
	return


# 6) VIEW BLOOD 
def ViewBlood():
	try :
		query = "select * FROM BLOOD"
		executeQuery(query)
		row = cur.fetchall()
		print(row)
	except Exception as e:
		excepting(e)

	return








# 7) SUPERVISORS
def Supervisors():
	try :
		a = input("Enter supervisor name: ")
		query = "select * FROM STAFF where supervisor='%s'" % (a)
		executeQuery(query)
		row = cur.fetchall()
		print("Employees under Supervisor", a, "are:" )
		print(row)
	except Exception as e:
		excepting(e)
		
	return         











# 
def TotalBlood():
	try :
		query = "select SUM(blood_amount) total FROM BLOOD"
		executeQuery(query)
		row = cur.fetchall()
		print("The total Plasma available is :")
		print(row)
	except Exception as e:
		excepting(e)
		
	return



def is_donor_id_unique(donor_id):
    db_connection = get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM DONORS WHERE donor_id = %s", (donor_id,))
    result = cursor.fetchone()
    db_connection.close()

    return result is None



