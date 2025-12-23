import sqlite3
from config import DEFAULT_SETTINGS

DB_NAME = "bot_users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            model TEXT,
            language TEXT,
            length TEXT,
            tone TEXT,
            creativity TEXT
        )
    ''')
    
    # Migration check
    cursor.execute("PRAGMA table_info(user_settings)")
    columns = [info[1] for info in cursor.fetchall()]
    
    if "length" not in columns: cursor.execute("ALTER TABLE user_settings ADD COLUMN length TEXT")
    if "tone" not in columns: cursor.execute("ALTER TABLE user_settings ADD COLUMN tone TEXT")
    if "creativity" not in columns: cursor.execute("ALTER TABLE user_settings ADD COLUMN creativity TEXT")

    conn.commit()
    conn.close()

def get_user_settings(user_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_settings WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    settings = DEFAULT_SETTINGS.copy()
    if result:
        for key in settings.keys():
            if result[key] is not None:
                settings[key] = result[key]
    return settings

def update_user_setting(user_id, setting_key, value):
    current = get_user_settings(user_id)
    current[setting_key] = value
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_settings (user_id, model, language, length, tone, creativity)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
        model=excluded.model,
        language=excluded.language,
        length=excluded.length,
        tone=excluded.tone,
        creativity=excluded.creativity
    ''', (user_id, current['model'], current['language'], current['length'], current['tone'], current['creativity']))
    conn.commit()
    conn.close()