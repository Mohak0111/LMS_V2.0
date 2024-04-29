from flask import request,redirect,url_for,jsonify, Response
from flask import render_template
from flask import current_app as app
from models import *
from flask_jwt_extended import create_access_token, jwt_required, current_user, get_jwt_identity, get_jwt
from datetime import timedelta
import datetime
from sqlalchemy import func
from cache import cache

import matplotlib
matplotlib.use('agg')


import io
import matplotlib.pyplot as plt
# Define custom dark theme
dark_theme = {
    'axes.facecolor': '#212529',  # Background color
    'figure.facecolor': '#212529',  # Figure background color
    'axes.edgecolor': 'white',  # Axes edge color
    'axes.labelcolor': 'white',  # Label color
    'text.color': 'white',  # Text color
    'xtick.color': 'white',  # X-axis tick color
    'ytick.color': 'white',  # Y-axis tick color
}

# Apply the custom theme
plt.style.use(dark_theme)






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
    



def auto_revoke():
    reqs=Request.query.filter(Request.request_status=="issued")
    for req in reqs:
        datetime_obj = datetime.datetime.strptime(req.request_issue_date, "%Y-%m-%d %H:%M:%S.%f")
        if (datetime.datetime.now()-datetime_obj).days>7:
            req.request_status="returned"
            User.query.get(req.user_email).user_num_requests-=1
            db.session.commit()


# returns (user_type, user_id)
def get_info(token):
    return (token["user_type"], token["sub"])



@app.route("/backend/graph")
@jwt_required()
@cache.memoize(timeout=50)
def backend_graph():
    type, logged_libr=get_info(get_jwt())
    if type!="librarian":
        return jsonify({"error":"Login as librarian to access this"}), 401
    requests_per_section = db.session.query(Section.section_title, func.count(Request.book_id)).select_from(Section).join(Book, Section.section_title == Book.section_title).join(Request, Book.book_id == Request.book_id).group_by(Section.section_title).all()
    
    section_titles = [row[0] for row in requests_per_section]
    num_requests = [row[1] for row in requests_per_section]
    plt.bar(section_titles, num_requests)
    plt.xlabel('Section Title')
    plt.ylabel('Number of Requests')
    plt.title('Requests per Section')
    plt.xticks(rotation=45, ha='right')



    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return Response(img.getvalue(), mimetype='image/png')

    



@app.route('/backend/libr_login',methods=["POST"])
def backend_libr_login():
    data=request.get_json()
    email=data["libr_email"]
    password=data["libr_password"]
    libr_from_db=Librarian.query.filter(Librarian.libr_email==email).first()
    if libr_from_db:
        if password==libr_from_db.libr_password:
            expiration_time = timedelta(hours=3)
            access_token={"access_token":create_access_token(identity=email, additional_claims={"user_type":"librarian"}, expires_delta=expiration_time), 'name':libr_from_db.libr_name}
            return jsonify(access_token), 200
        else:
            error={'error':'wrong password'}
    else:
        error={'error':'unauthorized id'}
    return jsonify(error), 401



# give info to login POST
@app.route('/backend/user_login',methods=["POST"])
def backend_user_login():
    data=request.get_json()
    email=data["user_email"]
    password=data["user_password"]
    user_from_db=User.query.filter(User.user_email==email).first()
    if user_from_db:
        if password==user_from_db.user_password:
            expiration_time = timedelta(hours=3)
            user_from_db.user_login_date=str(datetime.datetime.today().date())
            db.session.commit()
            access_token={"access_token":create_access_token(identity=email, additional_claims={"user_type":"user"}, expires_delta=expiration_time), 'name':user_from_db.user_name}
            return jsonify(access_token), 200
        else:
            error={'error':'wrong password'}
    else:
        error={'error':'unauthorized id'}
    return jsonify(error), 401


# give info to register POST
@app.route("/backend/user_register", methods=["POST"])
def backend_user_register():
    data=request.get_json()
    email=data["user_email"]
    name=data["user_name"]
    password=data["user_password"]
    user=User.query.filter(User.user_email==email).first()
    if user:
        return {"error":"user already exists"}, 422
    else:
        db.session.add(User(user_name=name, user_email=email, user_password=password, user_login_date=str(datetime.datetime.today().date())))
        db.session.commit()
        expiration_time = timedelta(hours=3)
        access_token={"access_token":create_access_token(identity=email, additional_claims={"user_type":"user"}, expires_delta=expiration_time)}
        return jsonify(access_token), 200



