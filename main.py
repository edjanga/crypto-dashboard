from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index(name='Home'):
    return render_template('index.html',content=name)

@app.route('/live-prices')
def live_prices(name='Live prices'):
    return render_template('live-prices.html',content=name)

@app.route('/top-performers')
def top(name='Top Performers'):
    return render_template('top-performers.html',content=name)

@app.route('/bottom-performers')
def bottom(name='Bottom Performers'):
    return render_template('bottom-performers.html',content=name)

@app.route('/correlation')
def correlation(name='correlation'):
    return render_template('correlation.html',content=name)

@app.route('/analytics')
def analytics(name='analytics'):
    return render_template('analytics.html',content=name)


if __name__ == '__main__':
    app.run()