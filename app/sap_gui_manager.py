"""
SAP Script Manager GUI Application

This application provides a comprehensive interface for managing SAP automation scripts.
It includes session management, script editing, transaction recording, and script execution.

Module: sap_gui_manager
Version: 1.0
Author: SAP Automation Team

Main Components:
    - SessionManager: Handles SAP GUI connections and session lifecycle
    - ScriptEditor: Provides editing interface for Python scripts
    - TransactionRecorder: Records user interactions with SAP
    - ScriptExecutor: Runs scripts and captures output
    - SAPScriptManagerApp: Main application window

Requirements:
    - PyQt5 >= 5.15.0
    - pywin32
    - SAP GUI 6.40+
"""

import sys
import os
import json
import threading
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTabWidget, QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit,
        QListWidget, QListWidgetItem, QMessageBox, QFileDialog, QDialog,
        QFormLayout, QSpinBox, QCheckBox, QGroupBox, QSplitter, QStatusBar,
        QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem,
        QProgressBar, QInputDialog
    )
    from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer, QRect
    from PyQt5.QtGui import QFont, QIcon, QColor, QTextCursor, QSyntaxHighlighter
    from PyQt5 import QtCore
except ImportError:
    print("Error: PyQt5 is required. Install with: pip install PyQt5")
    sys.exit(1)

try:
    import win32com.client as win32com
except ImportError:
    print("Error: pywin32 is required. Install with: pip install pywin32")
    sys.exit(1)

from SAP import (
    sap_sess_attach, sap_sess_create, sap_win_exists, sap_win_close,
    sap_obj_select, sap_obj_value_set, sap_obj_value_get, SAPException
)


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """Provides syntax highlighting for Python code in the script editor.
    
    Highlights keywords, strings, comments, and numbers using PyQt5's
    syntax highlighting framework.
    """
    
    def __init__(self, document):
        """Initialize the syntax highlighter.
        
        Args:
            document: The QTextDocument to apply highlighting to.
        """
        super().__init__(document)
        
        self.highlighting_rules = []
        
        keyword_format = self._create_format(color="blue", bold=True)
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def",
            "del", "elif", "else", "except", "False", "finally", "for",
            "from", "global", "if", "import", "in", "is", "lambda", "None",
            "nonlocal", "not", "or", "pass", "raise", "return", "True",
            "try", "while", "with", "yield"
        ]
        
        for keyword in keywords:
            pattern = f"\\b{keyword}\\b"
            self.highlighting_rules.append((pattern, keyword_format))
        
        string_format = self._create_format(color="green")
        self.highlighting_rules.append((r'"[^"]*"', string_format))
        self.highlighting_rules.append((r"'[^']*'", string_format))
        
        comment_format = self._create_format(color="gray", italic=True)
        self.highlighting_rules.append((r"#[^\n]*", comment_format))
        
        number_format = self._create_format(color="purple")
        self.highlighting_rules.append((r"\b\d+\b", number_format))
    
    def _create_format(self, color: str = "black", bold: bool = False, italic: bool = False):
        """Create a QTextCharFormat with specified styling.
        
        Args:
            color: Color name for the text.
            bold: Whether text should be bold.
            italic: Whether text should be italic.
            
        Returns:
            Configured QTextCharFormat object.
        """
        fmt = QtCore.QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(QtCore.QFont.Bold)
        if italic:
            fmt.setFontItalic(True)
        return fmt
    
    def highlightBlock(self, text: str):
        """Apply syntax highlighting to a code block.
        
        Args:
            text: The code block text to highlight.
        """
        for pattern, fmt in self.highlighting_rules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)