# get data after login for dash GET
@app.route("/backend/libr_dash")
@jwt_required()
@cache.memoize(timeout=50)
def backend_libr_dash():
    type, logged_libr=get_info(get_jwt())
    if type!="librarian":
        return jsonify({"error":"Login as librarian to access this"}), 401
    librarian=Librarian.query.filter(Librarian.libr_email==logged_libr).first()
    name=librarian.libr_name
    email=librarian.libr_email
    sections=Section.query.all()
    response={"name":name, "email":email, "sections":[section.get_json() for section in sections]}
    return response, 200



# get data after login for dash GET
@app.route("/backend/user_dash")
@jwt_required()
def backend_user_dash():
    type, logged_user=get_info(get_jwt())
    if type!="user":
        return jsonify({"error":"Login as user to access this"}), 401
    user=User.query.filter(User.user_email==logged_user).first()
    name=user.user_name
    email=user.user_email
    sections=Section.query.all()
    issue_flag=False
    if user.user_num_requests<5:
        issue_flag=True
    response={"name":name, "email":email, "sections":[section.get_json() for section in sections], "issue_flag":issue_flag, "user":user.get_json()}
    return response, 200




# get search data GET
@app.route("/backend/user_search", methods=["POST"])
@jwt_required()
def backend_user_search():
    type, logged_user=get_info(get_jwt())
    if type!="user":
        return jsonify({"error":"Login as user to access this"}), 401
    data=request.get_json()
    parameter=data["parameter"]
    search_string=data["search_string"]
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
    results=[i.get_json() for i in results]
    return {"results":results, "content":content}, 200



@app.route("/backend/user_requests")
@jwt_required()
def backend_user_requests():
    auto_revoke()
    type, logged_user=get_info(get_jwt())
    if type!="user":
        return jsonify({"error":"Login as user to access this"}), 401
    requests=Request.query.filter(Request.user_email==logged_user).all()
    books=Book.query.all()

    return {"requests":[req.get_json() for req in requests], "books":[book.get_json() for book in books]}, 200



@app.route("/backend/user_request", methods=["PUT", "POST"])
@jwt_required()
def backend_user_request():
    type, logged_user=get_info(get_jwt())
    if type!="user":
        return jsonify({"error":"Login as user to access this"}), 401
    if request.method=="PUT":
        # return {"message":"okay"}
        data=request.get_json()
        book_id=data["book_id"]
        user=User.query.get(logged_user)
        book=Book.query.get(book_id)
        return {"user":user.get_json(), "book":book.get_json()}
    data=request.get_json()
    book_id=data["book_id"]
    user_email=logged_user
    existing_request=Request.query.get((user_email, book_id))
    if not existing_request:
        request_status="pending"
        request_num_days=int(data["days"])
        new_request=Request(book_id=book_id, user_email=user_email, request_status=request_status, request_num_days=request_num_days)
        user=User.query.get(user_email)
        user.user_num_requests+=1
        db.session.add(new_request)
        db.session.commit()
        return {"created_request":new_request.get_json()}, 200
    existing_request.request_status="pending"
    user=User.query.get(logged_user)
    user.user_num_requests+=1
    db.session.commit()
    return {"updated_request":existing_request.get_json()}, 200






# give data to create section POST

@app.route("/backend/section_create", methods=[ "POST"])
@jwt_required()
def backend_section_create():
    type, logged_libr=get_info(get_jwt())
    if type!="librarian":
        return jsonify({"error":"Login as librarian to access this"}), 401
    data=request.get_json()
    title=data["section_title"]
    if Section.query.get(title):
        return {"error":"section already exists"}, 409
    description=data["section_description"]
    new_sec=Section(section_title=title, section_description=description)
    db.session.add(new_sec)
    db.session.commit()
    return {"created_section":new_sec.get_json()}



