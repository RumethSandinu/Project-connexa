from flask import Flask, render_template, request, url_for, redirect, session
import tensorflow as tf
import pickle
import pandas as pd
import numpy as np
import mysql.connector
from decimal import Decimal
from matplotlib import pyplot as plt
from blueprints.db_handler import DatabaseHandler
import datetime

with open('../customer_preference_analysis/cluster_model.pkl', 'rb') as prf_model_file:
    cust_pref_model = pickle.load(prf_model_file)

with open('../time_based_analysis/TimeBasedAnalysis.pickle', 'rb') as tb_model_file:
    time_based_model = pickle.load(tb_model_file)

sales_pred_model = tf.keras.models.load_model('../sales_analysis/sales_prediction_model.keras')

cluster_data = pd.read_csv('../customer_preference_analysis/model_building.csv')
sales_pred_columns = pd.read_csv('../sales_analysis/column_names.csv')
time_model = pd.read_csv('../time_based_analysis/time_model.csv')
columns_loss_rate = pd.read_csv('../loss_rate_analysis/column_names')

app = Flask(__name__)
app.secret_key = 'Connexa123'


db_handler = DatabaseHandler()
cnx = mysql.connector.connect(user='root', password='', host='localhost', database='connexa')

if cnx.is_connected():
    print('Connected to database')
else:
    print('Error connecting to database:', cnx.connect_error)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/customer_ui')
def customer_ui():
    return render_template('customer_ui.html')

@app.route('/staff_ui')
def staff_ui():
    return render_template('staff_setting.html')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/shop')
def shop():
    cursor = cnx.cursor()
    query = 'SELECT item_name, price_kg, image_path FROM item'
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return render_template('shop.html', rows=rows)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ""  # Initialize error message

    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        # Authenticate user
        user_data = authenticate_user(email, password)
        print("123", user_data)

        if user_data:
            # User authentication successful, store user data in session
            session['user_email'] = email
            user_type = determine_user_type(email)
            session['user_type'] = user_type

            # Redirect based on user type
            if user_type == 'customer':
                return redirect(url_for('customer_ui'))
            elif user_type == 'staff':
                return redirect(url_for('staff_ui'))
        else:
            # If authentication fails, show an error message
            error_message = "Invalid email or password. Please try again."

    # If the request method is GET or authentication failed, render the login form with error message
    return render_template('login.html', error_message=error_message)


def authenticate_user(email, password):
    # Determine user type based on the email domain
    user_type = determine_user_type(email)
    print(user_type)
    # Authenticate user based on user type
    if user_type == 'customer':
        return db_handler.authenticate_customer(email, password)
    elif user_type == 'staff':
        return db_handler.authenticate_staff(email, password)
    elif user_type == 'admin':
        return db_handler.authenticate_admin(email, password)
    return None, "Invalid user type"


def determine_user_type(email):
    # Example: Check the email domain to determine user type
    if email.endswith('@connexa.com'):
        return 'staff'
    elif email.endswith('@connexa.com'):
        return 'admin'
    else:
        return 'customer'


@app.route('/dashboard')
def dashboard():
    # Example of a protected route that requires authentication
    if 'user_email' in session:
        return f"Welcome to the dashboard, {session['user_email']}! User Type: {session['user_type']}"
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("Form Data:", request.form)
        register_customer(request.form)
        user_type = request.form.get('userType')
        print("User Type:", user_type)
        if user_type == 'customer':
            result = register_customer(request.form)
        elif user_type == 'staff':
            result = register_staff(request.form)
        elif user_type == 'admin':
            result = register_admin(request.form)
        else:
            # Handle unexpected 'userType'
            result = False  # Or any other appropriate action
            print("Unexpected userType:", user_type)

        if result:
            return redirect(url_for('login'))  # Redirect to login page after successful registration

    return render_template('register.html')


def register_customer(form_data, pbkdf2_sha256=None):
    print("Form Data in register_customer function:", form_data)

    email = form_data.get('email_customer')
    password = form_data.get('password_customer')
    confirm_password = form_data.get('confirmPassword')
    first_name = form_data.get('firstName_customer')
    last_name = form_data.get('lastName_customer')
    dob = form_data.get('dob_customer')
    street = form_data.get('street_customer')
    city = form_data.get('city_customer')
    province = form_data.get('province_customer')
    postal_code = form_data.get('postalCode_customer')


    if password == confirm_password:
        hashed_password = pbkdf2_sha256.hash(password)

        customer = {
            'email': email,
            'password': hashed_password,
            'f_name': first_name,
            'l_name': last_name,
            'dob': dob,
            'street': street,
            'city': city,
            'province': province,
            'postal_code': postal_code
        }
        print(customer)

        return db_handler.insert_customer(customer)
    else:
        # Passwords do not match
        return False


