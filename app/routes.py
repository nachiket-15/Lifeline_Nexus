# have included comment in routes regarding detailed Info of pymysql
import pymysql

from flask import Flask,render_template, request, redirect, url_for,session,flash,get_flashed_messages

from app import app,mail

from flask_mail import Mail,Message

from app.utils import get_db_connection, authenticate_admin, authenticate_user, create_user_account,is_donor_id_unique,excepting,executeQuery,executeQueryWithLastID,fetchOne,calculate_age,fetch_user_email_from_db


from datetime import date,datetime





app.secret_key = 'your_secret_key' 




@app.route('/')
def index():
    return render_template("index.html")






'''

@app.route()
This decorator in flask is used to associate a URL with a particular view function in your application . In below case '/admin_login' (URL) is associated with a view function that handles both GET & POST Requests.

admin_login() below is the corresponding view function

This view function is associated with particular URL (here '/admin_login')


When client requests a specific URL (/admin_login) from your Flask application , flask invokes corresponding view function to handle that request.

'''


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



'''
"request" is an object provided by Flask itself. It is part of Flask framework and is used to access incoming request data, such as form data, query parameters, and headers, when handling HTTP requests.


When a request is made to route -> '/admin_login' , flask will inspect (check) request method of incoming HTTP request and deteremines if it matches any of the methods specified in "methods" parameter 


request.method: This attribute gives you access to the HTTP method of the request (e.g., 'GET', 'POST').
request.form: This attribute is a dictionary-like object containing the form data from a POST request.
request.args: This attribute is a dictionary-like object containing the query parameters from a request URL.
'''








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




'''
In a Flask application, both `redirect` and `render_template` are functions used to generate HTTP responses, but they serve different purposes:

1. "redirect":
   - `redirect` is a function provided by Flask that generates an HTTP redirect response to a specified URL.
   - It is typically used to redirect the user's browser to a different URL, either within the same Flask application or to an external URL.
   - `redirect` takes a URL as its argument, which can be specified as a string representing the target URL or using the "url_for" function to generate a URL based on a specific route or endpoint in your Flask application.

   - Example:
     ```
     return redirect(url_for('admin_dashboard'))
     ```

   - In this example, if the admin authentication is successful, the user is redirected to the `'admin_dashboard'` route in the Flask application.



2. "url_for":

   - "url_for" is a function provided by Flask that generates a URL for a given route or endpoint in your Flask application.
   - It is commonly used to dynamically generate URLs in your templates or when generating redirects using the "redirect" function.
   - "url_for" takes the name of a route or endpoint as its argument and optionally accepts keyword arguments corresponding to the route's parameters.
   - Example:
     ```
     return redirect(url_for('admin_dashboard'))
     ```
   - In this example, "url_for('admin_dashboard')" generates the URL for the `'admin_dashboard'` route in the Flask application, which is then used as the target URL for the redirect.

3. "`render_template`:"
   - `render_template` is a function provided by Flask that renders a template file (typically an HTML file) and returns it as the HTTP response.
   - It is used to generate HTML content dynamically by rendering templates with data passed from the view function.
   - "render_template" takes the name of the template file as its argument and optionally accepts additional keyword arguments representing data to be passed to the template.
   - Example:
     ```
     return render_template('admin_login.html', error="Invalid Admin Credentials")
     ```
   - In this example, if the admin authentication fails, the 'admin_login.html' template file is rendered with an error message indicating invalid admin credentials.


In summary, `redirect` is used to redirect the user's browser to a different URL, `url_for` is used to generate URLs dynamically within your Flask application, and `render_template` is used to render HTML templates and generate dynamic HTML content for HTTP responses.

'''








@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html',current_user_is_admin=False)
    








@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_email=request.form['new_email']
        new_password = request.form['new_password']

        success = create_user_account(new_username,new_email,new_password)
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
            return render_template('error.html', error_message='Donor Not Eligible.')


    return render_template('add_donor.html')



