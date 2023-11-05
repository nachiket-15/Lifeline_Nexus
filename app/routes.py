from flask import Flask,render_template, request, redirect, url_for,session
from app import app
from flask_mail import Mail,Message
from app.utils import get_db_connection, authenticate_admin, authenticate_user, create_user_account,is_donor_id_unique,excepting,executeQuery,executeQueryWithLastID,fetchOne,calculate_age
from datetime import date,datetime
import pymysql

from app import app, mail


app.secret_key = 'your_secret_key' 




@app.route('/')
def index():
    return render_template("index.html")







@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form['admin_username']
        admin_password = request.form['admin_password']

        if authenticate_admin(admin_username, admin_password):
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error="Invalid Admin Credentials")

    return render_template('admin_login.html')









@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')









@app.route('/user_login', methods=['GET', 'POST'])
def user_login():

    if request.method == 'POST':
        user_username = request.form['user_username']
        user_password = request.form['user_password']

        if authenticate_user(user_username, user_password):
            session['username'] = user_username
            return render_template('user_dashboard.html')
        else:
            return render_template('user_login.html', error="Invalid User Credentials")
    return render_template("user_login.html")









@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html',current_user_is_admin=False)
    








@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']

        success = create_user_account(new_username, new_password)
        if success:
            return redirect(url_for('user_login'))
        else:
            return render_template('create_account.html', error="Error creating account")

    return render_template('create_account.html')






@app.route('/add_donor', methods=['GET', 'POST'])
def add_donor():
    if request.method == 'POST':
        date_of_donation = request.form['date_of_donation']
        donor_name = request.form['donor_name']
        blood_type = request.form['blood_type']
        phone_no = request.form['phone_no']
        address = request.form['address']
        email = request.form['email']
        body_weight = float(request.form['body_weight'])
        age = int(request.form['age'])
        health_conditions = 'health_conditions' in request.form 
        blood_amount = float(request.form['blood_amount']) 
        hemoglobin_level=int(request.form['hemoglobin_level'])

        if not health_conditions:
            return render_template('error.html', error_message="Sorry, the donor is not eligible for donation due to certain health conditions.")

        try:
            conn = get_db_connection()
            cur = conn.cursor()

           # Insert donor information into DONORS table
            donor_query = "INSERT INTO DONORS (donor_name, blood_type, date_of_donation, phone_no, address, email, body_weight, age, health_condition, blood_amount, hemoglobin_level) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            donor_values = (donor_name, blood_type, date_of_donation, phone_no, address, email, body_weight, age, health_conditions, blood_amount, hemoglobin_level)

            cur.execute(donor_query, donor_values)

            # Get the last inserted donor_id
            if cur.lastrowid:
                donor_id = cur.lastrowid
            else:
                donor_id = None

            # Insert blood donation information into BLOOD_UNITS table
            blood_unit_query = "INSERT INTO BLOOD_UNITS (donor_id, collection_date, expiry_date, blood_type, blood_amount) VALUES (%s, %s, DATE_ADD(%s, INTERVAL 42 DAY), %s, %s)"
            blood_unit_values = (donor_id, date_of_donation, date_of_donation, blood_type, blood_amount)
            cur.execute(blood_unit_query, blood_unit_values)


            blood_amount_query = "UPDATE BLOOD_AMOUNT SET blood_amount = blood_amount + %s WHERE blood_type = %s"
            increment_amount = blood_amount
            blood_amount_values = (increment_amount, blood_type)
            executeQuery(blood_amount_query, blood_amount_values)




            # Commit changes and close the connection
            conn.commit()
            cur.close()
            conn.close()

            return render_template('success.html', success_message="Donor and Blood Donation added successfully!")

        except pymysql.Error as e:
            print(f"MySQL Error: {e}")
            return render_template('error.html', error_message='A MySQL error occurred while adding the donor and blood donation.')


    return render_template('add_donor.html')