def register_staff(form_data, pbkdf2_sha256=None):
    email = form_data.get('email_staff')
    staff_id = form_data.get('staffId')
    password = form_data.get('password')
    first_name = form_data.get('firstName_staff')
    last_name = form_data.get('lastName')
    dob = form_data.get('dob')

    hashed_password = pbkdf2_sha256.hash(password)

    staff = {
        'email': email,
        'staff_id': staff_id,
        'password': hashed_password,
        'f_name': first_name,
        'l_name': last_name,
        'dob': dob
    }

    return db_handler.insert_staff(staff)


def register_admin(form_data):
    email = form_data.get('email')
    admin_id = form_data.get('adminId')

    admin = {
        'email': email,
        'admin_id': admin_id
    }

    return db_handler.insert_admin(admin)


@app.route('/sale_booster')
def sale_booster():
    cursor = cnx.cursor()
    cursor.execute('SELECT item_id, item_name, category, price_kg, stock, discount_rate FROM item')
    # get all records to tuples
    rows = cursor.fetchall()
    # Close the cursor
    cursor.close()
    return render_template('sale_booster.html', rows=rows)


@app.route('/sale_booster_setup/<int:item_id>')
def sale_booster_setup(item_id):
    cursor = cnx.cursor()
    # %s --> placeholder for item_id (prevent from SQL injection)
    cursor.execute('SELECT item_name, category, price_kg FROM item WHERE item_id = %s', (item_id,))
    item_row = cursor.fetchone()
    # unpack values to variables
    item_name, category, price_per_kg = item_row
    cursor.execute('SELECT ROUND(COUNT(*) / 7, 0) AS mean_orders_count_past_7_days FROM purchase WHERE item_id = %s AND sale_date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) AND DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY);', (item_id,))
    mean_customers_past_7_days = cursor.fetchone()[0]
    mean_customers_past_7_days = int(Decimal(mean_customers_past_7_days))

    # Close the cursor
    cursor.close()

    # adjust the discount range
    discount_range = np.arange(-40, 41)
    sales = []

    column_values = sales_pred_columns.values
    print(column_values)

    # Find the index of 'unit_selling_price_rmb/kg' in the array
    unit_price_index = np.where(column_values == 'unit_selling_price_rmb/kg')[0][0]

    for discount in discount_range:
        # decimal to float
        price_per_kg_float = float(Decimal(price_per_kg))
        discount_amount = price_per_kg_float * (discount / 100)

        # process the input data
        input_data = np.zeros((1, 131))
        input_data[0, unit_price_index] = price_per_kg_float + discount_amount

        item_name_index = None
        category_index = None

        for idx, value in enumerate(column_values):
            if value == f'item_name_{item_name}':
                item_name_index = idx
            elif value == f'category_name_{category}':
                category_index = idx

        if item_name_index is None or category_index is None:
            return render_template('item_not_available.html', item_name=item_name, category=category)

        input_data[0, item_name_index] = 1
        input_data[0, category_index] = 1

        # get predictions
        prediction = sales_pred_model.predict(input_data)
        prediction = prediction * mean_customers_past_7_days
        sales.append(prediction[0][0])

    # plot sales with discount percentage
    plt.figure(figsize=(15, 6))
    plt.plot(discount_range, sales, marker='o', linestyle='-', color='b')
    plt.xlabel('Additional Price Percentage (%)')
    plt.ylabel('Sales (kg)')
    plt.title('Sales vs Additional Price Percentage')
    plt.grid(True)
    integer_ticks = np.arange(np.ceil(discount_range.min()), np.floor(discount_range.max()) + 1, 5, dtype=int)
    plt.xticks(integer_ticks)
    # save the plot
    plt.savefig('static/assets/images/sales_vs_discount.png')
    plt.close()

    return render_template('sale_booster_setup.html', item_id=item_id, item_name=item_name, category=category)