@app.route("/backend/book_create", methods=["GET", "POST"])
@jwt_required()
def backend_book_create():
    type, logged_libr=get_info(get_jwt())
    if type!="librarian":
        return jsonify({"error":"Login as librarian to access this"}), 401
    if request.method=="GET":
        sections=Section.query.all()
        return {"sections":[sec.get_json() for sec in sections]}
    data=request.get_json()
    name=data["book_name"]
    content=data["book_content"]
    authors=data["book_authors"]
    section=data["section"]
    newbook=Book(book_name=name, book_content=content, book_authors=authors, section_title=section)
    db.session.add(newbook)
    db.session.commit()
    return {"book_created":newbook.get_json()}


@app.route("/backend/section_delete", methods=["GET", "POST"])
@jwt_required()
def backend_section_delete():
    type, logged_libr=get_info(get_jwt())
    if type!="librarian":
        return jsonify({"error":"Login as librarian to access this"}), 401
    if request.method=="GET":
        sections=Section.query.all()
        return {"sections":[sec.get_json() for sec in sections]}
    data=request.get_json()
    title=data["section_title"]
    sec=Section.query.get(title)
    for book in sec.section_books:
        delete_book_and_requests(book.book_id)
    db.session.delete(sec)
    db.session.commit()
    return {"section_deleted":sec.get_json()}, 200



@app.route("/backend/book_delete", methods=["GET", "POST"])
@jwt_required()
def backend_book_delete():
    type, logged_libr=get_info(get_jwt())
    if type!="librarian":
        return jsonify({"error":"Login as librarian to access this"}), 401
    if request.method=="GET":
        books=Book.query.all()
        return {"books":[book.get_json() for book in books]}
    data=request.get_json()
    book_id=data["book_id"]
    delete_book_and_requests(book_id)
    return {"book_deleted":{"book_id":book_id}}, 200



@app.route("/backend/section_edit", methods=["GET", "POST"])
@jwt_required()
def backend_section_edit():
    type, logged_libr=get_info(get_jwt())
    if type!="librarian":
        return jsonify({"error":"Login as librarian to access this"}), 401
    if request.method=="GET":
        sections=Section.query.all()
        return {"sections":[sec.get_json() for sec in sections]}
    data=request.get_json()
    title=data["section_title"]
    section=Section.query.get(title)
    description=(str(data["new_description"])).strip()
    section.section_description=description
    db.session.commit()
    return {"section_edited":section.get_json()}




@app.route("/backend/book_edit", methods=["GET", "POST"])
@jwt_required()
def backend_book_edit():
    type, logged_libr=get_info(get_jwt())
    if type!="librarian":
        return jsonify({"error":"Login as librarian to access this"}), 401
    if request.method=="POST":
        data=request.get_json()
        name=data["new_name"]
        id=int(data["book_id"])
        content=data["new_content"]
        authors=data["new_authors"]
        section=data["section_title"]
        print(data)
        book=Book.query.get(id)
        book.book_name=name
        book.book_content=content
        book.book_authors=authors
        book.section_title=section
        db.session.commit()
        return {"book_edited":book.get_json()}, 200
    books=Book.query.all()
    sections=Section.query.all()
    return {"books":[book.get_json() for book in books], "sections":[sec.get_json() for sec in sections]}



@app.route("/backend/admin_summary")
@jwt_required()
def backend_admin_summary():
    auto_revoke()
    type, logged_libr=get_info(get_jwt())
    if type!="librarian":
        return jsonify({"error":"Login as librarian to access this"}), 401
    
    requests_per_section = db.session.query(Section.section_title, func.count(Request.book_id)).select_from(Section).join(Book, Section.section_title == Book.section_title).join(Request, Book.book_id == Request.book_id).group_by(Section.section_title).all()
    
    section_titles = [row[0] for row in requests_per_section]
    num_requests = [row[1] for row in requests_per_section]

    books=Book.query.all()
    
    return {"section_titles":section_titles, "num_requests":num_requests, "books":[book.get_json() for book in books]}, 200

@app.route("/backend/user_view", methods=["POST"])
@jwt_required()
def backend_user_view():
    type, logged_user=get_info(get_jwt())
    if type!="user":
        return jsonify({"error":"Login as user to access this"}), 401
    book_id=request.get_json()["book_id"]
    book=Book.query.get(book_id)
    return {"book":book.get_json()}, 200

