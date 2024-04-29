from flask import current_app as app
from flask import render_template, request, redirect, url_for
from models import *
import datetime
import tasks

logged_libr="mohakk.mk@gmail.com"
logged_user="mohakk.mk@gmail.com"

def auto_revoke():
    reqs=Request.query.filter(Request.request_status=="issued")
    for req in reqs:
        datetime_obj = datetime.datetime.strptime(req.request_issue_date, "%Y-%m-%d %H:%M:%S.%f")
        if (datetime.datetime.now()-datetime_obj).days>7:
            req.request_status="returned"
            User.query.get(req.user_email).user_num_requests-=1
            db.session.commit()



@app.route("/celery_func")
def celery_func():
    job=tasks.func.apply_async(["Mohak"])
    return str(job), 200


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/libr_login", methods=["GET","POST"])
def libr_login():
    global logged_libr
    if request.method=="GET":
        return render_template("libr_login.html", error=None)
    email=request.form.get("libr_email")
    password=request.form.get("libr_password")
    libr=Librarian.query.filter(Librarian.libr_email==email).first()
    if libr:
        if libr.libr_password==password:
            logged_libr=libr.libr_email
            return redirect(url_for("libr_dash"))
        else:
            return render_template("libr_login.html", error="Password error")
    else:
        return render_template("libr_login.html", error="email error")
    
@app.route("/user_login", methods=["GET","POST"])
def user_login():
    global logged_user
    if request.method=="GET":
        return render_template("user_login.html", error=None)
    email=request.form.get("user_email")
    password=request.form.get("user_password")
    user=User.query.filter(User.user_email==email).first()
    if user:
        if user.user_password==password:
            logged_user=user.user_email
            user.user_login_date=str(datetime.datetime.today().date())
            return redirect(url_for("user_dash"))
        else:
            return render_template("user_login.html", error="Password error")
    else:
        return render_template("user_login.html", error="email error")
    

@app.route("/user_register", methods=["GET","POST"])
def user_register():
    global logged_user
    if request.method=="GET":
        return render_template("user_register.html", error=None)
    email=request.form.get("user_email")
    password=request.form.get("user_password")
    user=User.query.filter(User.user_email==email).first()
    if user:
        return render_template("user_register.html", error="Email already exists")
    else:
        return render_template("user_register.html", error="email error")

# from weasyprint import HTML
@app.route("/monthly_report")
def monthly_report():
    users=User.query.filter().all()
    for user in users:
        message=render_template("monthly_report.html", user=User.query.get("mohakk.mk@gmail.com"), books=Book.query.all())
        # html=HTML(string=message)
        # file_name=user.user_email+".pdf"
        # html.write_pdf(target=file_name)
        print("MONTHLY_REPORT")
        return ("MONTHLY_REPORT")


@app.route("/libr_dash")
def libr_dash():
    if not logged_libr:
        return redirect(url_for("libr_login"))
    librarian=Librarian.query.filter(Librarian.libr_email==logged_libr).first()
    name=librarian.libr_name
    email=librarian.libr_email
    sections=Section.query.all()
    return render_template("libr_dash.html", name=name, email=email, sections=sections)


@app.route("/user_search", methods=["GET", "POST"])
def user_search():
    results=None
    content=None
    if not logged_user:
        return redirect("user_login")
    if request.method=="POST":
        parameter=request.form.get("parameter")
        search_string=request.form.get("search_string")
        if parameter=="section_title":
            results=Section.query.filter(Section.section_title.like(f"%{search_string}%")).all()
            content="section"
        if parameter=="book_authors":
            results=Book.query.filter(Book.book_authors.like(f"%{search_string}%")).all()
            content="book"
        if parameter=="section_description":
            results=Section.query.filter(Section.section_description.like(f"%{search_string}%")).all()
            content="section"
        if parameter=="book_availability":
            results=Book.query.filter(Book.book_issue_flag==0).all()
            content="book"
        if parameter=="book_name":
            results=Book.query.filter(Book.book_name.like(f"%{search_string}%")).all()
            content="book"
        # section author description available name
    return render_template("user_search.html", results=results, content=content)

@app.route("/user_dash")
def user_dash():
    auto_revoke()
    if not logged_user:
        return redirect(url_for("libr_login"))
    user=User.query.filter(User.user_email==logged_user).first()
    name=user.user_name
    email=user.user_email
    sections=Section.query.all()
    issue_flag=False
    if user.user_num_requests<5:
        issue_flag=True
    return render_template("user_dash.html", name=name, email=email, sections=sections, issue_flag=issue_flag, user=user)