@app.route('/update_discount', methods=['POST'])
def update_discount():
    cursor = cnx.cursor()
    # get the discount percentage and item_id from the form data
    discount_percentage = request.form.get('discount_percentage')
    item_id = request.form.get('item_id')

    discount_percentage = float(discount_percentage)

    # update the database with
    cursor.execute('UPDATE item SET discount_rate = %s WHERE item_id = %s', (discount_percentage, item_id))
    cnx.commit()

    # Redirect to the sale_booster route after the update
    return redirect(url_for('sale_booster'))


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/item')
def item():
    return render_template('staff.html')


@app.route('/loss_rate_model', methods=['GET', 'POST'])
def loss_rate_model():
    if request.method == 'POST':
        # Get form data
        item_name = request.form['item_name']
        category_name = request.form['category_name']
        month = int(request.form['Month'])
        unit_selling_price = float(request.form['unit_selling_price_rmb/kg'])
        wholesale_price = float(request.form['wholesale_price_(rmb/kg)'])

        column_values = sales_pred_columns.values
        unit_price_index = np.where(column_values == 'unit_selling_price_rmb/kg')[0][0]

        # process the input data
        input_data = np.zeros((1, 131))
        input_data[0, unit_price_index] = unit_selling_price
        item_name_index = None
        category_index = None

        for idx, value in enumerate(column_values):
            if value == f'item_name_{item_name}':
                item_name_index = idx
            elif value == f'category_name_{category_name}':
                category_index = idx

        if item_name_index is None or category_index is None:
            return render_template('item_not_available.html', item_name=item_name, category=category_name)

        input_data[0, item_name_index] = 1
        input_data[0, category_index] = 1

        # get predictions
        pred_sale = sales_pred_model.predict(input_data)
        cursor = cnx.cursor()
        cursor.execute('SELECT item_id FROM item where item_name = %s and category = %s', (item_name, category_name))
        item_id = cursor.fetchone()[0]
        cursor.execute('SELECT ROUND(COUNT(*) / 30, 0) AS mean_orders_count_past_7_days FROM purchase WHERE item_id = %s AND sale_date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) AND DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY);',(item_id,))
        mean_customers_past_30_days = cursor.fetchone()[0]
        total_sales = pred_sale * int(Decimal(mean_customers_past_30_days))

        # Load the column names used during training
        column_loss_rate_values = columns_loss_rate.values

        month_index = np.where(column_loss_rate_values == 'Month')[0]
        unit_price_index = np.where(column_loss_rate_values == 'unit_selling_price_rmb/kg')[0]
        whole_price_index = np.where(column_loss_rate_values == 'wholesale_price_(rmb/kg)')[0]
        tot_sales_index = np.where(column_loss_rate_values == 'total_sales')[0]

        input_data = np.zeros((1, 185))
        input_data[0, month_index] = month
        input_data[0, unit_price_index] = unit_selling_price
        input_data[0, whole_price_index] = wholesale_price
        input_data[0, tot_sales_index] = total_sales

        item_name_index = None
        category_index = None

        for idx, value in enumerate(column_loss_rate_values):
            if value == f'item_name_{item_name}':
                item_name_index = idx
            elif value == f'category_name_{category_name}':
                category_index = idx
        if item_name_index is None or category_index is None:
            return render_template('item_not_available.html', item_name=item_name, category=category_name)

        input_data[0, item_name_index] = 1
        input_data[0, category_index] = 1

        with open('../loss_rate_analysis/lossRatemodel.pickle', 'rb') as file:
            loss_rate_model = pickle.load(file)

            # Perform prediction
            prediction = loss_rate_model.predict(input_data)

            # Generate discount based on the loss rate prediction
            discount_percentage = calculate_discount(prediction[0])

            # Render the result.html template with the predicted value and generated discount
            return render_template('loss_rate_model.html', loss_rate_prediction=prediction[0],
                                   discount_percentage=discount_percentage)

    elif request.method == 'GET':
    # Code to render the form initially
        return render_template('loss_rate_model.html')


def calculate_discount(loss_rate_prediction):
    # Example logic to generate discount based on the loss rate prediction
    if loss_rate_prediction > 0.5:
        return 20  # 20% discount for high predicted loss rate
    elif loss_rate_prediction > 0.2:
        return 10  # 10% discount for moderate predicted loss rate
    else:
        return 5  # 5% discount for low predicted loss rate
@app.route('/staff')
def staff():
    cursor = cnx.cursor()
    cursor.execute('SELECT staff_id, email, f_name, l_name, dob FROM staff')
    # get all records to tuples
    rows = cursor.fetchall()
    return render_template('staff.html', rows=rows)


