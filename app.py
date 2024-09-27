# from flask import Flask, request, render_template, send_file
# import pandas as pd
# import time
# import os
# import psycopg2
# import pymysql
# import pymssql
# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import datetime

# app = Flask(__name__)

# scheduler = BackgroundScheduler()
# scheduler.start()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/execute', methods=['POST'])
# def execute():
#     job_name=request.form['job_name']
#     db_type = request.form['db_type']
#     server = request.form['server']
#     database = request.form['database']
#     username = request.form['username']
#     password = request.form['password']
#     queries = request.form['queries'].split(';')
#     output_file = request.form['output_file']
#     email_ids = request.form['email_ids']
#     frequency = int(request.form['frequency'])
#     start_date = request.form['start_date']
#     end_date = request.form['end_date']

#     # Ensure the output filename has the correct extension
#     if not output_file.endswith('.xlsx'):
#         output_file += '.xlsx'

#     # Use a relative path for the output file
#     output_path = os.path.join('output', output_file)
#     os.makedirs('output', exist_ok=True)

#     # Validate and convert date strings to datetime objects
#     try:
#         start_date = datetime.strptime(start_date, '%d-%m-%Y %H:%M:%S')
#         end_date = datetime.strptime(end_date, '%d-%m-%Y %H:%M:%S')
#     except ValueError:
#         return "Invalid date format. Please use 'DD-MM-YYYY HH:MM:SS'."

#     def run_queries():
#         start_time = time.time()

#         # Establish a connection based on the database type
#         if db_type == 'mssql':
#             conn = pymssql.connect(server=server, database=database, user=username, password=password)
#         elif db_type == 'postgres':
#             conn = psycopg2.connect(host=server, database=database, user=username, password=password)
#         elif db_type == 'mysql':
#             conn = pymysql.connect(host=server, database=database, user=username, password=password)
#         else:
#             return "Unsupported database type"

#         cursor = conn.cursor()

#         # Create a Pandas Excel writer using openpyxl as the engine
#         writer = pd.ExcelWriter(output_path, engine='openpyxl')

#         for i, query in enumerate(queries):
#             query = query.strip()
#             if query:
#                 cursor.execute(query)
#                 result = cursor.fetchall()
#                 df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
#                 sheet_name = f'Sheet{i+1}'
#                 df.to_excel(writer, sheet_name=sheet_name, index=False)

#         writer.close()

#         cursor.close()
#         conn.close()

#         end_time = time.time()
#         execution_time = end_time - start_time

#         # Here you can add code to send the output file to the email IDs
#         # For example, using smtplib to send emails

#         return f"Execution Time: {execution_time} seconds. <a href='/download/{output_file}'>Download {output_file}</a>"

#     # Schedule the job
#     scheduler.add_job(run_queries, 'interval', minutes=frequency, start_date=start_date, end_date=end_date)

#     return "Job scheduled successfully"

# @app.route('/download/<filename>')
# def download(filename):
#     file_path = os.path.join('output', filename)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)






from flask import Flask, request, render_template, send_file, redirect, url_for
import pandas as pd
import time
import os
import psycopg2
import pymysql
import pymssql
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from models import db, Job  # Import the db and Job model

app = Flask(__name__)

# Update the following line with your MySQL database credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Aug10#border@localhost/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

scheduler = BackgroundScheduler()
scheduler.start()

jobs = {}

