from flask import Flask, render_template, request
import threading
import os
import logging

app = Flask(__name__)
LOG_FILE = './logs/debug_plugin.log'

def start_debug_plugin_server():
    app.run(host='0.0.0.0', port=5000)

def configure_plugin(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Debug Plugin Configuration")
    stdscr.refresh()
    stdscr.getch()

def execute():
    threading.Thread(target=start_debug_plugin_server).start()

@app.route('/')
def home():
    return "Debug Plugin Home Page"

@app.route('/control')
def control_panel():
    try:
        with open(LOG_FILE, 'r') as f:
            log_content = f.read()
    except FileNotFoundError:
        log_content = "Log file not found."
    return render_template('control_panel.html', log_content=log_content)

@app.route('/edit', methods=['GET', 'POST'])
def edit_file():
    if request.method == 'POST':
        file_path = request.form['file_path']
        file_content = request.form['file_content']
        with open(file_path, 'w') as f:
            f.write(file_content)
        return f"File {file_path} updated successfully."
    else:
        file_path = request.args.get('file')
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                file_content = f.read()
        else:
            file_content = "File not found."
        return render_template('edit_file.html', file_path=file_path, file_content=file_content)

@app.route('/logs')
def view_logs():
    main_log = './logs/main2.log'
    debug_log = './logs/debug_plugin.log'
    with open(main_log, 'r') as f:
        main_log_content = f.read()
    with open(debug_log, 'r') as f:
        debug_log_content = f.read()
    return render_template('view_logs.html', main_log_content=main_log_content, debug_log_content=debug_log_content)

@app.route('/restart')
def restart_project():
    os.system('pkill -f main2.py')
    os.system('python3 main2.py &')
    return "Project restarted."

@app.route('/stop')
def stop_project():
    os.system('pkill -f main2.py')
    return "Project stopped."

if __name__ == "__main__":
    execute()
