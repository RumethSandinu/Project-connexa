from flask import Flask, render_template, request, url_for, redirect, session
# import tf_keras as tf
import pickle
import pandas as pd
import numpy as np
import mysql.connector
from decimal import Decimal
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from blueprints.db_handler import DatabaseHandler
import datetime

with open('../customer_preference_analysis/cluster_model.pkl', 'rb') as prf_model_file:
    cust_pref_model = pickle.load(prf_model_file)

with open('../time_based_analysis/TimeBasedAnalysis.pickle', 'rb') as tb_model_file:
    time_based_model = pickle.load(tb_model_file)

with open('../loss_rate_analysis/lossRatemodel.pickle', 'rb') as file:
    model = pickle.load(file)

# sales_pred_model = tf.models.load_model('../sales_analysis/sales_prediction_model')

cluster_data = pd.read_csv('../customer_preference_analysis/model_building.csv')
sales_pred_columns = pd.read_csv('../sales_analysis/column_names')
time_model = pd.read_csv('../time_based_analysis/time_model.csv')

app = Flask(__name__)

db_handler = DatabaseHandler()
cnx = mysql.connector.connect(user='root', password='', host='localhost', database='connexa')

if cnx.is_connected():
    print('Connected to database')
else:
    print('Error connecting to database:', cnx.connect_error)

@app.route('/')
def index():
    return render_template('index.html')


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
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        # Authenticate user
        user_data = authenticate_user(email, password)

        if user_data:
            # User authentication successful, store user data in session
            session['user_email'] = user_data[0]
            session['user_type'] = determine_user_type(email)

            # Redirect to a protected route or dashboard
            return redirect(url_for('dashboard'))

        # If authentication fails, show an error message
        error_message = "Invalid email or password. Please try again."
        return render_template('Register.html', error_message=error_message)

    # If the request method is GET, render the login form
    return render_template('login.html')


def authenticate_user(email, password):
    # Determine user type based on the email domain
    user_type = determine_user_type(email)

    # Authenticate user based on user type
    if user_type == 'customer':
        return db_handler.authenticate_customer(email, password)
    elif user_type == 'staff':
        return db_handler.authenticate_staff(email, password)
    elif user_type == 'admin':
        return db_handler.authenticate_admin(email, password)

    return None


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
def register(pbkdf2_sha256=None):
    result = None
    if request.method == 'POST':
        user_type = request.form.get('userType')

        if user_type == 'customer':
            result = register_customer(request.form, pbkdf2_sha256=pbkdf2_sha256)
        elif user_type == 'staff':
            result = register_staff(request.form, pbkdf2_sha256=pbkdf2_sha256)
        elif user_type == 'admin':
            result = register_admin(request.form)
        else:
            print("hello")

        if result:
            return redirect(url_for('login'))  # Redirect to login page after successful registration

    elif request.method == 'GET':
        # Code to render the form initially
        return render_template('Register.html')

    return render_template('Register.html')


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

    # Find the index of 'unit_selling_price_rmb/kg' in the array
    unit_price_index = np.where(column_values == 'unit_selling_price_rmb/kg')[0][0]

    for discount in discount_range:
        # decimal to float
        price_per_kg_float = float(Decimal(price_per_kg))
        discount_amount = price_per_kg_float * (discount / 100)

        # process the input data
        input_data = np.zeros((1, 155))
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

# Assuming 'model' is your machine learning model


@app.route('/loss_rate_model', methods=['GET', 'POST'])
def loss_rate_model():
    if request.method == 'POST':
        try:
            # Get form data
            month = int(request.form['Month'])
            quantity_sold_kg = float(request.form['quantity_sold_kg'])
            unit_selling_price = float(request.form['unit_selling_price_rmb/kg'])
            wholesale_price = float(request.form['wholesale_price_(rmb/kg)'])
            total_sales = float(request.form['total_sales'])
            category_name = request.form['category_name']
            item_name = request.form['item_name']
            discount = request.form['discount']
            sale_or_return = request.form['sale_or_return']

            # Load the column names used during training
            columns_loss_rate = pd.read_csv('../loss_rate_analysis/column_names.csv')
            column_loss_rate_values = columns_loss_rate.values.flatten()

            # Debugging print statement to check loaded column names
            print("Column names used during training:", column_loss_rate_values)

            # Adjusting required columns based on encoding
            required_columns = [
                f'category_name_{category_name}',
                f'item_name_{item_name}',
                f'discount_{discount}',
                f'sale_or_return_{sale_or_return}'
            ]

            # Debugging print statement to check required columns
            print("Required columns:", required_columns)

            # Check if all required columns are present
            if not all(col in column_loss_rate_values for col in required_columns):
                raise ValueError("One or more required columns not found in the loaded column names.")

            # Prepare input data as a NumPy array with zeros
            print(len(column_loss_rate_values))
            input_data = np.zeros((1, len(column_loss_rate_values)))

            # Set the corresponding column values to non-zero based on the form data
            for col in required_columns:
                input_data[0, np.where(column_loss_rate_values == col)[0][0]] = 1

            # Set numerical values in the input data
            input_data[0, 0] = month
            input_data[0, 1] = quantity_sold_kg
            input_data[0, 2] = unit_selling_price
            input_data[0, 3] = wholesale_price
            input_data[0, 4] = total_sales

            # Debugging print statement to check loaded column names
            print("Column names used during training:", column_loss_rate_values)

            # Debugging print statement to check received form data
            print("Received form data:", input_data)

            # Debugging print statements to check missing columns
            missing_columns = [col for col in required_columns if col not in column_loss_rate_values]
            print("Missing columns:", missing_columns)

            # Load the trained model and label encoder
            with open('../loss_rate_analysis/lossRatemodel.pickle', 'rb') as file:
                loss_rate_model = pickle.load(file)
            # Check if the loaded model is an instance of LinearRegression
            if isinstance(loss_rate_model, LinearRegression):
                # Perform prediction
                prediction = loss_rate_model.predict(input_data)

                # Print the prediction
                print("Prediction:", prediction)

                # Render the result.html template with the predicted value
                return render_template('loss_rate_model.html', loss_rate_prediction=prediction[0])

            else:
                print("The loaded object is not a LinearRegression model. Check the model file.")
                # Handle the case where the loaded model is not a LinearRegression model
                return render_template('error.html', error_message="Invalid model type")

        except Exception as e:
            # Handle the exception, e.g., log the error, show an error message, or redirect to an error page
            print(f"Error processing form data: {e}")
            return render_template('error.html', error_message=str(e))

    elif request.method == 'GET':
        # Code to render the form initially
        return render_template('loss_rate_model.html')


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
    cursor = cnx.cursor()
    cursor.execute('SELECT item_id, item_name, category, description, price_kg, stock, discount_rate, image_path FROM item')
    # get all records to tuples
    rows = cursor.fetchall()
    current_time = datetime.datetime.now()
    current_hour = current_time.hour
    return render_template('discount.html', rows=rows)



