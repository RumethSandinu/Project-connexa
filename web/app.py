from flask import Flask, render_template
import tensorflow as tf

tf.keras.models.load_model('../sales_prediction_analysis/sales_prediction_model')

app = Flask(__name__)
print(app)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__' :
    app.run(debug=True)
