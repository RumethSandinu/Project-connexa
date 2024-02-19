from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle
import mysql.connector
import tensorflow as tf
from decimal import Decimal


model = tf.keras.models.load_model('../sales_analysis/sales_prediction_model')

app = Flask(__name__)

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


@app.route('/sale_booster')
def sale_booster():
    if cnx.is_connected():
        print('Connected to database')
    else:
        print('Error connecting to database:', cnx.connect_error)
    cursor.execute('SELECT item_id, item_name, category, price_per_kg, quantity_kg, discount_rate FROM item')
    # get all records to tuples
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return render_template('sale_booster.html', rows=rows)


# item_id is passed as an argument to the function as dynamic part of the URL
@app.route('/sale_booster_setup/<int:item_id>')
def sale_booster_setup(item_id):
    # %s --> placeholder for item_id
    cursor.execute('SELECT item_name, category, price_per_kg FROM item WHERE item_id = %s', (item_id,))
    item_row = cursor.fetchone()
    # unpack values to variables
    item_name, category, price_per_kg = item_row

    discount_range = np.arange(-30, 31)

    for discount in discount_range:
        # decimal to float
        price_per_kg_float = float(Decimal(str(price_per_kg)))
        discount_amount = price_per_kg_float * (discount / 100)
    return render_template('sale_booster_setup.html', item_id=item_id, item_name=item_name, category=category)


@app.route('/blog')
def blog():
    return render_template('blog.html')


# Load the trained model
with open('../loss_rate_analysis/lossRatemodel.pickle', 'rb') as file:
    model = pickle.load(file)


@app.route('/model', methods=['POST'])
def model():
    if request.method == 'POST':
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

         # Create a DataFrame for prediction
        input_data = pd.DataFrame({
            'Month': [month],
            'quantity_sold_kg': [quantity_sold_kg],
            'unit_selling_price_rmb/kg': [unit_selling_price],
            'wholesale_price_(rmb/kg)': [wholesale_price],
            'total_sales': [total_sales],
            'category_name': [category_name],
            'item_name': [item_name],
            'discount_Yes': [1] if discount == 'Yes' else [0],
            'sale_or_return_Return': [1] if sale_or_return == 'Return' else [0]
        })

         # Make prediction
        loss_rate_prediction = model.predict(input_data)

         # Render the result in the model.html file
        return render_template('model.html', loss_rate_prediction=loss_rate_prediction[0])


if __name__ == '__main__':
    app.run(debug=True)