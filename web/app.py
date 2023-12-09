from flask import Flask, render_template
import tensorflow as tf

tf.saved_model.load('../Rumeth/final_sold_amount_model')

app = Flask(__name__)
print(app)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__' :
    app.run(debug=True)