@app.route('/add_donor_user', methods=['GET', 'POST'])
def add_donor_user():
    if request.method == 'POST':
        date_of_donation = request.form['date_of_donation']
        donor_name = request.form['donor_name']
        blood_type = request.form['blood_type']
        phone_no = request.form['phone_no']
        address = request.form['address']
        email = request.form['email']
        body_weight = float(request.form['body_weight'])
        age = int(request.form['age'])
        health_conditions = 'health_conditions' in request.form 
        blood_amount = float(request.form['blood_amount']) 
        hemoglobin_level=int(request.form['hemoglobin_level'])

        if not health_conditions:
            return render_template('error.html', error_message="Sorry, the donor is not eligible for donation due to certain health conditions.")

        try:
            conn = get_db_connection()
            cur = conn.cursor()

           # Insert donor information into DONORS table
            donor_query = "INSERT INTO DONORS (donor_name, blood_type, date_of_donation, phone_no, address, email, body_weight, age, health_condition, blood_amount, hemoglobin_level) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            donor_values = (donor_name, blood_type, date_of_donation, phone_no, address, email, body_weight, age, health_conditions, blood_amount, hemoglobin_level)

            cur.execute(donor_query, donor_values)

            # Get the last inserted donor_id
            if cur.lastrowid:
                donor_id = cur.lastrowid
            else:
                donor_id = None

            # Insert blood donation information into BLOOD_UNITS table
            blood_unit_query = "INSERT INTO BLOOD_UNITS (donor_id, collection_date, expiry_date, blood_type, blood_amount) VALUES (%s, %s, DATE_ADD(%s, INTERVAL 42 DAY), %s, %s)"
            blood_unit_values = (donor_id, date_of_donation, date_of_donation, blood_type, blood_amount)
            cur.execute(blood_unit_query, blood_unit_values)


            blood_amount_query = "UPDATE BLOOD_AMOUNT SET blood_amount = blood_amount + %s WHERE blood_type = %s"
            increment_amount = blood_amount
            blood_amount_values = (increment_amount, blood_type)
            executeQuery(blood_amount_query, blood_amount_values)




            # Commit changes and close the connection
            conn.commit()
            cur.close()
            conn.close()

            return render_template('success.html', success_message="Donor and Blood Donation added successfully!")

        except pymysql.Error as e:
            print(f"MySQL Error: {e}")
            return render_template('error.html', error_message='A MySQL error occurred while adding the donor and blood donation.')


    return render_template('add_donor_user.html')

















@app.route('/add_recipient', methods=['GET', 'POST'])
def add_recipient():
    if request.method == 'POST':
        try:
            row = {}
            row["recipient_name"] = request.form.get("recipient_name")
            row["blood_type"] = request.form.get("blood_type")
            row["quantity_needed"] = int(request.form.get("quantity_needed"))
            row["date_of_request"] = request.form.get("date_of_request")
            row["dOB"] = request.form.get("dob")
            row["age"] = calculate_age(datetime.strptime(row["dOB"], '%Y-%m-%d'))
            row["sex"] = request.form.get("sex")
            row["address"] = request.form.get("address")

            # Check if the required blood quantity is available
            check_query = "SELECT blood_amount FROM BLOOD_AMOUNT WHERE blood_type = %s"
            check_values = (row["blood_type"],)
            result = fetchOne(check_query, check_values)

            total_available_blood = result['blood_amount'] if result and 'blood_amount' in result else 0

            if total_available_blood >= row["quantity_needed"]:
                # Proceed with the insertion into RECIPIENT table
                query = "INSERT INTO RECIPIENT(blood_type, quantity_needed, date_of_request, recipient_name, dOB, age, sex, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                values = (row["blood_type"], row["quantity_needed"], row["date_of_request"], row["recipient_name"], row["dOB"], row["age"], row["sex"], row["address"])
                executeQuery(query, values)

                # Update the available blood quantity in BLOOD_AMOUNT table
                update_query = "UPDATE BLOOD_AMOUNT SET blood_amount = blood_amount - %s WHERE blood_type = %s"
                update_values = (row["quantity_needed"], row["blood_type"])
                affected_rows = executeQuery(update_query, update_values)

                if isinstance(affected_rows, list) and affected_rows:
                    if affected_rows[0] > 0:
                        print(f"Blood assigned successfully for Recipient: {row['recipient_name']}")
                        success_message = f"Blood assigned successfully for Recipient: {row['recipient_name']}"
                        return render_template('success.html', success_message=success_message)
                    else:
                        print(f"No available blood for Recipient: {row['recipient_name']}")
                        error_message = f"No available blood for Recipient: {row['recipient_name']}"
                        return render_template('error.html', error_message=error_message)
                else:          
                    error_message = f"Unable to determine affected rows after updating BLOOD_AMOUNT."
                    print(f"Error: {error_message}")
                    return render_template('error.html', error_message=error_message)

            else:
                error_message = f"Insufficient blood available for blood type {row['blood_type']}"
                print(f"Error: {error_message}")
                return render_template('error.html', error_message=error_message)

        except Exception as e:
            import traceback
            print(f"Error: {e}")
            print(traceback.format_exc())
            return render_template('error.html', error_message='An error occurred.')

    return render_template('add_recipient.html')





