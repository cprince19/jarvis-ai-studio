APP_STYLESHEET = """
QMainWindow, QWidget {
    background: #111827;
    color: #e5e7eb;
    font-family: Segoe UI;
    font-size: 14px;
}
QFrame#sidebar {
    background: #0b1220;
    border-right: 1px solid #263244;
}
QLabel#brand {
    font-size: 22px;
    font-weight: 700;
    color: #f9fafb;
}
QLabel#subtitle {
    color: #94a3b8;
}
QPushButton {
    background: #1f2937;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 9px 14px;
}
QPushButton:hover { background: #273449; }
QPushButton#primary {
    background: #2563eb;
    border: 0;
    font-weight: 700;
}
QPushButton#primary:hover { background: #1d4ed8; }
QListWidget, QLineEdit, QTextEdit {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px;
}
QStatusBar { background: #0b1220; color: #94a3b8; }
"""
