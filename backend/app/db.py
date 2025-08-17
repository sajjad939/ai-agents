# ========== app/db.py ==========
class SupabaseClient:
    def __init__(self):
        self.db = {
            "users": [],
            "profiles": [],
            "lessons": [],
            "lesson_types": [],
            "transcript_steps": [],
            "progress": [],
            "achievements": []
        }
    def insert(self, table, data):
        self.db[table].append(data)
        return data
    def select(self, table, filters=None):
        if not filters:
            return self.db[table]
        return [row for row in self.db[table] if all(row.get(k) == v for k, v in filters.items())]
    def update(self, table, filters, data):
        for row in self.db[table]:
            if all(row.get(k) == v for k, v in filters.items()):
                row.update(data)
        return True

supabase = SupabaseClient()