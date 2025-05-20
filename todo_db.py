import sqlite3
from datetime import datetime

class TodoDatabase:
    def __init__(self, db_path="todos.db"):
        """データベースの初期化"""
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """データベースとテーブルの作成"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    completed BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_todo(self, title):
        """新しいToDoを追加する"""
        if not title.strip():
            raise ValueError("タイトルは空にできません")

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO todos (title, created_at) VALUES (?, ?)",
                (title, datetime.now().isoformat())
            )
            conn.commit()
            return cursor.lastrowid  # 追加されたToDoのIDを返す

    def get_all_todos(self):
        """全てのToDoを取得する"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
            return cursor.fetchall()

    def delete_todo(self, todo_id):
        """ToDoを削除する"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
            conn.commit()
            return cursor.rowcount > 0  # 削除が成功したかどうかを返す

    def toggle_todo_status(self, todo_id):
        """ToDoの完了状態を切り替える"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 現在の状態を取得
            cursor.execute("SELECT completed FROM todos WHERE id = ?", (todo_id,))
            current_status = cursor.fetchone()
            if current_status is None:
                return False
            
            # 状態を反転
            new_status = 0 if current_status[0] else 1
            cursor.execute("UPDATE todos SET completed = ? WHERE id = ?", (new_status, todo_id))
            conn.commit()
            return True

# テスト用のコード
if __name__ == "__main__":
    # データベースのインスタンスを作成
    db = TodoDatabase()

    # テスト用のToDoを追加
    try:
        todo_id = db.add_todo("買い物に行く")
        print(f"ToDoを追加しました。ID: {todo_id}")

        # 全てのToDoを表示
        todos = db.get_all_todos()
        print("\n現在のToDo一覧:")
        for todo in todos:
            print(f"ID: {todo[0]}, タイトル: {todo[1]}, 完了: {todo[2]}, 作成日時: {todo[3]}")
    except ValueError as e:
        print(f"エラー: {e}")