@app.route("/user_requests")
def user_requests():
    auto_revoke()
    if not logged_user:
        return redirect(url_for("user_login"))
    requests=Request.query.filter(Request.user_email==logged_user).all()
    books=Book.query.all()

    return render_template("user_requests.html", requests=requests, books=books)


@app.route("/user_request", methods=["GET", "POST"])
def user_request():
    if not logged_user:
        return redirect(url_for("user_login"))
    if request.method=="GET":
        book_id=request.args.get("book_id")
        user=User.query.get(logged_user)
        book=Book.query.get(book_id)
        return render_template("user_request.html",user=user, book=book)
    book_id=request.form.get("book_id")
    user_email=request.form.get("user_email")
    existing_request=Request.query.get((user_email, book_id))
    if not existing_request:
        request_status="pending"
        request_num_days=request.form.get("days")
        new_request=Request(book_id=book_id, user_email=user_email, request_status=request_status, request_num_days=request_num_days)
        user=User.query.get(user_email)
        user.user_num_requests+=1
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for("user_dash"))
    existing_request.request_status="pending"
    user=User.query.get(logged_user)
    user.user_num_requests+=1
    db.session.commit()
    return redirect(url_for("user_dash"))
    
@app.route("/section_create", methods=["GET", "POST"])
def section_create():
    if not logged_libr:
        return redirect(url_for("libr_login"))
    if request.method=="GET":
        return render_template("section_create.html")
    title=request.form.get("section_title")
    description=request.form.get("section_description")
    new_sec=Section(section_title=title, section_description=description)
    db.session.add(new_sec)
    db.session.commit()
    return redirect(url_for("libr_dash"))

@app.route("/book_create", methods=["GET", "POST"])
def book_create():
    if not logged_libr:
        return redirect(url_for("libr_login"))
    if request.method=="GET":
        sections=Section.query.all()
        return render_template("book_create.html", sections=sections)
    name=request.form.get("book_name")
    content=request.form.get("book_content")
    authors=request.form.get("book_authors")
    section=request.form.get("section")
    newbook=Book(book_name=name, book_content=content, book_authors=authors, section_title=section)
    db.session.add(newbook)
    db.session.commit()
    return redirect(url_for("libr_dash"))

@app.route("/section_delete", methods=["GET", "POST"])
def section_delete():
    if not logged_libr:
        return redirect(url_for("libr_login"))
    if request.method=="GET":
        sections=Section.query.all()
        return render_template("section_delete.html", sections=sections)
    title=request.form.get("section_title")
    sec=Section.query.get(title)
    for book in sec.section_books:
        delete_book_and_requests(book.book_id)
    db.session.delete(sec)
    db.session.commit()
    return redirect(url_for("libr_dash"))


def delete_book_and_requests(book_id):
    book=Book.query.get(book_id)
    user_emails=[req.user_email for req in book.book_requests if ((req.request_status=="pending") or (req.request_status=="issued"))]
    for i in user_emails:
        User.query.get(i).user_num_requests-=1
    book_requests=[req for req in book.book_requests]
    for i in book_requests:
        db.session.delete(i)
    db.session.delete(book)
    db.session.commit()
    


@app.route("/book_delete", methods=["GET", "POST"])
def book_delete():
    if not logged_libr:
        return redirect(url_for("libr_login"))
    if request.method=="GET":
        books=Book.query.all()
        return render_template("book_delete.html", books=books)
    book_id=request.form.get("book_id")
    delete_book_and_requests(book_id)
    return redirect(url_for("libr_dash"))





@app.route("/section_edit", methods=["GET", "POST"])
def section_edit():
    if not logged_libr:
        return redirect(url_for("libr_login"))
    if request.method=="GET":
        return render_template("section_edit.html", sections=Section.query.all())
    title=request.form.get("section_title")
    section=Section.query.get(title)
    description=(str(request.form.get("new_description"))).strip()
    section.section_description=description
    db.session.commit()
    return redirect(url_for("libr_dash"))



@app.route("/book_edit", methods=["GET", "POST"])
def book_edit():
    if not logged_libr:
        return redirect(url_for("libr_login"))
    if request.method=="POST":
        name=request.form.get("new_name")
        id=request.form.get("book_id")
        content=request.form.get("new_content")
        authors=request.form.get("new_authors")
        section=request.form.get("section_title")
        book=Book.query.get(id)
        book.book_name=name
        book.book_content=content
        book.book_authors=authors
        book.section_title=section
        db.session.commit()
        return redirect(url_for("libr_dash"))
    books=Book.query.all()
    sections=Section.query.all()
    return render_template("book_edit.html", books=books, sections=sections)




