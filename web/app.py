from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import pickle
import mysql.connector
import tensorflow as tf
from decimal import Decimal
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px


sales_pred_model = tf.keras.models.load_model('../sales_analysis/sales_prediction_model')

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