@app.route('/add_plasma_details', methods=['GET', 'POST'])
def add_plasma_details():
    if request.method == 'POST':
        plasma_bag_number = request.form['plasma_bag_number']
        blood_type = request.form['blood_type']
        blood_amount = request.form['blood_amount']
        platelets_count = request.form['platelets_count']

        # Use placeholders in the SQL query to avoid SQL injection
        query = "INSERT INTO BLOOD(plasma_bag_number, blood_type, blood_amount, platelets_count) VALUES (%s, %s, %s, %s)"
        values = (plasma_bag_number, blood_type, blood_amount, platelets_count)

        try:
            executeQuery(query, values)
            print("Plasma details added successfully!")
            return render_template('success.html')

        except Exception as e:
            print(e)
            return render_template('error.html', error_message=str(e))

    return render_template('add_plasma_details.html')








@app.route('/update_blood_cost', methods=['GET', 'POST'])
def update_blood_cost():
    if request.method == 'POST':
        blood_type = request.form['blood_type']
        blood_cost = request.form['blood_cost']

        # Check if blood_type exists
        existing_query = "SELECT * FROM BLOOD_COST WHERE blood_type = %s"
        existing_values = (blood_type,)
        existing_record = fetchOne(existing_query, existing_values)

        if existing_record:
            # Update the existing record
            update_query = "UPDATE BLOOD_COST SET cost = %s WHERE blood_type = %s"
            update_values = (blood_cost, blood_type)
            executeQuery(update_query, update_values)
            print("Blood cost updated successfully!")
        else:
            # Insert a new record
            insert_query = "INSERT INTO BLOOD_COST(blood_type, cost) VALUES (%s, %s)"
            insert_values = (blood_type, blood_cost)
            executeQuery(insert_query, insert_values)
            print("Blood cost added successfully!")

    return render_template('update_blood_cost.html')







@app.route('/add_payment_transaction', methods=['GET', 'POST'])
def add_payment_transaction():
    if request.method == 'POST':
        rec_id = request.form['rec_id']
        payment_amt = request.form['payment_amt']

        query = "INSERT INTO PAYMENT_TRANSACTION(rec_id, payment_amt) VALUES (%s, %s)"
        values = (rec_id, payment_amt)
        executeQuery(query, values)

        print("Payment transaction added successfully!")

    return render_template('add_payment_transaction.html')









@app.route('/view_blood')
def view_blood():
    try:
        con = get_db_connection()
        cur = con.cursor()

        today = date.today()

        query = "SELECT blood_type, blood_amount  FROM BLOOD_AMOUNT "
        cur.execute(query)
        blood_data = cur.fetchall()

        cur.close()
        con.close()

        return render_template('view_blood.html', blood_data=blood_data)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message='An error occurred.')






@app.route('/view_blood_user')
def view_blood_user():
    try:
        con = get_db_connection()
        cur = con.cursor()

        today = date.today()

        query = "SELECT blood_type, blood_amount  FROM BLOOD_AMOUNT "
        cur.execute(query)
        blood_data = cur.fetchall()

        cur.close()
        con.close()

        return render_template('view_blood_user.html', blood_data=blood_data)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message='An error occurred.')





import logging

@app.route('/blood_cost')
def blood_cost():
    try:
        # Using 'with' statement for context management
        with get_db_connection() as conn, conn.cursor() as cur:
            query = """
                SELECT bc.blood_type, bc.cost
                FROM BLOOD_COST bc
            """
            cur.execute(query)
            blood_cost_data = cur.fetchall()

        # Log successful retrieval of data
        app.logger.info("Blood cost data retrieved successfully")

        return render_template('blood_cost.html', blood_cost_data=blood_cost_data)
    except Exception as e:
        # Log the exception
        app.logger.error(f"An error occurred: {e}")

        
        return render_template('error.html', error_message='An error occurred.')
















@app.route('/view_donors')
def view_donors():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = "SELECT donor_id, donor_name, blood_type, date_of_donation,blood_amount FROM DONORS"
        cur.execute(query)
        donor_data = cur.fetchall()

        cur.close()
        conn.close()

        return render_template('view_donors.html', donor_data=donor_data)
    except Exception as e:
        # print(f"Error: {e}")  # Add this line for debugging
        return render_template('error.html', error_message='An error occurred.')













