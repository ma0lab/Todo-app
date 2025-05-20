import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QLineEdit, QPushButton, QListWidget,
                           QListWidgetItem, QMessageBox, QCheckBox)
from PyQt5.QtCore import Qt
from todo_db import TodoDatabase

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = TodoDatabase()
        self.init_ui()
        self.load_todos()

    def init_ui(self):
        """UIの初期化"""
        self.setWindowTitle('ToDoリスト')
        self.setGeometry(100, 100, 600, 400)

        # メインウィジェットとレイアウトの設定
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # 入力フォームの作成
        input_layout = QHBoxLayout()
        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText('新しいタスクを入力...')
        self.todo_input.returnPressed.connect(self.add_todo)
        
        add_button = QPushButton('追加')
        add_button.clicked.connect(self.add_todo)
        
        input_layout.addWidget(self.todo_input)
        input_layout.addWidget(add_button)
        layout.addLayout(input_layout)

        # ToDoリストの作成
        self.todo_list = QListWidget()
        layout.addWidget(self.todo_list)

    def add_todo(self):
        """新しいToDoを追加"""
        title = self.todo_input.text().strip()
        if not title:
            QMessageBox.warning(self, '警告', 'タスクを入力してください。')
            return

        try:
            self.db.add_todo(title)
            self.todo_input.clear()
            self.load_todos()
        except ValueError as e:
            QMessageBox.warning(self, 'エラー', str(e))

    def load_todos(self):
        """ToDoリストの読み込みと表示"""
        self.todo_list.clear()
        todos = self.db.get_all_todos()
        
        for todo in todos:
            item = QListWidgetItem()
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            
            # チェックボックス
            checkbox = QCheckBox()
            checkbox.setChecked(bool(todo[2]))  # completedの状態を設定
            checkbox.stateChanged.connect(lambda state, id=todo[0]: self.toggle_todo(id))
            layout.addWidget(checkbox)
            
            # タスクのタイトル
            title_label = QPushButton(todo[1])
            title_label.setStyleSheet('text-align: left; border: none;')
            if todo[2]:  # 完了済みの場合は取り消し線を表示
                title_label.setStyleSheet('text-align: left; border: none; text-decoration: line-through;')
            layout.addWidget(title_label)
            
            # 削除ボタン
            delete_button = QPushButton('削除')
            delete_button.setFixedWidth(60)
            delete_button.clicked.connect(lambda checked, id=todo[0]: self.delete_todo(id))
            layout.addWidget(delete_button)
            
            widget.setLayout(layout)
            item.setSizeHint(widget.sizeHint())
            
            self.todo_list.addItem(item)
            self.todo_list.setItemWidget(item, widget)

    def toggle_todo(self, todo_id):
        """ToDoの完了状態を切り替える"""
        if self.db.toggle_todo_status(todo_id):
            self.load_todos()
        else:
            QMessageBox.warning(self, 'エラー', 'タスクの状態更新に失敗しました。')

    def delete_todo(self, todo_id):
        """ToDoの削除"""
        reply = QMessageBox.question(
            self, '確認',
            'このタスクを削除してもよろしいですか？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.db.delete_todo(todo_id):
                self.load_todos()
            else:
                QMessageBox.warning(self, 'エラー', 'タスクの削除に失敗しました。')

def main():
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 