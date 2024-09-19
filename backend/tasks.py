import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from celery.schedules import crontab
import pyexcel
from libmgmt_app_backend.extensions import celery_app
from libmgmt_app_backend import create_flask_app
from celery.signals import worker_init

flask_app = None

@worker_init.connect
def initialize_flask_app(**kwargs):
    global flask_app
    flask_app = create_flask_app()

@celery_app.task
def add(x,y):
    return x+y

# @celery_app.on_after_finalize.connect
# def setup_periodic_hello_tasks(sender,**kwargs):
#     sender.add_periodic_task(crontab(minute='*/2'),daily_notification_task.s(),name="run every 2 minute")

@celery_app.on_after_finalize.connect
def setup_periodic_hello_tasks(sender,**kwargs):
    sender.add_periodic_task(crontab(minute=0, hour=17),daily_notification_task.s(),name="Runs everyday at 1700 hours")

@celery_app.on_after_finalize.connect
def setup_periodic_monthly_tasks(sender,**kwargs):
    sender.add_periodic_task(crontab(minute=0, hour=0, day_of_month=1),monthly_report_task.s(),name="Runs 1st of every month")

#Download CSV report task
@celery_app.task
def export_csv_task():
    data = retrieveDataforCSV()
    filename = "test.csv"
    output_dir = './libmgmt_app_backend/user-downloads'
    file_path = os.path.join(output_dir, filename)
    pyexcel.save_as(records=data, dest_file_name=file_path)
    return f"CSV file saved at {file_path}"

#Monthly report task
@celery_app.task
def monthly_report_task():
    data = retrieveDataforCSV()
    htmlContent = generate_html(data)
    send_mail_task(htmlContent, subject_line='Monthly Report Email', receiver_mail='admin@lms.com')
    return "Monthly report shared successfully"

#Daily notification task
@celery_app.task
def daily_notification_task():
    global flask_app
    with flask_app.app_context():
        from libmgmt_app_backend.models.user import User
        from libmgmt_app_backend.extensions import db
        users = User.query.filter_by(visitedToday=False).all()
        allUsers = User.query.filter_by(visitedToday=True).all()
        html_content = f'''
                        <h2>Dear Reader,</h2>
                        <p>I hope this email finds you well.</p>
                        <p>This is a auto-generated mail to be sent as part of a testing for automation process. 
                        This is a gentle remainder to login today and check for all the latest ebooks.<p>
                        <p>Best regards,</p>
                        <p>LMS Admin</p>
                        <p>admin123</p>
                        <p>admin@lms.com</p>
                        '''
        if not users:
            for user in allUsers:
                user.visitedToday = False
                db.session.commit()
            return "No inactive user found"
        else:
            for user in users:
                send_mail_task(html_content, subject_line='Daily Remainder Mail', receiver_mail=user.email)
            for user in allUsers:
                user.visitedToday = False
                db.session.commit()
            
    return "Email successfully sent to inactive users"

def retrieveDataforCSV():
    global flask_app
    with flask_app.app_context():
        from libmgmt_app_backend.models.issuedBook import IssuedBook
        from libmgmt_app_backend.models.book import Book 
        data = (
            IssuedBook.query
            .join(Book, IssuedBook.bookId == Book.id)
            .with_entities(
                IssuedBook.bookId,
                IssuedBook.bookName,
                Book.author,        
                Book.releaseDate,
                Book.section,
                IssuedBook.issuerName,
                IssuedBook.status,
                IssuedBook.issuedDate,
                IssuedBook.returnedDate,
                Book.rating
            )
            .all()
        )
        formatted_data = [
            {
                'Book Id': record.bookId,
                'Book Name': record.bookName,
                'Author': record.author,
                'Release Date': record.releaseDate,
                'Section': record.section,
                'Issuer Name': record.issuerName,
                'Status': record.status,
                'Issued Date': record.issuedDate,
                'Returned Date': record.returnedDate,
                'Rating': record.rating
            }
            for record in data
        ]
        
        return formatted_data

def generate_html(data):
    html = "<h2>Monthly Report - EBooks</h2><table border='1'><tr><th>Book Id</th><th>Book Name</th><th>Author</th><th>Release Date</th><th>Section</th><th>Issuer Name</th><th>Status</th><th>Issued Date</th><th>Returned Date</th><th>Rating</th></tr>"
    
    for record in data:
        html += f"<tr>"
        html += f"<td>{record.get('Book Id')}</td>"
        html += f"<td>{record.get('Book Name')}</td>"
        html += f"<td>{record.get('Author')}</td>"
        html += f"<td>{record.get('Release Date')}</td>"
        html += f"<td>{record.get('Section')}</td>"
        html += f"<td>{record.get('Issuer Name')}</td>"
        html += f"<td>{record.get('Status')}</td>"
        html += f"<td>{record.get('Issued Date')}</td>" 
        html += f"<td>{record.get('Returned Date')}</td>" 
        html += f"<td>{record.get('Rating')}</td>"
        html += "</tr>"
    html += "</table>"
    return html

def send_mail_task(content, subject_line, receiver_mail):
    # Email configuration
    sender = '23dp1000016@ds.study.iitm.ac.in'
    receiver = receiver_mail
    subject = subject_line
    body = content
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # Send the email using smtplib
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login('23dp1000016@ds.study.iitm.ac.in', '')
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Failed to send email: {e}')