@app.route('/delete_staff', methods=['POST'])
def delete_staff():
    staff_id = request.form['staff_id']
    cursor = cnx.cursor()
    # Implement database deletion logic here
    cursor.execute('DELETE FROM staff WHERE staff_id = %s', (staff_id,))
    cnx.commit()
    return redirect(url_for('staff'))


@app.route('/update_staff', methods=['POST'])
def update_staff():
    staff_id = request.form['staff_id']
    email = request.form['email']
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    dob = request.form['dob']
    cursor = cnx.cursor()

    cursor.execute('UPDATE staff SET email=%s, f_name=%s, l_name=%s, dob=%s WHERE staff_id=%s',
                   (email, f_name, l_name, dob, staff_id))
    cnx.commit()

    return redirect(url_for('staff'))


@app.route('/discount')
def discount():
    user_email = session.get('user_email')
    cursor = cnx.cursor()
    query = "SELECT p.item_id, p.quantity_kg, i.item_name, i.category FROM purchase AS p JOIN item AS i ON p.item_id = i.item_id WHERE p.email = %s ORDER BY p.sale_date DESC LIMIT 1;"
    cursor.execute(query, ('customer@example.com',))
    latest_purchase = cursor.fetchone()
    cursor.close()
    if latest_purchase is None:
        return "No purchase records found."

    item_id, quantity_kg, item_name, category = latest_purchase
    current_time = datetime.datetime.now()
    current_hour = current_time.hour
    column_values = sales_pred_columns.values

    # process the input data
    input_data = np.zeros((1, 185))
    input_data[0, 0] = int(current_hour)
    input_data[0, 1] = int(Decimal(quantity_kg))

    item_name_index = None
    category_index = None
    for idx, value in enumerate(column_values):
        if value == f'item_name_{item_name}':
            item_name_index = idx
        elif value == f'category_name_{category}':
            category_index = idx

    if item_name_index is None or category_index is None:
        return render_template('item_not_available.html', item_name=item_name, category=category)

    input_data[0, item_name_index] = 1
    input_data[0, category_index] = 1

    # get predictions
    prediction = time_based_model.predict(input_data)
    print(prediction)
    return render_template('discount.html')


@app.route('/update_discount', methods=['POST'])
def update_discount_route():
    item_id = request.form['item_id']
    discount_rate = request.form['discount_rate']

    cursor = cnx.cursor()
    cursor.execute('UPDATE item SET discount_rate=%s WHERE item_id=%s', (discount_rate, item_id))
    cnx.commit()

    return redirect(url_for('discount'))


@app.route('/personalised_discount_package')
def personalised_discount_package():
    user_email = session.get('user_email')
    cursor = cnx.cursor()
    query = "SELECT p.item_id, p.quantity_kg, i.item_name, i.category FROM purchase AS p JOIN item AS i ON p.item_id = i.item_id WHERE p.email = %s ORDER BY p.sale_date DESC LIMIT 1;"
    cursor.execute(query, (user_email,))
    latest_purchase = cursor.fetchone()
    if latest_purchase is None:
        return "No purchase records found."
    item_id, quantity_kg, item_name, category = latest_purchase
    purchase = [item_name, category, quantity_kg]
    purchase_array = np.array([purchase])
    pred_cluster = cust_pref_model.predict(purchase_array, categorical=[0, 1])

    # Selecting ten items randomly using the dataset
    count = 0
    discount_item_names = []
    while count < 10:
        random_item_name = np.random.choice(cluster_data['item_name'])
        if (cluster_data[cluster_data['item_name'] == random_item_name]['cluster'].values[0] != pred_cluster) and (random_item_name not in discount_item_names):
            count += 1
            discount_item_names.append(random_item_name)

    #the item names are used to get the item from the database
    selected_items = []
    for item_name in discount_item_names:
        cursor.execute('SELECT item_name, price_kg, image_path FROM item WHERE item_name = %s', (item_name,))
        item_data = cursor.fetchone()
        selected_items.append(item_data)
    cursor.close()

    print(f"Fetched {len(selected_items)} items for discounts.")
    print("Details of selected items for discounts:")
    for item in selected_items:
        if item:  # Check if item is not None
            item_name, price_kg, image_path = item
            print(f"Item Name: {item_name}, Price/kg: {price_kg}, Image Path: {image_path}")
        else:
            print("An item's details could not be fetched.")

    return render_template('personalised_discount_package.html', rows=selected_items)


if __name__ == '__main__':
    app.run(debug=True)