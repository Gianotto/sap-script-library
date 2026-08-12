# SAP Script Manager - Code Documentation

## Overview

The SAP Script Manager is a comprehensive Python application providing a graphical user interface for managing SAP automation scripts. The application enables users to create, edit, execute, and record SAP transactions with an intuitive interface.

## Architecture Overview

The application follows a modular architecture with distinct components:

```
┌─────────────────────────────────────────────────────────────┐
│            SAPScriptManagerApp (Main Window)                │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Session    │  │    Script    │  │  Transaction     │  │
│  │   Manager    │  │    Editor    │  │   Recorder       │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │    Script    │  │   Settings   │                        │
│  │   Executor   │  │   Manager    │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│           SAP.py Automation Library                         │
│     (COM Interface to SAP GUI Scripting)                    │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│              SAP GUI Scripting Interface                     │
│                  (SAP ERP System)                           │
└─────────────────────────────────────────────────────────────┘
```

## Module Components

### 1. PythonSyntaxHighlighter

Provides Python syntax highlighting in the script editor.

**Class Methods:**

- `__init__(document)`: Initialize highlighter with QTextDocument
- `_create_format(color, bold, italic)`: Create styled text format
- `highlightBlock(text)`: Apply highlighting to code block

**Functionality:**
- Highlights keywords (blue, bold)
- Highlights strings (green)
- Highlights comments (gray, italic)
- Highlights numbers (purple)

**Example Usage:**
```python
highlighter = PythonSyntaxHighlighter(text_edit.document())
```

### 2. SessionManager

Manages all SAP GUI session interactions and lifecycle.

**Attributes:**
- `sessions`: List of active session dictionaries
- `current_session_id`: Currently active session identifier
- `session_counter`: Counter for generating unique session IDs

**Key Methods:**

**get_available_sessions() → List[str]**

Queries SAP GUI scripting interface for running sessions.

Returns:
  - List of session titles
  
Raises:
  - SAPException: If unable to query sessions

Example:
```python
manager = SessionManager()
sessions = manager.get_available_sessions()
print(f"Available sessions: {sessions}")
```

**connect_to_session(window_title) → bool**

Attaches to a specific SAP session.

Args:
  - window_title: Title of SAP window to connect (default: "SAP Easy Access")

Returns:
  - True if connection successful

Raises:
  - SAPException: If connection fails

Example:
```python
success = manager.connect_to_session("SAP Easy Access")
```

**create_new_session(transaction) → bool**

Creates a new SAP session.

Args:
  - transaction: Optional transaction code to run in new session

Returns:
  - True if session created

Raises:
  - SAPException: If creation fails

Example:
```python
manager.create_new_session("SE38")
```

**get_session_info(session_id) → Optional[Dict]**

Retrieves metadata about a session.

Args:
  - session_id: The session identifier

Returns:
  - Dictionary with session information or None

Example:
```python
info = manager.get_session_info("session_0")
print(f"Created: {info['created']}, Status: {info['status']}")
```

**close_session(window_title) → bool**

Closes a SAP window.

Args:
  - window_title: Title of window to close

Returns:
  - True if window closed

Example:
```python
manager.close_session("Program Editor")
```

### 3. ScriptEditor

Manages script file operations and editing state.

**Attributes:**
- `current_file`: Path to currently open script
- `is_modified`: Modification flag
- `scripts_directory`: Directory for storing scripts

**Key Methods:**

**create_new_script(name, template) → str**

Creates new script with optional template.

Args:
  - name: Script name without extension
  - template: Optional initial content

Returns:
  - Script content string

Example:
```python
editor = ScriptEditor()
content = editor.create_new_script("my_automation")
```

**open_script(file_path) → Tuple[bool, str]**

Opens existing script file.

Args:
  - file_path: Path to script

Returns:
  - Tuple of (success, content_or_error)

Example:
```python
success, content = editor.open_script("sap_scripts/my_script.py")
if success:
    print(content)
else:
    print(f"Error: {content}")
```

**save_script(file_path, content) → Tuple[bool, str]**

Saves script content to file.

Args:
  - file_path: Target file path
  - content: Script content to save

Returns:
  - Tuple of (success, message)

Example:
```python
success, msg = editor.save_script("sap_scripts/script.py", "print('Hello')")
print(msg)
```

**list_scripts() → List[str]**

Lists all available scripts.

Returns:
  - Sorted list of script filenames

Example:
```python
scripts = editor.list_scripts()
for script in scripts:
    print(f"Found: {script}")
```

