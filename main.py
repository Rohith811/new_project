from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('production_data.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

@app.route('/data', methods=['GET'])
def get_data():
    well_number = request.args.get('well', default=None, type=str)
    if not well_number:
        return jsonify({'error': 'API well number is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT oil, gas, brine FROM production
        WHERE api_well_number = ?
        ''', (well_number,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return jsonify({
                'oil': result['oil'],
                'gas': result['gas'],
                'brine': result['brine']
            })
        else:
            return jsonify({'error': 'API well number not found'}), 404

    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=8080)

 