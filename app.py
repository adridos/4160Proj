#.\env\Scripts\activate
from flask import Flask, render_template, request, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__, template_folder='/var/www/html')



app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'mc'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Pass123#'
app.config['MYSQL_DATABASE_DB'] = 'pottydb'

mysql = MySQL(app)
mysql.init_app(app)


@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM motion_detection ORDER BY timestamp')
    data = cursor.fetchall()

    return render_template('index.html', data=data)
    
@app.route('/tracker', methods=['POST'])
def handle_motion_detection():
    data = request.get_json()
    motion_detected = data.get('motion_detected')
    timestamp = data.get('timestamp')
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO motion_detection (motion_detected, timestamp) VALUES (%s, %s)', (motion_detected, timestamp))
    conn.commit()

    return jsonify({'motion_detected': motion_detected, 'timestamp': timestamp})

@app.route('/tracker', methods=['GET'])
def get_motion_detection():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM motion_detection ORDER BY timestamp')
    data = cursor.fetchall()

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
