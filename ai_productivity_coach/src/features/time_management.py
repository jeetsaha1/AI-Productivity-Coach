import json
import uuid
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).parent / 'tasks.json'

class TaskManagement:
    def __init__(self):
        if not DATA_FILE.exists():
            DATA_FILE.write_text('[]')

    def _read(self):
        return json.loads(DATA_FILE.read_text())

    def _write(self, data):
        DATA_FILE.write_text(json.dumps(data, indent=2))

    def get_tasks(self):
        return self._read()

    def create_task(self, data):
        tasks = self._read()
        task = {
            'id': str(uuid.uuid4()),
            'title': data.get('title'),
            'created_at': datetime.utcnow().isoformat()
        }
        tasks.insert(0, task)
        self._write(tasks)
        return task

    def delete_task(self, task_id):
        tasks = self._read()
        tasks = [t for t in tasks if t['id'] != task_id]
        self._write(tasks)

from datetime import datetime
from pathlib import Path
import json

LOG_FILE = Path(__file__).parent / 'timers.json'

class TimeManagement:
    def __init__(self):
        if not LOG_FILE.exists():
            LOG_FILE.write_text('[]')

    def start_timer(self, data):
        duration = data.get('duration')
        entry = {
            'started_at': datetime.utcnow().isoformat(),
            'duration': duration
        }
        logs = json.loads(LOG_FILE.read_text())
        logs.insert(0, entry)
        LOG_FILE.write_text(json.dumps(logs, indent=2))
        print("Timer started:", entry)