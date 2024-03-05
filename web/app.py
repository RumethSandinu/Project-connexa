from flask import Flask, render_template, request, url_for, redirect, session
import pandas as pd
import numpy as np
import pickle
import mysql.connector

from sklearn.exceptions import NotFittedError
from sklearn.preprocessing import LabelEncoder

from blueprints.database_handler import DatabaseHandler

sales_pred_model = tf.keras.models.load_model('../sales_analysis/sales_prediction_model')

app = Flask(__name__)
db_handler = DatabaseHandler()
cnx = mysql.connector.connect(user='root', password='', host='localhost', database='connexa')
cursor = cnx.cursor()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')

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
        return render_template('login.html', error_message=error_message)

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
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        user_type = request.form.get('userType')

        if user_type == 'customer':
            result = register_customer(request.form)
        elif user_type == 'staff':
            result = register_staff(request.form)
        elif user_type == 'admin':
            result = register_admin(request.form)

        if result:
            return redirect(url_for('login'))  # Redirect to login page after successful registration

    return render_template('Register.html')

def register_customer(form_data, pbkdf2_sha256=None):
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
    if cnx.is_connected():
        print('Connected to database')
    else:
        print('Error connecting to database:', cnx.connect_error)
    cursor.execute('SELECT item_id, item_name, category, price_per_kg, quantity_kg, discount_rate FROM item')
    # get all records to tuples
    rows = cursor.fetchall()
    return render_template('sale_booster.html', rows=rows)


@app.route('/sale_booster_setup/<int:item_id>')
def sale_booster_setup(item_id):
    # %s --> placeholder for item_id
    cursor.execute('SELECT item_name, category, price_per_kg FROM item WHERE item_id = %s', (item_id,))
    item_row = cursor.fetchone()
    # unpack values to variables
    item_name, category, price_per_kg = item_row

    # adjust the discount range
    discount_range = np.arange(-30, 11)
    sales = []

    columns = pd.read_csv('../sales_analysis/column_names')
    column_values = columns.values

    # Find the index of 'unit_selling_price_rmb/kg' in the array
    unit_price_index = np.where(column_values == 'unit_selling_price_rmb/kg')[0][0]

    for discount in discount_range:
        # decimal to float
        price_per_kg_float = float(Decimal(price_per_kg))
        discount_amount = price_per_kg_float * (discount / 100)

        # process the input data
        input_data = np.zeros((1, 155))
        input_data[0, unit_price_index] = price_per_kg_float + discount_amount
        item_name_index = np.where(column_values == f'item_name_{item_name}')[0][0]
        category_index = np.where(column_values == f'category_name_{category}')[0][0]
        input_data[0, item_name_index] = 1
        input_data[0, category_index] = 1

        # get predictions
        prediction = sales_pred_model.predict(input_data)
        sales.append(prediction[0][0])

    # plot sales with discount percentage
    plt.figure(figsize=(15, 6))
    plt.plot(discount_range, sales)
    plt.xlabel('Additional Price Percentage (%)')
    plt.ylabel('Sales (kg)')
    plt.title('Sales vs Additional Price Percentage')
    plt.grid(True)
    integer_ticks = np.arange(np.ceil(discount_range.min()), np.floor(discount_range.max()) + 1, dtype=int)
    plt.xticks(integer_ticks)
    # save the plot
    plt.savefig('static/assets/images/sales_vs_discount.png')
    plt.close()

    return render_template('sale_booster_setup.html', item_id=item_id, item_name=item_name, category=category)


@app.route('/update_discount', methods=['POST'])
def update_discount():
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


# Load the trained model
with open('../loss_rate_analysis/lossRatemodel.pickle', 'rb') as file:
    model = pickle.load(file)

# Assuming you have a label encoder instance
label_encoder = LabelEncoder()

# Assuming 'model' is your machine learning model

@app.route('/loss_rate_model', methods=['GET', 'POST'])
def loss_rate_model():
    if request.method == 'POST':
        try:
            # Read CSV file and select only the relevant columns
            relevant_columns = ['Month', 'quantity_sold_kg', 'unit_selling_price_rmb/kg', 'wholesale_price_(rmb/kg)',
                                 'total_sales', 'category_name', 'item_name', 'discount', 'sale_or_return']
            csv_data = pd.read_csv('../../datasets/cleaned_loss_rate_dataset.csv', usecols=relevant_columns)
            # Rearrange the columns in the order specified
            csv_data = csv_data[['Month', 'quantity_sold_kg', 'unit_selling_price_rmb/kg', 'wholesale_price_(rmb/kg)',
                                 'total_sales', 'category_name', 'item_name', 'discount', 'sale_or_return']]
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

            # Store form data in a Python list
            form_data = [
                month,
                quantity_sold_kg,
                unit_selling_price,
                wholesale_price,
                total_sales,
                category_name,
                item_name,
                1 if discount == 'Yes' else 0,
                1 if sale_or_return == 'Return' else 0
            ]

            # Create a DataFrame for prediction with explicit columns and order
            input_data = pd.DataFrame([form_data], columns=relevant_columns)

            print("Input Data Columns:", input_data.columns.tolist())
            print("CSV Data Columns:", csv_data.columns.tolist())

            # Encode categorical names in the CSV data
            encoded_csv_data = csv_data.apply(lambda x: label_encoder.fit_transform(x) if x.dtype == 'O' else x)

            # Ensure that the input data and encoded CSV data match
            assert input_data.columns.tolist() == encoded_csv_data.columns.tolist(), "Input data and encoded CSV data columns do not match"

            try:
                encoded_input_data = input_data.apply(lambda x: label_encoder.transform(x) if x.dtype == 'O' else x)
            except NotFittedError as e:
                # If LabelEncoder is not fitted, fit it on the entire dataset and then transform the input data
                label_encoder.fit(encoded_csv_data.astype(str))
                encoded_input_data = input_data.apply(lambda x: label_encoder.transform(x) if x.dtype == 'O' else x)

            print(encoded_csv_data)
            print(encoded_input_data)

            # Make prediction
            loss_rate_prediction = model.predict(encoded_input_data)

            # Render the result in the loss_rate_model.html file
            return render_template('loss_rate_model.html', loss_rate_prediction=loss_rate_prediction[0], form_data=form_data)

        except Exception as e:
            # Handle the exception, e.g., log the error, show an error message, or redirect to an error page
            print(f"Error processing form data: {e}")
            return render_template('error.html', error_message=str(e))

    elif request.method == 'GET':
        # Code to render the form initially
        return render_template('loss_rate_model.html')

@app.route('/staff')
def staff():
    # Fetch data from MySQL
    cursor.execute("SELECT staff_id, email, f_name, l_name, dob FROM staff")
    data = cursor.fetchall()
    columns = ['staff_id', 'email', 'f_name', 'l_name', 'dob']  # Define the columns manually
    return render_template('staff.html', data=data, columns=columns)

if __name__ == '__main__':
    app.run(debug=True)