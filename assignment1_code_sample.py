import os
import pymysql
from urllib.request import urlopen

# A07:2021-Identification and Authentication Failures
# The database credentials are hardcoded in the script. This exposes sensitive credentials in the source code, making them vulnerable to leaks.
# Mitigation: Store credentials securely using environment variables or a secrets manager.
db_config = {
    'host': 'mydatabase.com',
    'user': 'admin',
    'password': 'secret123'
}

# A03:2021-Injection
# The script does not validate or sanitize user input before using it. This can lead to XSS (Cross-Site Scripting) attacks.
# Mitigation: Sanitize user input by removing dangerous characters, for example, we can put "return html.escape(user_input)".
def get_user_input():
    user_input = input('Enter your name: ')
    return user_input

def send_email(to, subject, body):
    os.system(f'echo {body} | mail -s "{subject}" {to}')

def get_data():
    url = 'http://insecure-api.com/get-data'
    data = urlopen(url).read().decode()
    return data

# A03:2021 – Injection
# The save_to_db() function directly concatenates user input into an SQL query, If data contains malicious SQL ('; DROP TABLE mytable; --), it could lead to data loss or database compromise.
# Mitigation: Use parameterized queries to prevent SQL injection.
    # query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    # connection = pymysql.connect(**db_config)
    # cursor = connection.cursor()
    # cursor.execute(query, (data, 'Another Value'))
    # connection.commit()
    # cursor.close()
    # connection.close()
def save_to_db(data):
    query = f"INSERT INTO mytable (column1, column2) VALUES ('{data}', 'Another Value')"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
