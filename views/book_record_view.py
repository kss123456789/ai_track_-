from flask import render_template, Blueprint, request, session, redirect, flash, url_for
from models import *
import datetime

bp = Blueprint('record', __name__, url_prefix="/record")

def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@bp.route('/<int:book_id>')
def borrow(book_id):
    if not session.get('user_id'):
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))
    else:
        book_info = BookList.query.filter(BookList.book_id==book_id).first()
        user_id = session['user_id']
        record_info = Record.query.filter(Record.user_id==user_id, Record.book_id==book_id, Record.last_date==None).all()
        if book_info.stock<1:
            flash("재고가 없습니다!")
            return redirect(url_for('main.home'))
        elif record_info:
            flash("이미 대출 중인 책입니다!")
            return redirect(url_for('main.home'))
        else:
            book_info.stock += -1
            new_record = Record(user_id=user_id, book_id=book_id, first_date=now())
            db.session.add(new_record)
            db.session.commit()
            flash("대여성공!")
            return redirect(url_for('main.home'))

@bp.route("/borrow_list/<string:user_id>")
def borrow_list(user_id):
    if not session.get('user_id'):
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))
    else:
        record_list = Record.query.filter(Record.user_id==user_id, Record.last_date==None).all()
        if not record_list:
            flash("대여 중인 책이 없습니다.")
        return render_template("borrow_list.html", record_list=record_list)

@bp.route("/back/<int:record_id>")
def back(record_id):
    if not session.get('user_id'):
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))
    else:
        back = Record.query.filter(Record.record_id==record_id).first()
        book_info = back.booklist
        book_info.stock += 1
        back.last_date=now()
        db.session.commit()
        flash("반납이 완료되었습니다.")
        return redirect(url_for("record.borrow_list", user_id=session['user_id']))

@bp.route("/record/<string:user_id>")
def record(user_id):
    if not session.get('user_id'):
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))
    else:
        page = request.args.get('page', type=int, default=1)
        record_list = Record.query.filter(Record.user_id==user_id, Record.last_date!=None).all()
        record_page = Record.query.filter(Record.user_id==user_id, Record.last_date!=None).order_by(Record.last_date.desc()).paginate(page, per_page=8)
        if not record_list:
            flash("대여기록이 없습니다.")
        return render_template("record.html", record_page=record_page)
