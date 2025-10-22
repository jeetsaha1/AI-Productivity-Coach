from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from ai.ai_assistant import AIAssistant
from features.task_management import TaskManagement
from features.time_management import TimeManagement
import os
from datetime import datetime

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['TEMPLATES_AUTO_RELOAD'] = True
# session secret (use real secret in production)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')

ai = AIAssistant()
tasks_mgr = TaskManagement()
time_mgr = TimeManagement()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    # ensure session history exists
    session.setdefault('history', [
        {"role": "system", "content": "You are a helpful AI productivity coach. Be concise and offer actionable steps."}
    ])
    return render_template('chat.html')

@app.route('/chat/api', methods=['POST'])
def chat_api():
    data = request.json or {}
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'no message provided'}), 400

    # append user message to history
    history = session.get('history', [])
    history.append({"role": "user", "content": message, "time": datetime.utcnow().isoformat()})

    # call assistant with full history
    reply, meta = ai.chat_with_history(history)

    # allow assistant to trigger local helpers via meta (e.g., set timer, create tasks)
    if meta.get('create_task'):
        tasks_mgr.create_task({'title': meta['create_task']})
    if meta.get('start_timer'):
        time_mgr.start_timer({'duration': meta['start_timer']})

    # append assistant reply to history and persist
    history.append({"role": "assistant", "content": reply, "time": datetime.utcnow().isoformat()})
    session['history'] = history

    return jsonify({'reply': reply, 'meta': meta})

@app.route('/chat/history', methods=['GET'])
def chat_history():
    history = session.get('history', [])
    # return user+assistant messages (omit system message)
    items = [
        {'role': m.get('role'), 'content': m.get('content'), 'time': m.get('time')}
        for m in history if m.get('role') != 'system'
    ]
    return jsonify({'history': items})

@app.route('/chat/clear', methods=['POST'])
def chat_clear():
    session['history'] = [
        {"role": "system", "content": "You are a helpful AI productivity coach. Be concise and offer actionable steps."}
    ]
    return jsonify({'status': 'cleared'})

@app.route('/tasks', methods=['GET', 'POST'])
def tasks_page():
    if request.method == 'POST':
        title = request.form.get('title') or (request.json or {}).get('title')
        if title:
            tasks_mgr.create_task({'title': title})
        return redirect(url_for('tasks_page'))
    tasks = tasks_mgr.get_tasks()
    return render_template('tasks.html', tasks=tasks)

@app.route('/tasks/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    tasks_mgr.delete_task(task_id)
    return redirect(url_for('tasks_page'))

@app.route('/timer', methods=['GET', 'POST'])
def timer_page():
    started = False
    duration = None
    if request.method == 'POST':
        duration = request.form.get('duration') or (request.json or {}).get('duration')
        time_mgr.start_timer({'duration': duration})
        started = True
    return render_template('timer.html', started=started, duration=duration)

@app.route('/ai/breakdown', methods=['POST'])
def ai_breakdown():
    data = request.json or {}
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'no text provided'}), 400
    result = ai.suggest_breakdown(text)
    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    # allow other devices on your LAN (phone) to connect
    app.run(host='0.0.0.0', port=port, debug=True)

# ngrok http 3000