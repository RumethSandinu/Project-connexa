from flask import Flask, render_template
import pickle


model = pickle.load(open('/Users/rumethsandinu/Study/Assessments/Year 2/DSGP/Project-connexa/Rumeth/saved model/model.pickle','rb'))
app = Flask(__name__)
print(app)

@app.route('/')
def index():
    return render_template("index.html")