# discount_rates = {
#     0: 0.1,  # Discount rate for cluster 0
#     1: 0.15,  # Discount rate for cluster 1
#     2: 0.2,  # Discount rate for cluster 2
#     3: 0.25  # Discount rate for cluster 3
# }
#
# @app.route('/discount', methods=['GET','POST'])
# def discount():
#     if request.method == 'POST':
#         try:
#             # Get from data
#             item_time = int(request.form['time'])
#             item_quantity_sold_kg = float(request.form['quantity_sold_kg'])
#             item_category_name = request.form['category_name']
#             discount_item_name = request.form['item_name']
#
#             # Load the column names
#             item_column_names = pd.read_csv('../time_based_analysis/item_columns_names.csv')
#             item_column_name_values = item_column_names.values.flatten()
#
#             print("Column name used during training:", item_column_name_values)
#
#             # Adjust required columns
#             dis_rate_required_col = [
#                 f'item_name_{discount_item_name}',
#                 f'category_name_{item_category_name}'
#             ]
#
#             print("Required columns:", dis_rate_required_col)
#
#             if not all(colu in item_column_name_values for colu in dis_rate_required_col):
#                 raise ValueError("Bla bla")
#
#             # Input data as numpy array
#             print(len(item_column_name_values))
#             item_input_data = np.zeros((1, len(item_column_name_values)))
#
#             for colu in dis_rate_required_col:
#                 item_input_data[0, np.where(item_column_name_values == colu)[0][0]] = 1
#
#             # Set numerical values
#             item_input_data[0, 0] = item_time
#             item_input_data[0, 1] = item_quantity_sold_kg
#
#             print(" used column name during train:", item_column_name_values)
#
#             print("Received data:", item_input_data)
#
#             cluster = time_based_model.predict(item_input_data)[0]
#
#             # Assign discount rate based on cluster
#             discount_rate = discount_rates[cluster]
#
#             return render_template('discount_rate.html', discount_rate=discount_rate)
#
#         except Exception as e:
#             print(f'Error processing data: {e}')
#             return render_template("item_error.html")
#
#
#     elif request.method == 'GET':
#         return render_template('discount.html')

@app.route('/discount_package')
def discount_package():  #discount_package.html in index?
    cursor = cnx.cursor() #getting the latest data
    query = 'SELECT item_name, category, quantity_kg FROM purchase ORDER BY sale_date DESC LIMIT 1'
    cursor.execute(query)
    latest_purchase = cursor.fetchone()

    if latest_purchase is None:
        return "No purchase records found."

    purchase_data = [(latest_purchase['item_name'], latest_purchase['category'], latest_purchase['quantity_kg'])]

    # Predict cluster for the purchase data
    pred_cluster = cust_pref_model.predict(purchase_data)

    # Selecting ten items randomly using the dataset
    count = 0
    discount_item_names = []
    while count < 10:
        random_item_name = np.random.choice(cluster_data['item_name'])
        if (cluster_data[cluster_data['item_name'] == random_item_name]['cluster'].values[0] != pred_cluster) and (
                random_item_name not in discount_item_names):
            count += 1
            discount_item_names.append(random_item_name)

    #the item names are used to get the item from the database
    selected_items= []
    for item_name in discount_item_names:
        cursor.execute('SELECT item_name, price_kg,image_path FROM item WHERE item_name = %s', (item_name,))
        item_data = cursor.fetchone()
        selected_items.append(item_data)
    cursor.close()
    return render_template('discount_package.html', rows=selected_items)


if __name__ == '__main__':
    app.run(debug=True)