class SessionManager:
    """Manages SAP GUI sessions and connections.
    
    This class handles all interactions with the SAP GUI scripting interface,
    including connecting to sessions, creating new sessions, and maintaining
    session state information.
    
    Attributes:
        sessions (List[Dict]): List of active SAP sessions with metadata.
        current_session_id (Optional[str]): ID of currently active session.
    """
    
    def __init__(self):
        """Initialize the SessionManager."""
        self.sessions: List[Dict[str, Any]] = []
        self.current_session_id: Optional[str] = None
        self.session_counter = 0
    
    def get_available_sessions(self) -> List[str]:
        """Retrieve list of available SAP GUI sessions.
        
        Queries the SAP GUI scripting interface to find running sessions.
        Updates the internal sessions list.
        
        Returns:
            List of session titles or empty list if no sessions found.
        """
        try:
            sapgui = win32com.GetObject("SAPGUI")
            sapapp = sapgui.GetScriptingEngine
            
            sessions = []
            if sapapp.Children.Count > 0:
                connection = sapapp.Children(0)
                for i in range(connection.Sessions.Count):
                    session_title = f"Session {i+1}"
                    sessions.append(session_title)
                    
                    self.sessions.append({
                        "id": f"session_{self.session_counter}",
                        "index": i,
                        "title": session_title,
                        "created": datetime.now().isoformat(),
                        "status": "connected"
                    })
                    self.session_counter += 1
            
            return sessions
        except Exception as e:
            raise SAPException(1, f"Failed to get available sessions: {str(e)}")
    
    def connect_to_session(self, window_title: str = "SAP Easy Access") -> bool:
        """Connect to a specific SAP session.
        
        Args:
            window_title: Title of the SAP window to connect to.
            
        Returns:
            True if connection successful, False otherwise.
            
        Raises:
            SAPException: If connection fails.
        """
        try:
            result = sap_sess_attach(window_title)
            self.current_session_id = f"session_{self.session_counter}"
            return result
        except SAPException as e:
            raise SAPException(e.error_code, f"Connection failed: {e.message}")
    
    def create_new_session(self, transaction: Optional[str] = None) -> bool:
        """Create a new SAP session.
        
        Args:
            transaction: Optional transaction code to execute in new session.
            
        Returns:
            True if session created successfully, False otherwise.
        """
        try:
            result = sap_sess_create(transaction)
            self.current_session_id = f"session_{self.session_counter}"
            self.session_counter += 1
            return result
        except SAPException as e:
            raise SAPException(e.error_code, f"Session creation failed: {e.message}")
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve information about a specific session.
        
        Args:
            session_id: The ID of the session to query.
            
        Returns:
            Dictionary with session information or None if not found.
        """
        for session in self.sessions:
            if session["id"] == session_id:
                return session
        return None
    
    def close_session(self, window_title: str) -> bool:
        """Close a SAP window/session.
        
        Args:
            window_title: Title of the window to close.
            
        Returns:
            True if window closed successfully, False otherwise.
        """
        try:
            return sap_win_close(window_title)
        except Exception as e:
            raise SAPException(1, f"Failed to close session: {str(e)}")


class ScriptEditor:
    """Manages script file operations and editing state.
    
    This class handles creating, opening, saving, and tracking modifications
    to Python scripts intended for SAP automation.
    
    Attributes:
        current_file (Optional[Path]): Path to currently open script file.
        is_modified (bool): Whether current script has unsaved changes.
        scripts_directory (Path): Directory where scripts are stored.
    """
    
    def __init__(self, scripts_dir: str = "sap_scripts"):
        """Initialize the ScriptEditor.
        
        Args:
            scripts_dir: Directory path for storing script files.
        """
        self.current_file: Optional[Path] = None
        self.is_modified = False
        self.scripts_directory = Path(scripts_dir)
        self.scripts_directory.mkdir(exist_ok=True)
    
    def create_new_script(self, name: str, template: str = "") -> str:
        """Create a new script with optional template content.
        
        Args:
            name: Name for the new script (without .py extension).
            template: Initial content for the script.
            
        Returns:
            The template content or default Python script template.
        """
        if not template:
            template = '''"""
SAP Script: {name}
Created: {timestamp}

