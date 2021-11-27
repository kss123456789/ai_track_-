from flask import render_template, Blueprint, request, session, redirect, flash, url_for
from models import *
from flask_bcrypt import Bcrypt

bp = Blueprint('main', __name__, url_prefix='/')
bcrypt = Bcrypt()

@bp.route("/")
def home():
    page = request.args.get('page', type=int, default=1)
    book_list = BookList.query.order_by(BookList.book_id.asc()).paginate(page, per_page=8)
    return render_template("main.html", book_list=book_list)

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 중복확인
        user_data = User.query.filter_by(id=request.form['user_id']).first()
        if not user_data:
            if not request.form['password']==request.form['password2']:
                flash("비밀번호가 일치하지 않습니다.")
                return redirect(url_for("main.register"))
            user_id = request.form['user_id']
            pw_hash = bcrypt.generate_password_hash(request.form['password'])
            name = request.form['name']
            user = User(id=user_id, pw=pw_hash, name=name)
            db.session.add(user)
            db.session.commit()
            flash("Elice Library의 회원이 되신 것을 환영합니다!")
            return redirect(url_for('main.home'))
        else:
            flash("이미 가입된 아이디입니다.")
            return redirect(url_for('main.register'))
    else:
        return render_template("register.html")

@bp.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_pw = request.form['password']
        user_data = User.query.filter(User.id==user_id).first()
        if not user_data:
            flash("아이디 혹은 비밀번호를 확인해 주세요.")
            return redirect(url_for('main.login'))
        elif not bcrypt.check_password_hash(user_data.pw, user_pw):
            flash("아이디 혹은 비밀번호를 확인해 주세요.")
            return redirect(url_for('main.login'))
        else:
            session.clear()
            session['user_id'] = user_id
            flash("로그인 성공!")
            return redirect(url_for('main.home'))
    else:
        return render_template("login.html")

@bp.route("/logout")
def logout():
    if not session.get('user_id'):
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))
    else:
        session.clear()
        flash("로그아웃 성공!")
        return redirect(url_for('main.home'))