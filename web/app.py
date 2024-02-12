from flask import Flask, render_template, request
import pandas as pd
import pickle
import tensorflow as tf

# tf.keras.models.load_model('../sales_analysis/sales_prediction_model')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


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