This script automates SAP transactions using the SAP Python automation library.
"""

import SAP

def main():
    """Main execution function for SAP automation."""
    try:
        SAP.sap_sess_attach("SAP Easy Access")
        
        # Add your automation code here
        
    except SAP.SAPException as e:
        print(f"Error: {{e.message}} (Code: {{e.error_code}})")
    except Exception as e:
        print(f"Unexpected error: {{str(e)}}")

if __name__ == "__main__":
    main()
'''.format(name=name, timestamp=datetime.now().isoformat())
        
        return template
    
    def open_script(self, file_path: str) -> Tuple[bool, str]:
        """Open an existing script file for editing.
        
        Args:
            file_path: Path to the script file to open.
            
        Returns:
            Tuple of (success: bool, content: str).
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return False, f"File not found: {file_path}"
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.current_file = path
            self.is_modified = False
            return True, content
        except Exception as e:
            return False, f"Error reading file: {str(e)}"
    
    def save_script(self, file_path: str, content: str) -> Tuple[bool, str]:
        """Save script content to file.
        
        Args:
            file_path: Path where script should be saved.
            content: The script content to save.
            
        Returns:
            Tuple of (success: bool, message: str).
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.current_file = path
            self.is_modified = False
            return True, f"Script saved: {file_path}"
        except Exception as e:
            return False, f"Error saving file: {str(e)}"
    
    def list_scripts(self) -> List[str]:
        """List all available scripts in the scripts directory.
        
        Returns:
            List of script file names.
        """
        try:
            scripts = [f.name for f in self.scripts_directory.glob("*.py")]
            return sorted(scripts)
        except Exception:
            return []


class TransactionRecorder:
    """Records user interactions with SAP for playback and analysis.
    
    This class captures SAP transactions, window changes, object interactions,
    and values entered, generating executable Python code that reproduces
    the recorded actions.
    
    Attributes:
        recording (bool): Whether recording is currently active.
        recorded_actions (List[Dict]): List of recorded user actions.
    """
    
    def __init__(self):
        """Initialize the TransactionRecorder."""
        self.recording = False
        self.recorded_actions: List[Dict[str, Any]] = []
        self.start_time: Optional[datetime] = None
    
    def start_recording(self) -> None:
        """Begin recording user interactions."""
        self.recording = True
        self.recorded_actions = []
        self.start_time = datetime.now()
    
    def stop_recording(self) -> List[Dict[str, Any]]:
        """Stop recording and return recorded actions.
        
        Returns:
            List of recorded actions with timestamps and details.
        """
        self.recording = False
        return self.recorded_actions
    
    def add_action(self, action_type: str, details: Dict[str, Any]) -> None:
        """Record a single user action.
        
        Args:
            action_type: Type of action (e.g., "object_set", "key_send", "window_wait").
            details: Dictionary containing action-specific details.
        """
        if not self.recording:
            return
        
        action = {
            "timestamp": datetime.now().isoformat(),
            "type": action_type,
            "details": details
        }
        self.recorded_actions.append(action)
    
    def generate_script_from_recording(self, script_name: str = "recorded_script") -> str:
        """Generate Python script code from recorded actions.
        
        Converts a series of recorded transactions into executable Python
        code that can be run independently.
        
        Args:
            script_name: Name for the generated script.
            
        Returns:
            Python script content as string.
        """
        script_lines = [
            '"""',
            f'SAP Script: {script_name}',
            f'Generated from recording: {datetime.now().isoformat()}',
            '"""',
            '',
            'import SAP',
            'import time',
            '',
            'def main():',
            '    """Playback of recorded SAP transactions."""',
            '    try:',
            '        SAP.sap_sess_attach("SAP Easy Access")',
            ''
        ]
        
        for action in self.recorded_actions:
            action_type = action.get("type")
            details = action.get("details", {})
            
            if action_type == "object_set":
                obj_id = details.get("object_id", "")
                value = details.get("value", "")
                script_lines.append(f'        SAP.sap_obj_value_set("{obj_id}", "{value}")')
            
            elif action_type == "object_select":
                obj_id = details.get("object_id", "")
                script_lines.append(f'        SAP.sap_obj_select("{obj_id}")')
            
            elif action_type == "key_send":
                keys = details.get("keys", "")
                script_lines.append(f'        SAP.sap_vkeys_send("{keys}")')
            
            elif action_type == "window_wait":
                window_title = details.get("window_title", "")
                script_lines.append(f'        SAP.sap_vkeys_send_until_win_exists("Enter", "{window_title}")')
            
            elif action_type == "pause":
                seconds = details.get("seconds", 1)
                script_lines.append(f'        time.sleep({seconds})')
        
        script_lines.extend([
            '',
            '    except SAP.SAPException as e:',
            '        print(f"SAP Error: {e.message} (Code: {e.error_code})")',
            '    except Exception as e:',
            '        print(f"Unexpected error: {str(e)}")',
            '',
            'if __name__ == "__main__":',
            '    main()',
        ])
        
        return '\n'.join(script_lines)


