from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('one.html')

@app.route("/2")
def index2():
    return render_template('two.html')

@app.route('/3', methods=['GET', 'POST'])
def index3():
    return render_template('three.html')

@app.route('/4', methods=['GET', 'POST'])
def index4():
    return render_template('four.html')


if __name__ == "__main__":
    app.run(debug=True)