@app.route('/view_recipients')
def view_recipients():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = "SELECT * FROM RECIPIENT"
        cur.execute(query)
        recipient_data = cur.fetchall()

        cur.close()
        conn.close()

        return render_template('view_recipients.html', recipient_data=recipient_data)
    except Exception as e:
        print(e)
        return render_template('error.html', error_message='An error occurred.')











@app.route('/hire_staff', methods=['GET', 'POST'])
def hire_staff():
    if request.method == 'POST':
        try:
            emp_id = request.form['emp_id']
            fname = request.form['fname']
            supervisor = request.form['supervisor']
            address1 = request.form['address1']
            phone_no = request.form['phone_no']
            salary = request.form['salary']

            #
            # Your query and values
            query = "INSERT INTO STAFF(emp_id, fname, supervisor, address1, phone_no, salary) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (emp_id, fname, supervisor, address1, phone_no, salary)

            executeQuery(query,values)

            return render_template('success.html',success_message='Staff hired successfully!')
        except Exception as e:
            return render_template('error.html', error_message=str(e))

    return render_template('hire_staff.html')







@app.route('/view_transactions')
def view_transactions():
    try:
        transaction_data = executeQuery("SELECT * FROM PAYMENT_TRANSACTION")
        print(transaction_data)  # Add this line for debugging
        return render_template('view_transactions.html', transaction_data=transaction_data)
    except Exception as e:
        print(str(e))  # Add this line for debugging
        return render_template('error.html', error_message=str(e))











@app.route('/view_staff')
def view_staff():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query="SELECT * FROM STAFF"
        cur.execute(query)
        staff_data = cur.fetchall()

        cur.close()
        conn.close()
        
        return render_template('view_staff.html', staff_data=staff_data)
    except Exception as e:
        return render_template('error.html', error_message=str(e))




@app.route('/admin_requests')
def admin_requests():
    # Retrieve requests from the database
    # (You should use placeholders to prevent SQL injection)
    query = "SELECT * FROM REQUESTS"
    # Assuming executeQuery returns the fetched data, modify it accordingly
    requests = executeQuery(query)

    return render_template('admin_requests.html', requests=requests)





@app.route('/admin_approve/<int:request_id>')
def admin_approve(request_id):
    query = "UPDATE REQUESTS SET status='Approved' WHERE request_id=%s"
    values = (request_id,)
    executeQuery(query,values)
    return redirect(url_for('admin_requests'))




@app.route('/admin_reject/<int:request_id>')
def admin_reject(request_id):
    
    query = "UPDATE REQUESTS SET status='Rejected' WHERE request_id=%s"
    values = (request_id,)
    executeQuery(query,values)
    return redirect(url_for('admin_requests'))





# routes.py



@app.route('/user_request', methods=['GET', 'POST'])
def user_request():
    if request.method == 'POST':
        username = session.get('username')
        blood_type = request.form['blood_type']
        quantity_needed = int(request.form['quantity_needed'])
        date_of_request = request.form['date_of_request']

        query = "INSERT INTO `REQUESTS` (username, blood_type, quantity_needed, date_of_request) VALUES (%s, %s, %s, %s)"
        values = (username, blood_type, quantity_needed, date_of_request)

        success = executeQuery(query, values)

        # Send email to admin
        admin_email = 'developernachiket@gmail.com'  # Replace with your admin's email
        subject = f"Blood Donation Request from {username}"
        body = f"A user with username {username} has requested {quantity_needed} ml of blood type {blood_type} on {date_of_request}."
        
        msg = Message(subject=subject, recipients=[admin_email], body=body)
        mail.send(msg)

        return render_template('success2.html', success_message="Blood donation request submitted successfully!")

    return render_template('user_request.html')






@app.route('/request_status')
def request_status():
    uname = session.get('username')
    if uname:
        query = "SELECT request_id, blood_type, quantity_needed, date_of_request, status FROM REQUESTS WHERE username = %s"
        values = (uname,)
        user_requests = executeQuery(query, values)

        if user_requests is not None:
            return render_template('request_status.html', user_requests=user_requests, uname=uname)
        else:
            return render_template('error.html', error_message="Error retrieving user requests.")
    else:
        return render_template('error.html', error_message="User not logged in.")
