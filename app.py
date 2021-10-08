from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/productos')
def productos():
    return render_template('modules/products.html')


@app.route('/login')
def login():
    return render_template('modules/login.html')


@app.route('/providers')
def providers():
    return render_template('modules/providers.html')


@app.route('/users')
def users():
    return render_template('modules/users.html')

if __name__ == '__main__':
    app.run(debug=True, port=5504)
