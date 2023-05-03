import asyncio
import json

from flask import redirect, url_for, flash, render_template, jsonify
from flask_bcrypt import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from server import app
from server import get_advertisement, get_user_by_username, hide_ad
from server.forms import LoginForm
from olxScraper import OlxScraper


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


@app.route('/advertisements/<string:sort>')
@login_required
def advertisements(sort):
    olx_scraper = OlxScraper()
    asyncio.run(olx_scraper.main())
    result = get_advertisement(current_user.access_category, current_user, sort)
    return json.dumps(result, ensure_ascii=False)


@app.route('/advertisements/delete/<int:ad_id>', methods=['DELETE'])
@login_required
def delete_advertisements(ad_id: int):
    hide_ad(current_user.id, ad_id)
    return jsonify({'status': 'deleted'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = get_user_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
