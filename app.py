import os
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from utils import process_and_insert_data, create_tables, test_db_connection, get_data_for_visualization
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    db_connected = test_db_connection()
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part in the request', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading', 'warning')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            try:
                process_and_insert_data(file_path)
                flash('File successfully uploaded and processed', 'success')
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'danger')
            
            return redirect(url_for('upload_file'))
        else:
            flash('Allowed file types are csv, xlsx, xls', 'warning')
            return redirect(request.url)
    return render_template('upload.html', db_connected=db_connected)

@app.route('/visualize')
def visualize():
    return render_template('visualize.html')

@app.route('/api/data/<category>')
def get_data(category):
    try:
        date_range = request.args.get('date_range', 'all')
        search = request.args.get('search', '')

        # Calculate the start date based on the selected date range
        if date_range == 'last7':
            start_date = datetime.now() - timedelta(days=7)
        elif date_range == 'last30':
            start_date = datetime.now() - timedelta(days=30)
        elif date_range == 'last90':
            start_date = datetime.now() - timedelta(days=90)
        else:
            start_date = None

        data = get_data_for_visualization(category, start_date, search)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    create_tables()
    connection_status = test_db_connection()
    print(f"Database connection status: {connection_status}")
    app.run(host='0.0.0.0', port=5000, debug=True)