### 4. TransactionRecorder

Records user interactions for playback and analysis.

**Attributes:**
- `recording`: Boolean recording state
- `recorded_actions`: List of action dictionaries
- `start_time`: Recording start timestamp

**Key Methods:**

**start_recording()**

Begins recording user actions.

Example:
```python
recorder = TransactionRecorder()
recorder.start_recording()
```

**stop_recording() → List[Dict]**

Stops recording and returns actions.

Returns:
  - List of recorded action dictionaries

Example:
```python
actions = recorder.stop_recording()
```

**add_action(action_type, details)**

Records single user action.

Args:
  - action_type: Type of action
  - details: Action-specific data

Supported action types:
  - "object_set": Set field value
  - "object_select": Click/select element
  - "key_send": Send virtual keys
  - "window_wait": Wait for window
  - "pause": Wait for time

Example:
```python
recorder.add_action("object_set", {
    "object_id": "usr/ctxt[0]",
    "value": "ZSE38"
})
```

**generate_script_from_recording(script_name) → str**

Generates Python script from recordings.

Args:
  - script_name: Name for generated script

Returns:
  - Complete Python script content

Example:
```python
script = recorder.generate_script_from_recording("my_recorded_script")
print(script)
```

### 5. ScriptExecutor

Executes scripts in separate thread.

**Signals:**
- `output_signal`: Emitted with output text
- `error_signal`: Emitted with error text
- `finished_signal`: Emitted when execution completes

**Key Methods:**

**__init__(script_path)**

Initialize executor with script path.

Args:
  - script_path: Path to Python script

Example:
```python
executor = ScriptExecutor("scripts/automation.py")
executor.output_signal.connect(print_output)
executor.start()
```

**run()**

Execute the script (called by thread).

Captures stdout and stderr, emits signals with output.

### 6. SAPScriptManagerApp

Main application window containing all UI components.

**Attributes:**
- `session_manager`: SessionManager instance
- `script_editor`: ScriptEditor instance
- `transaction_recorder`: TransactionRecorder instance
- `script_executor`: ScriptExecutor instance (when running)

**Tab Components:**

**1. Session Manager Tab**

Interface for SAP session management:
- List available sessions
- Connect to session
- Create new session
- View session details

Key widgets:
  - `session_list`: QListWidget showing sessions
  - `session_info_text`: QTextEdit showing details

Methods:
  - `refresh_sessions()`: Update session list
  - `connect_to_session()`: Connect to selected session
  - `create_new_session()`: Create new session
  - `show_session_info()`: Display session details

**2. Script Editor Tab**

Python script editing interface:
- Create new scripts
- Open existing scripts
- Edit with syntax highlighting
- Save and run scripts

Key widgets:
  - `script_text_edit`: QTextEdit with highlighter
  - `file_path_label`: Shows current file path
  
Methods:
  - `new_script()`: Create new script
  - `open_script()`: Open existing script
  - `save_script()`: Save current script
  - `run_script()`: Execute script
  - `on_script_modified()`: Track changes

**3. Transaction Recorder Tab**

Record SAP user interactions:
- Start/stop recording
- Add manual actions
- View recorded actions
- Generate scripts

Key widgets:
  - `recorded_actions_list`: QListWidget of actions
  - `action_type_combo`: QComboBox for action type
  - `action_details_input`: QLineEdit for details

Methods:
  - `start_recording()`: Begin recording
  - `stop_recording()`: End recording
  - `add_manual_action()`: Add custom action
  - `generate_script_from_recording()`: Create script

**4. Script Executor Tab**

Execute and monitor scripts:
- Select script file
- Execute script
- View output in real-time
- Monitor progress

Key widgets:
  - `executor_file_input`: QLineEdit for file path
  - `output_text`: QTextEdit for output
  - `progress_bar`: QProgressBar showing status

Methods:
  - `execute_script()`: Run selected script
  - `append_output()`: Add output text
  - `append_error()`: Add error text
  - `clear_output()`: Clear output display
  - `on_execution_finished()`: Handle completion

**5. Settings Tab**

Configure application preferences:
- Scripts directory
- Connection timeout
- Auto-save setting

Key widgets:
  - `scripts_dir_input`: QLineEdit for directory
  - `timeout_spinbox`: QSpinBox for timeout
  - `auto_save_checkbox`: QCheckBox

Methods:
  - `save_settings()`: Write settings to file
  - `browse_scripts_directory()`: Directory selection

**Main Methods:**