from sqlalchemy import func

@app.route("/admin_summary")
def admin_summary():
    auto_revoke()

    if not logged_libr:
        return redirect(url_for("user_login"))
    
    # Perform a query to count the number of requests per section
    requests_per_section = db.session.query(Section.section_title, func.count(Request.book_id)).\
        select_from(Section).\
        join(Book, Section.section_title == Book.section_title).\
        join(Request, Book.book_id == Request.book_id).\
        group_by(Section.section_title).all()
    
    # Extract the data for the chart
    section_titles = [row[0] for row in requests_per_section]
    num_requests = [row[1] for row in requests_per_section]

    books=Book.query.all()
    
    return render_template("libr_summary.html", section_titles=section_titles, num_requests=num_requests, books=books)


@app.route("/user_view")
def user_view():
    if not logged_user:
        return redirect(url_for("user_login"))
    book_id=request.args.get("book_id")
    book=Book.query.get(book_id)
    return render_template("user_view.html", book=book)


@app.route("/user_books")
def user_books():
    auto_revoke()

    if not logged_user:
        return redirect(url_for("user_login"))
    books_with_requests = db.session.query(Book, Request).join(Request).filter(Request.user_email == logged_user,Request.request_status == 'issued').all()
    books=[book for book,requests in books_with_requests]    
    return render_template("user_books.html", books=books)


@app.route("/user_feedback", methods=["GET", "POST"])
def user_feedback():
    if not logged_user:
        return redirect(url_for("user_login"))
    if request.method=="GET":
        book_id=request.args.get("book_id")
        book=Book.query.get(book_id)
        feedback=Request.query.get((logged_user, book_id)).request_feedback
        return render_template("user_feedback.html", book=book, feedback=feedback)
    else:
        book_id=request.form.get("book_id")
        feedback=request.form.get("feedback")
        Request.query.get((logged_user, book_id)).request_feedback=feedback
        db.session.commit()
        return redirect(url_for("user_dash"))
    

@app.route("/user_return")
def user_return():
    auto_revoke()

    if not logged_user:
        return redirect(url_for("user_login"))
    book_id=request.args.get("book_id")
    Book.query.get(book_id).book_issue_flag=0
    User.query.get(logged_user).user_num_requests-=1
    Request.query.get((logged_user, book_id)).request_status="returned"
    db.session.commit()
    return redirect(url_for("user_dash"))










@app.route("/grant")
def grant():
    if not logged_libr:
        return redirect(url_for("libr_dash"))
    user_email=request.args.get("user_email")
    book_id=request.args.get("book_id")
    book=Book.query.get(book_id)
    our_request=Request.query.get((user_email,book_id))
    our_request.request_status="issued"
    book.book_issue_flag=1
    our_request.request_issue_date=str(datetime.datetime.now())
    db.session.commit()
    return redirect(url_for("requests"))

@app.route("/reject")
def reject():
    if not logged_libr:
        return redirect(url_for("libr_dash"))
    user_email=request.args.get("user_email")
    user=User.query.get(user_email)
    book_id=request.args.get("book_id")
    our_request=Request.query.get((user_email,book_id))
    our_request.request_status="denied"
    user.user_num_requests-=1
    db.session.commit()
    return redirect(url_for("requests"))


@app.route("/revoke")
def revoke():
    if not logged_libr:
        return redirect(url_for("libr_dash"))
    user_email=request.args.get("user_email")
    user=User.query.get(user_email)
    book_id=request.args.get("book_id")
    our_request=Request.query.get((user_email,book_id))
    our_request.request_status="revoked"
    book=Book.query.get(book_id)
    book.book_issue_flag=0
    user.user_num_requests-=1
    db.session.commit()
    return redirect(url_for("requests"))





@app.route("/requests", methods=["GET", "POST"])
def requests():
    auto_revoke()

    if not logged_libr:
        return redirect(url_for("libr_login"))
    if request.method=="POST":
        pass
    requests=Request.query.all()
    books=Book.query.all()
    return render_template("requests.html", requests=requests, books=books)









@app.route("/logout")
def logout():
    global logged_libr
    logged_libr=None
    global logged_user
    logged_user=None
    return redirect(url_for("home"))






