# Job Scheduler

## Overview
Job Scheduler is a Python-based project that allows users to schedule jobs to generate reports from a database. The reports are generated in Excel format and can be sent via email if specified by the user. The scheduling can be set to run daily, monthly, yearly, or at any custom interval.

## Features
- Connects to any database and executes user-defined queries.
- you can write as many queries as you want it will be generated in a single excel with mant sheets. 
- Generates reports in Excel format.
- Sends reports via email if specified.
- Allows scheduling of jobs at various intervals (daily, monthly, yearly, etc.).
- Web interface built with Flask for easy job management.

## Technologies Used
- **Python**: Core programming language.
- **Flask**: Web framework for the user interface.
- **SQLAlchemy**: For database connections and queries.
- **Pandas**: For data manipulation and Excel file generation.
- **APScheduler**: For scheduling jobs.
- **Flask-Mail**: For sending emails.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/job-scheduler.git
    cd job-scheduler
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your database and email configurations in `config.py`.

## Usage
1. Run the Flask application:
    ```bash
    flask run
    ```
     ```vscode
    pyhton app.py
    ```
    

2. Open your web browser and go to `http://127.0.0.1:5000`.

3. Use the web interface to create and manage your scheduled jobs.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.


## Contact
For any questions or suggestions, please open an issue or contact me at [adityajangitiaap@gmail.com].

