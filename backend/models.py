from database import db

class Librarian(db.Model):
    __tablename__="librarian"
    libr_email=db.Column(db.String,primary_key=True)
    libr_password=db.Column(db.String , nullable=False)
    libr_name=db.Column(db.String, nullable=False)

    def get_json(self):
        return {"libr_email": self.libr_email, "libr_password": self.libr_password, "libr_name": self.libr_name}

class User(db.Model):
    __tablename__="user"
    user_email=db.Column(db.String,primary_key=True)
    user_password=db.Column(db.String , nullable=False)
    user_login_date=db.Column(db.String)
    user_name=db.Column(db.String, nullable=False)
    user_num_requests=db.Column(db.Integer, db.CheckConstraint('user_num_requests >= 0 AND user_num_requests <= 5', name='check_user_num_requests'), default=0)
    user_requests=db.relationship("Request")

    def get_json(self):
        requests=[request.get_json() for request in self.user_requests]
        return {"user_email": self.user_email, "user_password": self.user_password, "user_name": self.user_name, "user_num_requests": self.user_num_requests, "user_requests":requests}

class Book(db.Model):
    __tablename__="book"
    book_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_content=db.Column(db.String , nullable=False)
    book_name=db.Column(db.String, nullable=False)
    book_issue_flag=db.Column(db.Integer, db.CheckConstraint("book_issue_flag in [0, 1]", name='check_book_issue_flag'), nullable=False, default=0)
    section_title=db.Column(db.String, db.ForeignKey("section.section_title"), nullable=False)
    book_requests=db.relationship("Request")
    book_authors=db.Column(db.String, nullable=False)

    def get_json(self):
        requests=[request.get_json() for request in self.book_requests]
        return {"book_id": self.book_id, "book_content": self.book_content, "book_name": self.book_name, "book_issue_flag": self.book_issue_flag, "section_title": self.section_title, "book_authors": self.book_authors, "book_requests":requests}

class Request(db.Model):
    __tablename__="request"
    user_email=db.Column(db.String, db.ForeignKey("user.user_email"), nullable=False, primary_key=True)
    book_id=db.Column(db.Integer, db.ForeignKey("book.book_id"), nullable=False, primary_key=True)
    request_status=db.Column(db.String ,db.CheckConstraint('request_status in ["pending","issued","returned","denied", "revoked"]', name='check_request_status'), nullable=False)
    request_issue_date=db.Column(db.String)
    request_return_date=db.Column(db.String)
    request_num_days=db.Column(db.Integer,db.CheckConstraint('request_num_days <8', name='check_request_num_days'))
    request_feedback=db.Column(db.String)

    def get_json(self):
        return {"user_email": self.user_email, "book_id": self.book_id, "request_status": self.request_status, "request_issue_date": self.request_issue_date, "request_return_date": self.request_return_date, "request_num_days": self.request_num_days, "request_feedback": self.request_feedback}

class Section(db.Model):
    __tablename__="section"
    section_title=db.Column(db.String,primary_key=True)
    section_description=db.Column(db.String, nullable=False)
    section_books=db.relationship("Book", backref="book_section")

    def get_json(self):
        books=[book.get_json() for book in self.section_books]
        return {"section_title": self.section_title, "section_description": self.section_description, "section_books":books}
