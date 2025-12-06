import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from functools import wraps

app = Flask(__name__)

# --- 配置 ---
app.config['SECRET_KEY'] = 'secret_key_123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- 邮箱配置 (请在运行成功后修改这里) ---
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = '123456@qq.com'
app.config['MAIL_PASSWORD'] = 'your_token'
app.config['MAIL_DEFAULT_SENDER'] = '123456@qq.com'

# --- 汇率配置 ---
EXCHANGE_RATES = {'CNY': 1.0, 'USD': 7.25, 'HKD': 0.93, 'EUR': 7.65, 'JPY': 0.048}
CURRENCY_SYMBOLS = {'CNY': '¥', 'USD': '$', 'HKD': 'HK$', 'EUR': '€', 'JPY': 'JP¥'}

db = SQLAlchemy(app)
mail = Mail(app)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    renew_price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False, default='CNY')
    description = db.Column(db.String(200))

def check_subscriptions():
    with app.app_context():
        target_date = datetime.now() + timedelta(days=7)
        expiring_subs = Subscription.query.filter(db.func.date(Subscription.end_date) == target_date.date()).all()
        for sub in expiring_subs:
            try:
                msg = Message(f"提醒：{sub.name} 即将到期", recipients=['admin@example.com'])
                msg.body = f"{sub.name} 将于 {sub.end_date} 到期。"
                mail.send(msg)
            except: pass

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_subscriptions, trigger="interval", hours=24)
scheduler.start()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session: return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else: flash('密码错误', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    subs = Subscription.query.order_by(Subscription.end_date).all()
    total_cost = sum(s.price * EXCHANGE_RATES.get(s.currency, 1.0) for s in subs)
    total_renew = sum(s.renew_price * EXCHANGE_RATES.get(s.currency, 1.0) for s in subs)
    return render_template('dashboard.html', subs=subs, total_cost=round(total_cost, 2), 
                           total_renew=round(total_renew, 2), symbols=CURRENCY_SYMBOLS)

@app.route('/add', methods=['POST'])
@login_required
def add_subscription():
    try:
        new_sub = Subscription(
            name=request.form['name'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%dT%H:%M'),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%dT%H:%M'),
            price=float(request.form['price']),
            renew_price=float(request.form['renew_price']),
            currency=request.form.get('currency', 'CNY'),
            description=request.form.get('description', '')
        )
        db.session.add(new_sub)
        db.session.commit()
    except Exception as e: flash(str(e), 'danger')
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:id>')
@login_required
def delete_subscription(id):
    db.session.delete(Subscription.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