@app.route("/backend/user_books")
@jwt_required()
def backend_user_books():
    auto_revoke()
    type, logged_user=get_info(get_jwt())
    if type!="user":
        return jsonify({"error":"Login as user to access this"}), 401
    books_with_requests = db.session.query(Book, Request).join(Request).filter(Request.user_email == logged_user,Request.request_status == 'issued').all()
    books=[book.get_json() for book,requests in books_with_requests]    
    return {"books":books}, 200



@app.route("/backend/user_feedback", methods=["PUT", "POST"])
@jwt_required()
def backend_user_feedback():
    type, logged_user=get_info(get_jwt())
    if type!="user":
        return jsonify({"error":"Login as user to access this"}), 401
    if request.method=="PUT":
        data=request.get_json()
        book_id=data["book_id"]
        book=Book.query.get(book_id).get_json()
        feedback=Request.query.get((logged_user, book_id)).request_feedback
        return {"book":book, "feedback":feedback}, 200
    else:
        data=request.get_json()
        book_id=data["book_id"]
        feedback=data["feedback"]
        req=Request.query.get((logged_user, book_id)).get_json()
        Request.query.get((logged_user, book_id)).request_feedback=feedback
        db.session.commit()
        return {"feedback_edited":req}, 200


@app.route("/backend/user_return", methods=["PATCH"])
@jwt_required()
def backend_user_return():
    auto_revoke()
    type, logged_user=get_info(get_jwt())
    if type!="user":
        return jsonify({"error":"Login as user to access this"}), 401
    data=request.get_json()
    book_id=data["book_id"]
    Book.query.get(book_id).book_issue_flag=0
    User.query.get(logged_user).user_num_requests-=1
    Request.query.get((logged_user, book_id)).request_status="returned"
    db.session.commit()
    return {"request_returned":Request.query.get((logged_user, book_id)).get_json()}, 200




@app.route("/backend/grant", methods=["PATCH"])
@jwt_required()
def backend_grant():
    type, logged_libr=get_info(get_jwt())
    if type!="librarian":
        return jsonify({"error":"Login as librarian to access this"}), 401
    data=request.get_json()
    user_email=data["user_email"]
    book_id=data["book_id"]
    book=Book.query.get(book_id)
    our_request=Request.query.get((user_email,book_id))
    our_request.request_status="issued"
    book.book_issue_flag=1
    our_request.request_issue_date=str(datetime.datetime.now())
    reqs = Request.query.filter(Request.book_id==book_id, Request.request_status=="pending").all()
    print(reqs)
    for req in reqs:
        req.request_status="denied"
    db.session.commit()
    return {"request_granted":our_request.get_json()}, 200

@app.route("/backend/reject", methods=["PATCH"])
@jwt_required()
def backend_reject():
    type, logged_libr=get_info(get_jwt())
    if type!="librarian":
        return jsonify({"error":"Login as librarian to access this"}), 401
    data=request.get_json()

    user_email=data["user_email"]
    user=User.query.get(user_email)
    book_id=data["book_id"]
    our_request=Request.query.get((user_email,book_id))
    our_request.request_status="denied"
    user.user_num_requests-=1
    db.session.commit()
    return {"request_rejected":our_request.get_json()}, 200


@app.route("/backend/revoke", methods=["PATCH"])
@jwt_required()
def backend_revoke():
    type, logged_libr=get_info(get_jwt())
    if type!="librarian":
        return jsonify({"error":"Login as librarian to access this"}), 401
    data=request.get_json()

    user_email=data["user_email"]
    user=User.query.get(user_email)
    book_id=data["book_id"]
    our_request=Request.query.get((user_email,book_id))
    our_request.request_status="revoked"
    book=Book.query.get(book_id)
    book.book_issue_flag=0
    user.user_num_requests-=1
    db.session.commit()
    return {"request_revoked":our_request.get_json()}, 200





@app.route("/backend/requests", methods=["GET", "POST"])
@jwt_required()
def backend_requests():
    auto_revoke()

    type, logged_libr=get_info(get_jwt())
    if type!="librarian":
        return jsonify({"error":"Login as librarian to access this"}), 401
    requests=Request.query.all()
    books=Book.query.all()
    return {"requests":[req.get_json() for req in requests], "books":[book.get_json() for book in books], "name":logged_libr}, 200