**init_ui()**

Initialize all UI components.

**create_session_tab() → QWidget**

Create and return session manager tab.

**create_script_editor_tab() → QWidget**

Create and return script editor tab.

**create_recorder_tab() → QWidget**

Create and return transaction recorder tab.

**create_executor_tab() → QWidget**

Create and return script executor tab.

**create_settings_tab() → QWidget**

Create and return settings tab.

**show_status_message(message)**

Display status bar message.

Args:
  - message: Message to display

## Signal/Slot Connections

The application uses PyQt5 signal/slot mechanism for component communication:

```
User Action (Button Click, etc.)
         ↓
    Qt Signal
         ↓
    Connected Slot
         ↓
    Component Method
         ↓
    Update UI/Process Data
```

Example signal connections:
```python
refresh_btn.clicked.connect(self.refresh_sessions)
save_btn.clicked.connect(self.save_script)
execute_btn.clicked.connect(self.execute_script)
self.script_executor.output_signal.connect(self.append_output)
```

## Data Flow

### Script Execution Flow

```
User clicks Execute
         ↓
execute_script() validates input
         ↓
ScriptExecutor thread created
         ↓
Script loaded and executed
         ↓
Output captured via stdout redirect
         ↓
output_signal emitted
         ↓
append_output() updates UI
         ↓
finished_signal emitted
         ↓
UI updated to show completion
```

### Recording to Script Flow

```
User clicks Start Recording
         ↓
start_recording() initializes
         ↓
User manually adds actions
         ↓
add_manual_action() records each action
         ↓
User clicks Stop Recording
         ↓
stop_recording() finalizes
         ↓
User clicks Generate Script
         ↓
generate_script_from_recording() creates code
         ↓
Script loaded into editor
         ↓
User can save or execute
```

## Configuration

Application settings are stored in `sap_manager_settings.json`:

```json
{
  "scripts_directory": "sap_scripts",
  "connection_timeout": 30,
  "auto_save": true
}
```

Settings are loaded on startup and saved via Settings tab.

## Error Handling

The application implements multi-level error handling:

1. **SAPException**: Custom exception for SAP-specific errors
   - Error code for classification
   - Descriptive message
   - Propagated to UI as message boxes

2. **Try/Except Blocks**: All external operations wrapped
   - File I/O
   - SAP API calls
   - Thread execution

3. **User Feedback**: All errors shown via:
   - Message boxes for critical errors
   - Status bar for informational messages
   - Output text for execution errors

## Performance Considerations

1. **Threading**: Script execution runs in separate thread to prevent UI freezing
2. **File Operations**: Synchronous for simplicity
3. **SAP Connections**: Kept minimal, created only when needed
4. **Syntax Highlighting**: Incremental highlighting per block

## Extension Points

The application can be extended at these points:

1. **New Actions**: Add new action types to TransactionRecorder
2. **Custom Executors**: Extend ScriptExecutor for different script types
3. **Session Types**: Extend SessionManager for non-SAP systems
4. **UI Customization**: Modify tab layouts and components
5. **Settings**: Add new configuration options

## Dependency Management

### PyQt5
- Version: >= 5.15.0
- Used for: GUI framework, signals/slots, widgets
- Alternatives: tkinter (simpler but less feature-rich), PySide2 (similar to PyQt5)

### pywin32
- Version: >= 300
- Used for: COM interface to SAP GUI
- Alternatives: comtypes (lower-level)

### SAP.py
- Local module providing automation functions
- Wraps SAP GUI scripting interface
- Depends on pywin32

## Testing Recommendations

1. **Unit Tests**: Test individual component methods
2. **Integration Tests**: Test component interactions
3. **UI Tests**: Test tab functionality
4. **SAP Tests**: Test against live SAP system (dev environment only)

Example test structure:
```python
import unittest

class TestSessionManager(unittest.TestCase):
    def setUp(self):
        self.manager = SessionManager()
    
    def test_get_available_sessions(self):
        sessions = self.manager.get_available_sessions()
        self.assertIsInstance(sessions, list)
```

## Debugging Tips

1. Enable Python logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. Print debug info to output:
```python
print(f"Debug: current_file = {self.script_editor.current_file}")
```

3. Use Qt debugging:
```python
from PyQt5.QtCore import qDebug
qDebug("Debug message")
```

4. SAP error investigation:
```python
try:
    sap_sess_attach("Window Title")
except SAPException as e:
    print(f"Error {e.error_code}: {e.message}")
```