class ScriptExecutor(QThread):
    """Executes scripts in a separate thread to prevent GUI freezing.
    
    This class runs Python scripts in an isolated thread, capturing output,
    errors, and execution progress. Signals are emitted to update the GUI
    with execution status and results.
    
    Signals:
        output_signal: Emitted with execution output.
        error_signal: Emitted with execution errors.
        finished_signal: Emitted when execution completes.
    """
    
    output_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, script_path: str):
        """Initialize the ScriptExecutor.
        
        Args:
            script_path: Path to the Python script to execute.
        """
        super().__init__()
        self.script_path = script_path
    
    def run(self):
        """Execute the script and emit signals with results.
        
        This method runs the script in isolation, capturing stdout and stderr.
        All output is emitted via signals for GUI updates.
        """
        import io
        import contextlib
        
        try:
            self.output_signal.emit(f"Starting script execution: {self.script_path}\n")
            
            with open(self.script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
            
            output_buffer = io.StringIO()
            
            with contextlib.redirect_stdout(output_buffer):
                exec(script_content, {})
            
            output = output_buffer.getvalue()
            if output:
                self.output_signal.emit(output)
            
            self.output_signal.emit("\nScript execution completed successfully.")
            
        except Exception as e:
            error_message = f"Execution error: {str(e)}\n{traceback.format_exc()}"
            self.error_signal.emit(error_message)
        
        finally:
            self.finished_signal.emit()


class SAPScriptManagerApp(QMainWindow):
    """Main application window for SAP Script Manager.
    
    This class creates and manages the user interface for the entire SAP
    automation application, including tabs for session management, script
    editing, transaction recording, and script execution.
    
    Components:
        - Session Manager Tab: Connect/create/manage SAP sessions
        - Script Editor Tab: Create and edit Python scripts
        - Transaction Recorder Tab: Record SAP user actions
        - Script Executor Tab: Run scripts and view output
        - Settings Tab: Configure application preferences
    """
    
    def __init__(self):
        """Initialize the main application window."""
        super().__init__()
        
        self.session_manager = SessionManager()
        self.script_editor = ScriptEditor()
        self.transaction_recorder = TransactionRecorder()
        self.script_executor = None
        
        self.current_script_content = ""
        
        self.init_ui()
        self.show_status_message("Application started successfully")
    
    def init_ui(self):
        """Initialize the user interface components.
        
        Sets up the main window, tab widget, and all application tabs.
        """
        self.setWindowTitle("SAP Script Manager")
        self.setGeometry(100, 100, 1400, 800)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        self.tab_widget.addTab(self.create_session_tab(), "Session Manager")
        self.tab_widget.addTab(self.create_script_editor_tab(), "Script Editor")
        self.tab_widget.addTab(self.create_recorder_tab(), "Transaction Recorder")
        self.tab_widget.addTab(self.create_executor_tab(), "Script Executor")
        self.tab_widget.addTab(self.create_settings_tab(), "Settings")
        
        main_widget.setLayout(main_layout)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
    
    def create_session_tab(self) -> QWidget:
        """Create the Session Manager tab.
        
        This tab allows users to list available SAP sessions, connect to
        specific sessions, create new sessions, and manage existing ones.
        
        Returns:
            QWidget containing the session manager interface.
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        info_label = QLabel("SAP Session Manager")
        font = info_label.font()
        font.setPointSize(12)
        font.setBold(True)
        info_label.setFont(font)
        layout.addWidget(info_label)
        
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh Sessions")
        refresh_btn.clicked.connect(self.refresh_sessions)
        button_layout.addWidget(refresh_btn)
        
        connect_btn = QPushButton("Connect to Session")
        connect_btn.clicked.connect(self.connect_to_session)
        button_layout.addWidget(connect_btn)
        
        new_session_btn = QPushButton("Create New Session")
        new_session_btn.clicked.connect(self.create_new_session)
        button_layout.addWidget(new_session_btn)
        
        layout.addLayout(button_layout)
        
        self.session_list = QListWidget()
        layout.addWidget(QLabel("Available Sessions:"))
        layout.addWidget(self.session_list)
        
        session_info_label = QLabel("Session Details:")
        layout.addWidget(session_info_label)
        
        self.session_info_text = QTextEdit()
        self.session_info_text.setReadOnly(True)
        self.session_info_text.setMaximumHeight(200)
        layout.addWidget(self.session_info_text)
        
        tab.setLayout(layout)
        return tab
    
    def create_script_editor_tab(self) -> QWidget:
        """Create the Script Editor tab.
        
        Provides a Python script editor with syntax highlighting, allowing
        users to create, open, modify, and save SAP automation scripts.
        
        Returns:
            QWidget containing the script editor interface.
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        info_label = QLabel("Python Script Editor")
        font = info_label.font()
        font.setPointSize(12)
        font.setBold(True)
        info_label.setFont(font)
        layout.addWidget(info_label)
        
        button_layout = QHBoxLayout()
        
        new_btn = QPushButton("New Script")
        new_btn.clicked.connect(self.new_script)
        button_layout.addWidget(new_btn)
        
        open_btn = QPushButton("Open Script")
        open_btn.clicked.connect(self.open_script)
        button_layout.addWidget(open_btn)
        
        save_btn = QPushButton("Save Script")
        save_btn.clicked.connect(self.save_script)
        button_layout.addWidget(save_btn)
        
        run_btn = QPushButton("Run Script")
        run_btn.clicked.connect(self.run_script)
        button_layout.addWidget(run_btn)
        
        layout.addLayout(button_layout)
        
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Current File:"))
        self.file_path_label = QLineEdit()
        self.file_path_label.setReadOnly(True)
        file_layout.addWidget(self.file_path_label)
        layout.addLayout(file_layout)
        
        self.script_text_edit = QTextEdit()
        self.script_text_edit.setFont(QFont("Courier", 10))
        self.script_text_edit.textChanged.connect(self.on_script_modified)
        PythonSyntaxHighlighter(self.script_text_edit.document())
        layout.addWidget(self.script_text_edit)
        
        tab.setLayout(layout)
        return tab
    
    def create_recorder_tab(self) -> QWidget:
        """Create the Transaction Recorder tab.
        
        This tab allows users to record SAP transactions and automatically
        generate Python scripts from the recorded interactions.
        
        Returns:
            QWidget containing the transaction recorder interface.
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        info_label = QLabel("SAP Transaction Recorder")
        font = info_label.font()
        font.setPointSize(12)
        font.setBold(True)
        info_label.setFont(font)
        layout.addWidget(info_label)
        
        button_layout = QHBoxLayout()
        
        self.record_start_btn = QPushButton("Start Recording")
        self.record_start_btn.clicked.connect(self.start_recording)
        button_layout.addWidget(self.record_start_btn)
        
        self.record_stop_btn = QPushButton("Stop Recording")
        self.record_stop_btn.clicked.connect(self.stop_recording)
        self.record_stop_btn.setEnabled(False)
        button_layout.addWidget(self.record_stop_btn)
        
        layout.addLayout(button_layout)
        
        manual_layout = QHBoxLayout()
        manual_layout.addWidget(QLabel("Add Manual Action:"))
        
        self.action_type_combo = QComboBox()
        self.action_type_combo.addItems([
            "object_set", "object_select", "key_send", "window_wait", "pause"
        ])
        manual_layout.addWidget(self.action_type_combo)
        
        self.action_details_input = QLineEdit()
        self.action_details_input.setPlaceholderText("Enter action details")
        manual_layout.addWidget(self.action_details_input)
        
        add_action_btn = QPushButton("Add Action")
        add_action_btn.clicked.connect(self.add_manual_action)
        manual_layout.addWidget(add_action_btn)
        
        layout.addLayout(manual_layout)
        
        layout.addWidget(QLabel("Recorded Actions:"))
        self.recorded_actions_list = QListWidget()
        layout.addWidget(self.recorded_actions_list)
        
        generate_layout = QHBoxLayout()
        
        self.record_name_input = QLineEdit()
        self.record_name_input.setPlaceholderText("Enter script name")
        generate_layout.addWidget(self.record_name_input)
        
        generate_btn = QPushButton("Generate Script")
        generate_btn.clicked.connect(self.generate_script_from_recording)
        generate_layout.addWidget(generate_btn)
        
        layout.addLayout(generate_layout)
        
        tab.setLayout(layout)
        return tab
    
    def create_executor_tab(self) -> QWidget:
        """Create the Script Executor tab.
        
        Allows users to execute Python scripts and view real-time output,
        error messages, and execution status.
        
        Returns:
            QWidget containing the script executor interface.
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        info_label = QLabel("Script Executor")
        font = info_label.font()
        font.setPointSize(12)
        font.setBold(True)
        info_label.setFont(font)
        layout.addWidget(info_label)
        
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Script to Execute:"))
        
        self.executor_file_input = QLineEdit()
        self.executor_file_input.setPlaceholderText("Path to script file")
        file_layout.addWidget(self.executor_file_input)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_script_file)
        file_layout.addWidget(browse_btn)
        
        layout.addLayout(file_layout)
        
        button_layout = QHBoxLayout()
        
        self.execute_btn = QPushButton("Execute Script")
        self.execute_btn.clicked.connect(self.execute_script)
        button_layout.addWidget(self.execute_btn)
        
        clear_output_btn = QPushButton("Clear Output")
        clear_output_btn.clicked.connect(self.clear_output)
        button_layout.addWidget(clear_output_btn)
        
        layout.addLayout(button_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        output_label = QLabel("Execution Output:")
        layout.addWidget(output_label)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Courier", 10))
        layout.addWidget(self.output_text)
        
        tab.setLayout(layout)
        return tab
    
    def create_settings_tab(self) -> QWidget:
        """Create the Settings tab.
        
        Provides configuration options for the application including
        script directory, SAP connection timeout, and UI preferences.
        
        Returns:
            QWidget containing the settings interface.
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        info_label = QLabel("Application Settings")
        font = info_label.font()
        font.setPointSize(12)
        font.setBold(True)
        info_label.setFont(font)
        layout.addWidget(info_label)
        
        form_layout = QFormLayout()
        
        scripts_dir_layout = QHBoxLayout()
        self.scripts_dir_input = QLineEdit("sap_scripts")
        scripts_dir_layout.addWidget(self.scripts_dir_input)
        browse_dir_btn = QPushButton("Browse")
        browse_dir_btn.clicked.connect(self.browse_scripts_directory)
        scripts_dir_layout.addWidget(browse_dir_btn)
        form_layout.addRow("Scripts Directory:", scripts_dir_layout)
        
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setValue(30)
        self.timeout_spinbox.setMinimum(5)
        self.timeout_spinbox.setMaximum(300)
        form_layout.addRow("SAP Connection Timeout (seconds):", self.timeout_spinbox)
        
        self.auto_save_checkbox = QCheckBox("Auto-save scripts")
        self.auto_save_checkbox.setChecked(True)
        form_layout.addRow("Auto-save:", self.auto_save_checkbox)
        
        layout.addLayout(form_layout)
        
        save_settings_btn = QPushButton("Save Settings")
        save_settings_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_settings_btn)
        
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab
    
    def refresh_sessions(self):
        """Refresh the list of available SAP sessions.
        
        Queries SAP GUI and updates the session list widget with
        currently available sessions.
        """
        try:
            self.session_list.clear()
            sessions = self.session_manager.get_available_sessions()
            
            if sessions:
                for session in sessions:
                    self.session_list.addItem(session)
                self.show_status_message(f"Found {len(sessions)} SAP session(s)")
            else:
                self.show_status_message("No SAP sessions found")
        except SAPException as e:
            self.show_status_message(f"Error: {e.message}")
    
    def connect_to_session(self):
        """Connect to the selected SAP session.
        
        Retrieves the selected session from the list and attempts connection.
        """
        try:
            if not self.session_list.selectedItems():
                QMessageBox.warning(self, "Selection Required", "Please select a session first")
                return
            
            selected_item = self.session_list.selectedItems()[0]
            window_title = selected_item.text()
            
            self.session_manager.connect_to_session(window_title)
            self.show_session_info()
            self.show_status_message(f"Connected to session: {window_title}")
        except SAPException as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect: {e.message}")
            self.show_status_message("Connection failed")
    
    def create_new_session(self):
        """Create a new SAP session.
        
        Prompts user for optional transaction code and creates new session.
        """
        try:
            transaction, ok = QInputDialog.getText(
                self, "New Session",
                "Enter transaction code (leave blank for default):"
            )
            
            if not ok:
                return
            
            transaction = transaction if transaction else None
            self.session_manager.create_new_session(transaction)
            self.refresh_sessions()
            self.show_status_message("New session created successfully")
        except SAPException as e:
            QMessageBox.critical(self, "Session Creation Error", f"Failed to create session: {e.message}")
    
    def show_session_info(self):
        """Display detailed information about current session.
        
        Updates the session information text area with metadata about
        the currently active session.
        """
        if self.session_manager.current_session_id:
            session_info = self.session_manager.get_session_info(
                self.session_manager.current_session_id
            )
            
            if session_info:
                info_text = f"""
Session ID: {session_info['id']}
Title: {session_info['title']}
Created: {session_info['created']}
Status: {session_info['status']}
                """
                self.session_info_text.setText(info_text)
    
    def new_script(self):
        """Create a new Python script.
        
        Prompts user for script name and initializes editor with template.
        """
        name, ok = QInputDialog.getText(self, "New Script", "Enter script name:")
        
        if not ok or not name:
            return
        
        template = self.script_editor.create_new_script(name)
        self.script_text_edit.setText(template)
        self.file_path_label.setText(f"[New] {name}.py")
        self.current_script_content = template
        self.show_status_message(f"New script created: {name}")
    
    def open_script(self):
        """Open an existing Python script for editing.
        
        Shows file dialog and loads selected script into the editor.
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open Script", str(self.script_editor.scripts_directory),
            "Python Files (*.py);;All Files (*)"
        )
        
        if file_path:
            success, content = self.script_editor.open_script(file_path)
            
            if success:
                self.script_text_edit.setText(content)
                self.file_path_label.setText(file_path)
                self.current_script_content = content
                self.show_status_message(f"Opened: {file_path}")
            else:
                QMessageBox.critical(self, "Error", content)
    
    def save_script(self):
        """Save the current script to a file.
        
        If script hasn't been saved before, prompts for file location.
        """
        content = self.script_text_edit.toPlainText()
        
        if not self.script_editor.current_file:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(
                self, "Save Script", str(self.script_editor.scripts_directory),
                "Python Files (*.py);;All Files (*)"
            )
            
            if not file_path:
                return
        else:
            file_path = str(self.script_editor.current_file)
        
        success, message = self.script_editor.save_script(file_path, content)
        
        if success:
            self.file_path_label.setText(file_path)
            self.current_script_content = content
            self.show_status_message(message)
        else:
            QMessageBox.critical(self, "Save Error", message)
    
    def run_script(self):
        """Execute the current script in the editor.
        
        Saves the script and executes it using the ScriptExecutor.
        """
        if not self.script_text_edit.toPlainText():
            QMessageBox.warning(self, "Empty Script", "Please write some code first")
            return
        
        self.save_script()
        
        if self.script_editor.current_file:
            self.tab_widget.setCurrentIndex(3)
            self.executor_file_input.setText(str(self.script_editor.current_file))
            self.execute_script()
    
    def on_script_modified(self):
        """Handle script text modifications.
        
        Updates modified state and window title to indicate unsaved changes.
        """
        self.script_editor.is_modified = True
        if not self.file_path_label.text().startswith("*"):
            self.file_path_label.setText("*" + self.file_path_label.text())
    
    def start_recording(self):
        """Start recording SAP transactions.
        
        Enables manual action recording interface.
        """
        self.transaction_recorder.start_recording()
        self.record_start_btn.setEnabled(False)
        self.record_stop_btn.setEnabled(True)
        self.recorded_actions_list.clear()
        self.show_status_message("Recording started")
    
    def stop_recording(self):
        """Stop recording SAP transactions.
        
        Disables recording and keeps recorded actions available for script generation.
        """
        self.transaction_recorder.stop_recording()
        self.record_start_btn.setEnabled(True)
        self.record_stop_btn.setEnabled(False)
        self.show_status_message("Recording stopped")
    
    def add_manual_action(self):
        """Add a manually entered action to the recording.
        
        Gets action type and details from input fields and adds to recording.
        """
        if not self.transaction_recorder.recording:
            QMessageBox.warning(self, "Not Recording", "Please start recording first")
            return
        
        action_type = self.action_type_combo.currentText()
        details_str = self.action_details_input.text()
        
        if not details_str:
            QMessageBox.warning(self, "Missing Details", "Please enter action details")
            return
        
        details = {"details": details_str}
        self.transaction_recorder.add_action(action_type, details)
        
        item_text = f"{action_type}: {details_str}"
        self.recorded_actions_list.addItem(item_text)
        self.action_details_input.clear()
        self.show_status_message(f"Action added: {action_type}")
    
    def generate_script_from_recording(self):
        """Generate Python script from recorded transactions.
        
        Creates a new script from the recorded actions and loads it into the editor.
        """
        if not self.transaction_recorder.recorded_actions:
            QMessageBox.warning(self, "No Actions", "Please record some actions first")
            return
        
        script_name = self.record_name_input.text() or "recorded_script"
        script_content = self.transaction_recorder.generate_script_from_recording(script_name)
        
        self.script_text_edit.setText(script_content)
        self.file_path_label.setText(f"[Generated] {script_name}.py")
        self.current_script_content = script_content
        self.tab_widget.setCurrentIndex(1)
        self.show_status_message(f"Script generated: {script_name}")
    
    def browse_script_file(self):
        """Open file browser for selecting script to execute.
        
        Updates the executor file input with selected script path.
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select Script", "",
            "Python Files (*.py);;All Files (*)"
        )
        
        if file_path:
            self.executor_file_input.setText(file_path)
    
    def execute_script(self):
        """Execute the selected script file.
        
        Validates script path and runs it in a separate thread.
        """
        script_path = self.executor_file_input.text()
        
        if not script_path:
            QMessageBox.warning(self, "No Script", "Please select a script file")
            return
        
        if not os.path.exists(script_path):
            QMessageBox.critical(self, "File Not Found", f"Script not found: {script_path}")
            return
        
        self.execute_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.output_text.clear()
        
        self.script_executor = ScriptExecutor(script_path)
        self.script_executor.output_signal.connect(self.append_output)
        self.script_executor.error_signal.connect(self.append_error)
        self.script_executor.finished_signal.connect(self.on_execution_finished)
        self.script_executor.start()
    
    def append_output(self, text: str):
        """Append output text to the execution output display.
        
        Args:
            text: Text to append to output.
        """
        self.output_text.append(text)
        self.progress_bar.setValue(self.progress_bar.value() + 10)
    
    def append_error(self, text: str):
        """Append error text to the execution output display.
        
        Args:
            text: Error text to append.
        """
        self.output_text.append(f"<span style='color:red;'>{text}</span>")
        self.progress_bar.setValue(self.progress_bar.value() + 10)
    
    def on_execution_finished(self):
        """Handle completion of script execution.
        
        Updates UI to show execution is complete.
        """
        self.execute_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.show_status_message("Script execution completed")
    
    def clear_output(self):
        """Clear the execution output display.
        
        Removes all text from the output text area.
        """
        self.output_text.clear()
    
    def browse_scripts_directory(self):
        """Open directory browser for selecting scripts directory.
        
        Updates the settings directory input.
        """
        directory = QFileDialog.getExistingDirectory(
            self, "Select Scripts Directory"
        )
        
        if directory:
            self.scripts_dir_input.setText(directory)
    
    def save_settings(self):
        """Save application settings.
        
        Writes current settings to configuration file.
        """
        settings = {
            "scripts_directory": self.scripts_dir_input.text(),
            "connection_timeout": self.timeout_spinbox.value(),
            "auto_save": self.auto_save_checkbox.isChecked()
        }
        
        try:
            with open("sap_manager_settings.json", 'w') as f:
                json.dump(settings, f, indent=2)
            
            QMessageBox.information(self, "Settings Saved", "Settings saved successfully")
            self.show_status_message("Settings saved")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save settings: {str(e)}")
    
    def show_status_message(self, message: str):
        """Display a message in the status bar.
        
        Args:
            message: Message to display.
        """
        self.status_bar.showMessage(message)


def main():
    """Application entry point.
    
    Creates and runs the QApplication and main window.
    """
    app = QApplication(sys.argv)
    window = SAPScriptManagerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
