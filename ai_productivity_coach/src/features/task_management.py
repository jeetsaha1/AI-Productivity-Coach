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
        try:
            return json.loads(DATA_FILE.read_text())
        except Exception:
            return []

    def _write(self, data):
        DATA_FILE.write_text(json.dumps(data, indent=2))

    def get_tasks(self):
        tasks = self._read()
        # Format created_at for template and ensure key exists
        for t in tasks:
            created = t.get('created_at')
            if created:
                try:
                    dt = datetime.fromisoformat(created)
                    t['created_at'] = dt.strftime('%Y-%m-%d %H:%M')
                except Exception:
                    t['created_at'] = str(created)
            else:
                t['created_at'] = '—'
        return tasks

    def create_task(self, data):
        tasks = self._read()
        task = {
            'id': str(uuid.uuid4()),
            'title': (data.get('title') or '').strip(),
            'created_at': datetime.utcnow().isoformat()
        }
        tasks.insert(0, task)
        self._write(tasks)
        return task

    def delete_task(self, task_id):
        tasks = self._read()
        tasks = [t for t in tasks if t.get('id') != task_id]
        self._write(tasks)