#routes and functions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    job_name = request.form['job_name']
    db_type = request.form['db_type']
    server = request.form['server']
    database = request.form['database']
    username = request.form['username']
    password = request.form['password']
    queries = request.form['queries'].split(';')
    output_file = request.form['output_file']
    email_ids = request.form['email_ids']
    frequency = int(request.form['frequency'])
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    if not output_file.endswith('.xlsx'):
        output_file += '.xlsx'

    output_path = os.path.join('output', output_file)
    os.makedirs('output', exist_ok=True)

    try:
        start_date = datetime.strptime(start_date, '%d-%m-%Y %H:%M:%S')
        end_date = datetime.strptime(end_date, '%d-%m-%Y %H:%M:%S')
    except ValueError:
        return "Invalid date format. Please use 'DD-MM-YYYY HH:MM:SS'."

    new_job = Job(
        job_name=job_name,
        db_type=db_type,
        server=server,
        database_name=database,
        username=username,
        password=password,
        queries=request.form['queries'],
        output_file=output_file,
        email_ids=email_ids,
        frequency=frequency,
        start_date=start_date,
        end_date=end_date
    )
    db.session.add(new_job)
    db.session.commit()

    def run_queries():
        start_time = time.time()

        if db_type == 'mssql':
            conn = pymssql.connect(server=server, database=database, user=username, password=password)
        elif db_type == 'postgres':
            conn = psycopg2.connect(host=server, database=database, user=username, password=password)
        elif db_type == 'mysql':
            conn = pymysql.connect(host=server, database=database, user=username, password=password)
        else:
            return "Unsupported database type"

        cursor = conn.cursor()
        writer = pd.ExcelWriter(output_path, engine='openpyxl')

        for i, query in enumerate(queries):
            query = query.strip()
            if query:
                cursor.execute(query)
                result = cursor.fetchall()
                df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
                sheet_name = f'Sheet{i+1}'
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        writer.close()
        cursor.close()
        conn.close()

        end_time = time.time()
        execution_time = end_time - start_time

        return f"Execution Time: {execution_time} seconds. <a href='/download/{output_file}'>Download {output_file}</a>"

    job = scheduler.add_job(run_queries, 'interval', minutes=frequency, start_date=start_date, end_date=end_date)
    jobs[new_job.id] = job

    return "Job scheduled successfully"

@app.route('/jobs')
def list_jobs():
    all_jobs = Job.query.all()
    return render_template('jobs.html', jobs=all_jobs)

@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        job.job_name = request.form['job_name']
        job.db_type = request.form['db_type']
        job.server = request.form['server']
        job.database_name = request.form['database']
        job.username = request.form['username']
        job.password = request.form['password']
        job.queries = request.form['queries']
        job.output_file = request.form['output_file']
        job.email_ids = request.form['email_ids']
        job.frequency = int(request.form['frequency'])
        job.start_date = datetime.strptime(request.form['start_date'], '%d-%m-%Y %H:%M:%S')
        job.end_date = datetime.strptime(request.form['end_date'], '%d-%m-%Y %H:%M:%S')

        db.session.commit()

        job_scheduler = jobs.get(job_id)
        if job_scheduler:
            job_scheduler.reschedule(trigger='interval', minutes=job.frequency, start_date=job.start_date, end_date=job.end_date)

        if 'execute_now' in request.form:
            return redirect(url_for('execute_job', job_id=job_id))

        return redirect(url_for('list_jobs'))

    return render_template('edit_job.html', job=job)

@app.route('/execute_job/<int:job_id>', methods=['POST','GET'])
def execute_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    def run_queries():
        start_time = time.time()

        if job.db_type == 'mssql':
            conn = pymssql.connect(server=job.server, database=job.database_name, user=job.username, password=job.password)
        elif job.db_type == 'postgres':
            conn = psycopg2.connect(host=job.server, database=job.database_name, user=job.username, password=job.password)
        elif job.db_type == 'mysql':
            conn = pymysql.connect(host=job.server, database=job.database_name, user=job.username, password=job.password)
        else:
            return "Unsupported database type"

        cursor = conn.cursor()
        output_path = os.path.join('output', job.output_file)
        writer = pd.ExcelWriter(output_path, engine='openpyxl')

        queries = job.queries.split(';')
        for i, query in enumerate(queries):
            query = query.strip()
            if query:
                cursor.execute(query)
                result = cursor.fetchall()
                df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
                sheet_name = f'Sheet{i+1}'
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        writer.close()
        cursor.close()
        conn.close()

        end_time = time.time()
        execution_time = end_time - start_time

        return f"Execution Time: {execution_time} seconds. Output saved to {output_path}"
    #frequency in integer format
    job.frequency = int(job.frequency)
    
    job_scheduler = scheduler.add_job(run_queries, 'interval', minutes=job.frequency, start_date=job.start_date, end_date=job.end_date)
    jobs[job.id] = job_scheduler
    

    result = run_queries()
    return result





@app.route('/delete/<int:job_id>')
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    job_scheduler = jobs.pop(job_id, None)
    if job_scheduler:
        job_scheduler.remove()
    return redirect(url_for('list_jobs'))

@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join('output', filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

