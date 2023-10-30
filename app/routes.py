from flask import render_template, request, redirect, url_for
from app import app
from app.utils import get_db_connection, authenticate_admin, authenticate_user, create_user_account,is_donor_id_unique,excepting,executeQuery





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
            return redirect(url_for('user_dashboard'))
        else:
            return render_template('user_login.html', error="Invalid User Credentials")

    return render_template('user_login.html')











@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')










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
        donor_id = request.form['donor_id']
        date_of_donation = request.form['date_of_donation']

        if is_donor_id_unique(donor_id):
            query = "INSERT INTO DONORS (donor_id, date_of_donation) VALUES (%s, %s)"
            values = (donor_id, date_of_donation)
            executeQuery(query, values)
            return "Donor added successfully!"
        else:
            return "Donor ID already taken. Choose a new unique Donor ID."

    return render_template('add_donor.html')










@app.route('/add_recipient', methods=['GET', 'POST'])
def add_recipient():
    if request.method == 'POST':
        try:
            row = {}
            row["recipient_name"] = request.form.get("recipient_name")
            row["rec_id"] = int(request.form.get("rec_id"))
            row["blood_type"] = request.form.get("blood_type")
            row["quantity_needed"] = int(request.form.get("quantity_needed"))
            row["date_of_request"] = request.form.get("date_of_request")
            dob = request.form.get("dob").split('-')
            row["dOB"] = dob[0]+'-'+dob[1]+'-'+dob[2]
            row["age"] = calculateAge(datetime.strptime(row["dOB"], '%Y-%m-%d'))
            row["sex"] = request.form.get("sex")
            row["address"] = request.form.get("address")

            query = "INSERT INTO RECIPIENT(recipient_name, rec_id, blood_type, quantity_needed, date_of_request, dOB, age, sex, address) VALUES (%s, %d, %s, %d, %s, %s, %d, %s, %s)"
            values = (row["recipient_name"], row["rec_id"], row["blood_type"], row["quantity_needed"], row["date_of_request"], row["dOB"], row["age"], row["sex"], row["address"])

            executeQuery(query, values)

            print("Inserted Into Database")

        except Exception as e:
            excepting(e)

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

        executeQuery(query,values)
        
        print("Plasma details added successfully!")

    return render_template('add_plasma_details.html')










@app.route('/add_blood_cost', methods=['GET', 'POST'])
def add_blood_cost():
    if request.method == 'POST':
        plasma_bag_number = request.form['plasma_bag_number']
        cost = request.form['cost']

        query = "INSERT INTO BLOOD_COST(plasma_bag_number, cost) VALUES (%s, %s)"
        values = (plasma_bag_number, cost)
        executeQuery(query, values)

        print("Blood cost added successfully!")

    return render_template('add_blood_cost.html')








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
        conn = get_db_connection()
        cur = conn.cursor()

        query = "SELECT * FROM BLOOD"
        cur.execute(query)  
        blood_data = cur.fetchall()

        cur.close()
        conn.close()

        return render_template('view_blood.html', blood_data=blood_data)
    except Exception as e:
        print(e)
        return render_template('error.html', error_message='An error occurred.')










@app.route('/supervisors')
def supervisors():
    return render_template('supervisors.html')








@app.route('/view_donors')
def view_donors():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = "SELECT * FROM DONORS"
        cur.execute(query)  
        donor_data = cur.fetchall()

        cur.close()
        conn.close()

        return render_template('view_donors.html', donor_data=donor_data)
    except Exception as e:
        print(e)
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













# Hire Staff
@app.route('/hire_staff', methods=['GET', 'POST'])
def hire_staff():
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        fname = request.form['fname']
        supervisor = request.form['supervisor']
        address1 = request.form['address1']
        phone_no = request.form['phone_no']
        salary = request.form['salary']

        # Use placeholders in the SQL query to avoid SQL injection
        query = "INSERT INTO STAFF(emp_id, fname, supervisor, address1, phone_no, salary) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (emp_id, fname, supervisor, address1, phone_no, salary)

        executeQuery(query, values)

        print("Staff hired successfully!")

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
        # Retrieve staff data from the database
        staff_data = executeQuery("SELECT * FROM STAFF")
        return render_template('view_staff.html', staff_data=staff_data)
    except Exception as e:
        return render_template('error.html', error_message=str(e))