'''
"cur.lastrowid" ->
In flask this is property of cursor object ('cur') that represents auto incremented ID of last row inserted into a table

This property is typically used after executing an INSERT statement to retrieve auto generated primary key value of newly inserted row.

"cur.fetchall()"->
This is a method of the cursor object (cur) that retrieves all remaining rows of a query result set as a list of tuples. This method is typically used after executing a SELECT statement to fetch multiple rows of data from the database.



'''








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

                affected_rows = executeQuery(update_query, update_values)#returns no of affected rows in form of list

                if isinstance(affected_rows, list) and affected_rows:
                    if affected_rows[0] > 0:
                        print(f"Blood assigned successfully for Recipient: {row['recipient_name']}")
                        success_message = f"Blood assigned successfully for Recipient: {row['recipient_name']}"
                        return render_template('success.html', success_message=success_message)
                    else:
                        print(f"No available blood for Recipient: {row['recipient_name']}")
                        error_message = f"No available blood for Recipient: {row['recipient_name']}"
                        return render_template('error.html', error_message=error_message)
                # else:          
                #     error_message = f"Unable to determine affected rows after updating BLOOD_AMOUNT."
                #     print(f"Error: {error_message}")
                #     return render_template('error.html', error_message=error_message)

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
    try:
        query = "SELECT * FROM REQUESTS"
        requests = executeQuery(query)
        messages = get_flashed_messages()

        return render_template('admin_requests.html', requests=requests, messages=messages)

    except Exception as e:
        import traceback
        print(f"Error in admin_requests: {e}")
        traceback.print_exc()
        flash('An error occurred.', 'danger')
        return redirect(url_for('error_page'))




'''

get_flashed_messages() function is a part of Flask's flash messaging system. In a Flask application, flash messages are temporary messages that can be stored and retrieved across requests. They are typically used to display feedback or notifications to users, such as success messages, error messages, or informational messages.

The get_flashed_messages() function is used to retrieve the flashed messages that were stored in the session during previous requests. It returns a list of flashed messages, and it can be called within a view function or a template to access these messages.

'''













def send_email(to, subject, body):
    try:
        msg = Message(subject, recipients=[to], body=body)
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


'''
Python function, send_email, is designed to send an email using Flask-Mail, a Flask extension for sending email messages from your Flask application.

function named send_email accepts three parameters: to, subject, and body, which represent the recipient email address, the email subject, and the email body respectively.

Inside the try block, an instance of the Message class is created with the specified subject, recipient email address (to), and email body (body).
The mail.send() method is then called to send the email message using the configured email server settings.
If the email is sent successfully without raising any exceptions, the function returns True to indicate success.

'''




@app.route('/admin_approve/<int:request_id>')
def admin_approve(request_id):
    try:
        # Get current blood type and requested amount
        query_info = "SELECT username, blood_type, quantity_needed, status FROM REQUESTS WHERE request_id=%s"
        values_info = (request_id,)
        result_info = fetchOne(query_info, values_info)

        if result_info:
            username = result_info['username']
            blood_type = result_info['blood_type']
            quantity_needed = result_info['quantity_needed']
            request_status = result_info['status']

            # Get current blood amount
            query_amount = "SELECT blood_amount FROM BLOOD_AMOUNT WHERE blood_type=%s"
            values_amount = (blood_type,)
            result_amount = fetchOne(query_amount, values_amount)

            if result_amount and result_amount['blood_amount'] >= quantity_needed:


                # Update request status to 'Approved'
                query_update = "UPDATE REQUESTS SET status='Approved' WHERE request_id=%s"
                values_update = (request_id,)
                executeQuery(query_update, values_update)



                # Reduce the quantity from BLOOD_AMOUNT table
                query_reduce_blood = "UPDATE BLOOD_AMOUNT SET blood_amount = blood_amount - %s WHERE blood_type = %s"
                values_reduce_blood = (quantity_needed, blood_type)
                executeQuery(query_reduce_blood, values_reduce_blood)



                # Send email to the user
                user_email = fetch_user_email_from_db(username)
                if user_email:
                    subject = 'Blood Request Status'
                    # body="Dear User , Your Request Has been taken into consideration , Kindly login your acccount to see the status of request \nThankyou!"
                    
                    
                    new_query="SELECT status FROM REQUESTS WHERE request_id=%s"
                    parameters=(request_id,)
                    con=get_db_connection()
                    cur=con.cursor()
                    cur.execute(new_query,parameters)

                    fetched=cur.fetchone()

                    result_required=fetched['status']

                    if result_required == 'Approved':
                        body = f"Your blood request with ID {request_id} has been approved. Kindly visit Blood Bank as soon as possible !"
                    
                    send_email(user_email, subject, body)

                    # flash('Request approved successfully. Email sent to the user.', 'success')
                else:
                    flash('User email not found. Email not sent.', 'warning')
            else:
                flash(["Insufficient blood available for blood type {}. Current amount: {}".format(blood_type, result_amount["blood_amount"])], 'danger')


        else:
            flash('Invalid request ID.', 'danger')

    except Exception as e:
        import traceback
        print(f"Error in admin_approve: {e}")
        print(traceback.format_exc())
        flash('An error occurred.', 'danger')

    return redirect(url_for('admin_requests'))






@app.route('/admin_reject/<int:request_id>')
def admin_reject(request_id):
    
    query = "UPDATE REQUESTS SET status='Rejected' WHERE request_id=%s"
    values = (request_id,)
    executeQuery(query,values)
    return redirect(url_for('admin_requests'))








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
