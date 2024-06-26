# -*- coding: utf-8 -*-
"""E- Commerce platform with payment integration 1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z_tTVxZAXNgFRaCwcl_cMNNjlPp3dhz0
"""

!pip install Flask stripe flask-ngrok

import stripe
from flask import Flask, render_template, jsonify, request
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

# Set your secret key: remember to change this to your live secret key in production
stripe.api_key = 'your_secret_key_here'

# Your domain name
YOUR_DOMAIN = 'http://localhost:5000'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'T-shirt',
                        },
                        'unit_amount': 2000,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
        return jsonify({
            'id': checkout_session.id
        })
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/success')
def success():
    return 'Payment succeeded!'

@app.route('/cancel')
def cancel():
    return 'Payment cancelled.'

if __name__ == '__main__':
    app.run()