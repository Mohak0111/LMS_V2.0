from workers import celery
from datetime import datetime
from celery.schedules import crontab
from models import User, Request, db, Book
from flask import render_template
import LMS_email_config
# from weasyprint import HTML
# https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#crontab-schedules



@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=16),
        # crontab(),        
        daily_reminder.s(),
        name='daily reminder'
    )

    sender.add_periodic_task(
        crontab(0, 0, day_of_month='1'),
        # crontab(),
        monthly_report.s(),
        name='monthly report'
    )

    sender.add_periodic_task(
        crontab(minute=0, hour=0),
        # crontab(),
        auto_revoke.s(),
        name='auto revoke'
    )


@celery.task()
def daily_reminder():
    users=User.query.filter(User.user_login_date != str(datetime.today().date())).all()
    for user in users:
        message=render_template("daily_reminder.html", user=user)
        LMS_email_config.send_email(user.user_email, "We Miss You!", message)
        print("DAILY_REMINDER")
    return "DAILY_REMINDER"
            



@celery.task()
def monthly_report():
    users=User.query.filter().all()
    for user in users:
        message=render_template("monthly_report.html", user=User.query.get("mohakk.mk@gmail.com"), books=Book.query.all())
        LMS_email_config.send_email(user.user_email, "Your monthly report is here!", message)
        print("MONTHLY_REPORT")
    return ("MONTHLY_REPORT")





@celery.task()
def auto_revoke():
    reqs=Request.query.filter(Request.request_status=="issued")
    for req in reqs:
        datetime_obj = datetime.strptime(req.request_issue_date, "%Y-%m-%d %H:%M:%S.%f")
        if (datetime.now()-datetime_obj).days>7:
            req.request_status="returned"
            User.query.get(req.user_email).user_num_requests-=1
            db.session.commit()
            print("AUTO_REVOKE")
    return("AUTO_REVOKE")
