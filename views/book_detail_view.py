from flask import render_template, Blueprint, request, session, redirect, flash, url_for
from models import *
import datetime

bp = Blueprint('book_detail', __name__, url_prefix="/book")

def average(book_id):
    review_info = Review.query.filter(Review.book_id==book_id).all()
    book_info = BookList.query.filter(BookList.book_id==book_id).first()
    rating_sum, average = 0, 0
    if review_info:
        for review in review_info:
            rating_sum += review.rating
        average = rating_sum / len(review_info)
    book_info.avg_rating = round(average)
    db.session.commit()

@bp.route('/<int:book_id>')
def detail(book_id):
    book_info = BookList.query.filter(BookList.book_id==book_id).first()
    reviews = Review.query.filter(Review.book_id==book_id).order_by(Review.date.desc()).all()

    return render_template("book_detail.html", book_info=book_info, reviews=reviews)

@bp.route('/write/<int:book_id>', methods=['POST'])
def write(book_id):
    if not session.get('user_id'):
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))
    else:
        # 리뷰 추가
        user_id = session['user_id']
        review = request.form['review']
        rating = request.form['rating']
        new_review = Review(book_id=book_id, user_id=user_id, review=review, rating=rating, date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))        
        db.session.add(new_review)
        db.session.commit()
        # 새로운 평균 계산
        average(book_id)      

        flash("소중한 리뷰 감사합니다.")
        return redirect(url_for('book_detail.detail', book_id=book_id))

@bp.route('/delete/<int:review_id>')
def delete(review_id):
        # 리뷰 삭제
        if not session.get('user_id'):
            flash("잘못된 접근입니다.")
            return redirect(url_for('main.home'))
        else:
            review_info = Review.query.filter(Review.review_id==review_id).first()
            book_id = review_info.book_id 
            db.session.delete(review_info)
            db.session.commit()
            # 새로운 평균 계산
            average(book_id)      
            flash("소중한 리뷰 감사합니다.")
            return redirect(url_for('book_detail.detail', book_id=book_id))