from flask import Flask, request, send_file, make_response
import cx_Oracle
import pandas as pd
import json

app = Flask(__name__)
@app.route('/api/download_excel', methods=['POST'])
def download_excel():
    data = request.get_json()
    sql_query = data.get('sql_query')
    excel_filename = data.get('excel_filename')

    excel_file = fetch_from_oracle(sql_query, excel_filename)

    
    message = f"File '{excel_filename}' has been initiated for download."

    
    response_data = {
        "message": message,
        "file_url": f"/downloads/{excel_filename}"  
    }

    
    response = make_response(json.dumps(response_data))

    
    response.headers['Content-Type'] = 'application/json'

    return response

def fetch_from_oracle(sql_query, excel_filename):
    
    with open('db_creds.json') as f:
        db_creds = json.load(f)

    oracle_username = db_creds["oracle_username"]
    oracle_password = db_creds["oracle_password"]
    oracle_host = db_creds["oracle_host"]
    oracle_port = db_creds["oracle_port"]
    oracle_service_name = db_creds["oracle_service_name"]

    connection = cx_Oracle.connect(
        user=oracle_username,
        password=oracle_password,
        dsn=f"{oracle_host}:{oracle_port}/{oracle_service_name}"
    )

    cursor = connection.cursor()
    cursor.execute(sql_query)
    columns = [col[0] for col in cursor.description]
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=columns)

    cursor.close()
    connection.close()

    df.to_excel(excel_filename, index=False)
    return excel_filename

if __name__ == '__main__':
    app.run(debug=True, port = 8080)
