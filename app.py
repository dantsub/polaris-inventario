from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/productos')
def productos():
    return render_template('modules/products.html')


@app.route('/pruebas')
def pruebas():
    return render_template('/pruebas.html')


if __name__ == '__main__':
    app.run(debug=True, port=5504)
