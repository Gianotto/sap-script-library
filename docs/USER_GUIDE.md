# SAP Script Manager - User Guide

## Getting Started

### Installation

**Step 1: Install Python Dependencies**

Open PowerShell or Command Prompt and run:

```powershell
pip install -r requirements.txt
```

This installs PyQt5 and pywin32.

**Step 2: Post-install pywin32**

After installation, run:

```powershell
python -m pip install --upgrade pywin32
python path\to\site-packages\pywin32_postinstall.py -install
```

This registers COM interfaces required for SAP integration.

**Step 3: Verify SAP Configuration**

Launch SAP GUI and verify scripting is enabled:

1. Open SAP Logon or SAP GUI
2. Log into SAP system
3. Select "Customize Local Layout" from toolbar
4. Go to Options
5. Select Scripting tab
6. Verify message "Scripting is installed!"
7. Check "Enable Scripting"
8. Uncheck notifications if preferred
9. Click OK

**Step 4: Launch Application**

Run the application:

```powershell
python sap_gui_manager.py
```

The main window opens with five tabs.

## Main Interface

The application window contains five tabs for different operations:

1. **Session Manager**: Connect to and manage SAP sessions
2. **Script Editor**: Create and edit Python automation scripts
3. **Transaction Recorder**: Record SAP interactions
4. **Script Executor**: Run scripts and view output
5. **Settings**: Configure application preferences

## Session Manager Tab

Manages connections to SAP systems.

### Viewing Available Sessions

Click "Refresh Sessions" to display all open SAP GUI sessions:

- Sessions are listed in the "Available Sessions" box
- Each session title shows the transaction or window name
- Click any session to view its details

### Session Details

After selecting a session, its information displays:

- Session ID: Internal identifier
- Title: Window or transaction name
- Created: Timestamp when session was established
- Status: Current connection state

### Connecting to a Session

To connect to an existing SAP session:

1. Click "Refresh Sessions"
2. Select desired session from list
3. Click "Connect to Session"
4. Status bar confirms connection

The application maintains the connection for script execution.

### Creating New Sessions

To open a new SAP session:

1. Click "Create New Session"
2. Enter optional transaction code in dialog
3. Click OK

The new session opens in SAP GUI. If you entered a transaction code, it launches automatically.

## Script Editor Tab

Create and modify Python automation scripts.

### Creating a New Script

To start a new script:

1. Click "New Script"
2. Enter script name in dialog
3. Click OK

A template script appears with basic structure including:
- Documentation header
- Import statements
- Main function
- Error handling

### Opening Existing Scripts

To open a previously saved script:

1. Click "Open Script"
2. Browse to script file location
3. Select Python file
4. Click Open

The script loads into the editor with syntax highlighting applied.

### Editing Scripts

The editor provides:

- Syntax highlighting for Python code
- Keywords in blue
- Strings in green
- Comments in gray
- Numbers in purple

Write your SAP automation code in the editor. The status bar shows modifications with asterisk (*) in the file path.

### Script Structure

Your scripts typically follow this structure:

```python
"""
SAP Script: TransferData
Automation for data movement in SAP
"""

import SAP
import time

def main():
    try:
        # Connect to SAP
        SAP.sap_sess_attach("SAP Easy Access")
        
        # Navigate to transaction
        SAP.sap_obj_value_set("usr/ctxt[0]", "ZSE38")
        SAP.sap_vkeys_send("Enter")
        
        # Wait for screen
        time.sleep(2)
        
        # Perform actions
        SAP.sap_obj_value_set("usr/ctxt[1]", "MyProgram")
        SAP.sap_obj_select("usr/btn[0]")
        
    except SAP.SAPException as e:
        print(f"Error: {e.message} (Code: {e.error_code})")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
```

### Available SAP Functions

Use these functions in your scripts:

**Session Management**
- `SAP.sap_sess_attach(window_title)` - Connect to session
- `SAP.sap_sess_create(transaction)` - Create new session

**Object Interaction**
- `SAP.sap_obj_value_set(object_id, value)` - Set field value
- `SAP.sap_obj_value_get(object_id)` - Read field value
- `SAP.sap_obj_select(object_id)` - Click/select element
- `SAP.sap_obj_deselect(object_id)` - Deselect element

**Property Management**
- `SAP.sap_obj_property_set(object_id, property, value)` - Set property
- `SAP.sap_obj_property_get(object_id, property)` - Read property

**Input Control**
- `SAP.sap_vkeys_send(keys)` - Send virtual keys
- `SAP.sap_vkeys_send_until_win_exists(keys, window_title)` - Send keys until window appears

**Window Management**
- `SAP.sap_win_exists(title)` - Check if window exists
- `SAP.sap_win_close(title)` - Close window

**Virtual Key Codes**

Common keys for vkeys_send:
- "Enter" - Execute
- "Escape" or "F12" - Cancel
- "F1" through "F12" - Function keys
- "Ctrl+S" - Save
- "Ctrl+A" - Select all
- "Shift+F1" - Help
- "Page up", "Page down" - Navigation

### Saving Scripts

To save the current script:

1. Click "Save Script"
2. If new script, choose file location and name
3. File saved to sap_scripts directory by default
4. Asterisk (*) removed from file path

Auto-save can be enabled in Settings tab.

### Running Scripts

To execute the current script:

1. Click "Run Script"
2. Script automatically saved
3. Application switches to "Script Executor" tab
4. Output appears in real-time

## Transaction Recorder Tab

Automatically generate scripts from recorded SAP interactions.

### Starting Recording

To record SAP transactions:

1. Click "Start Recording"
2. Button becomes disabled, "Stop Recording" becomes enabled
3. Status bar shows "Recording started"

### Recording Actions Manually

While recording, add actions by:

1. Select action type from dropdown:
   - object_set: Set field value
   - object_select: Click element
   - key_send: Send keyboard keys
   - window_wait: Wait for window to appear
   - pause: Wait for seconds

2. Enter action details in text field:
   - For object_set: "object_id:value"
   - For object_select: "object_id"
   - For key_send: "Enter"
   - For window_wait: "Window Title"
   - For pause: "2" (seconds)

3. Click "Add Action"

Action appears in "Recorded Actions" list.

### Example Recording Session

To record a simple data entry:

1. Start Recording
2. Add action: type=object_set, details="usr/ctxt[0]:ZSE38"
3. Add action: type=key_send, details="Enter"
4. Add action: type=pause, details="2"
5. Add action: type=object_set, details="usr/ctxt[1]:MYDATA"
6. Add action: type=object_select, details="usr/btn[0]"
7. Stop Recording

### Generating Script from Recording

After recording actions:

1. Enter script name in "Enter script name" field
2. Click "Generate Script"
3. Script automatically loads into "Script Editor" tab
4. Review generated code
5. Make any necessary adjustments
6. Save or run the script

The generated script contains all recorded actions in executable Python code.

### Viewing Generated Code

The generated code follows this pattern:

```python
"""
SAP Script: my_recording
Generated from recording: 2026-08-12T15:30:45.123456
"""

import SAP
import time

def main():
    """Playback of recorded SAP transactions."""
    try:
        SAP.sap_sess_attach("SAP Easy Access")
        
        SAP.sap_obj_value_set("usr/ctxt[0]", "ZSE38")
        SAP.sap_vkeys_send("Enter")
        time.sleep(2)
        SAP.sap_obj_value_set("usr/ctxt[1]", "MYDATA")
        SAP.sap_obj_select("usr/btn[0]")
        
    except SAP.SAPException as e:
        print(f"SAP Error: {e.message} (Code: {e.error_code})")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
```

## Script Executor Tab

Execute Python scripts and monitor results.

### Selecting a Script

To choose script for execution:

1. Click "Browse" to open file browser
2. Navigate to script location
3. Select Python file
4. Click Open

Or manually enter path in "Script to Execute" field.

### Executing Scripts

To run the selected script:

1. Script path appears in text field
2. Click "Execute Script"
3. Progress bar appears
4. Status bar shows "Executing script"
5. Output updates in real-time

### Monitoring Output

The execution output displays:

- Script startup message
- All print() output
- Any error messages (in red)
- Completion message

Output scrolls automatically as script runs.

### Stopping Execution

Scripts run to completion without user intervention. To stop execution, close the application window.

### Clearing Output

To clear the output display:

Click "Clear Output"

Previous execution output is removed, ready for next run.

### Troubleshooting Execution

If script execution fails:

1. Check error message in output (red text)
2. Common issues:
   - SAP session not connected: Call sap_sess_attach first
   - Invalid object ID: Verify object_id parameter
   - Window not found: Increase wait time or check window title
   - Connection timeout: SAP GUI not responding

3. Modify script in Script Editor tab
4. Save and run again

## Settings Tab

Configure application preferences.

### Scripts Directory

Sets where scripts are saved and loaded:

1. Enter directory path or click "Browse"
2. Default is "sap_scripts" in application directory
3. Directory created automatically if it doesn't exist

### Connection Timeout

Sets maximum seconds to wait for SAP response:

1. Use spinner to set timeout (5-300 seconds)
2. Default is 30 seconds
3. Higher values for slow systems or slow networks

### Auto-save

Enables automatic script saving:

1. Check "Auto-save scripts" to enable
2. Scripts save automatically on modification
3. Useful for preventing loss of work

### Saving Settings

To apply settings changes:

1. Modify desired settings
2. Click "Save Settings"
3. Settings written to sap_manager_settings.json
4. Message confirms save
5. Settings load automatically on next startup

## Common Workflows

### Workflow 1: Simple Field Entry

Task: Fill form and submit

1. Open Script Editor
2. Create new script
3. Write code:
   ```python
   SAP.sap_sess_attach("SAP Easy Access")
   SAP.sap_obj_value_set("usr/ctxt[0]", "ZT001")
   SAP.sap_obj_value_set("usr/ctxt[1]", "100.00")
   SAP.sap_obj_select("usr/btn[0]")
   ```
4. Save script
5. Run from Script Executor tab

### Workflow 2: Multi-step Transaction

Task: Navigate through multiple screens

1. Connect to session in Session Manager
2. Open Script Editor
3. Write code for first screen
4. Add vkeys_send("Enter") to proceed
5. Add wait for next screen
6. Write code for second screen
7. Repeat as needed
8. Save and execute

### Workflow 3: Record and Replay

Task: Capture actions then replay

1. Open Transaction Recorder tab
2. Click Start Recording
3. Manually add actions for your SAP steps
4. Click Stop Recording
5. Enter script name
6. Click Generate Script
7. Script opens in Editor
8. Run from Executor tab whenever needed

### Workflow 4: Batch Processing

Task: Process multiple records

1. Create script with loop:
   ```python
   data = ["Record1", "Record2", "Record3"]
   for record in data:
       SAP.sap_obj_value_set("usr/ctxt[0]", record)
       SAP.sap_obj_select("usr/btn[0]")
   ```
2. Save script
3. Execute once to process all records

## Tips and Best Practices

### Performance

- Use short pauses between actions
- Avoid unnecessary waits
- Cache object IDs if used repeatedly
- Close unused sessions

### Reliability

- Always use try/except for error handling
- Check window existence before proceeding
- Add meaningful pauses after navigation
- Log important steps with print()

### Debugging

- Add print statements to track execution
- Use shorter scripts for testing
- Test individual functions first
- Check SAP GUI responsiveness

### Organization

- Create separate scripts for different tasks
- Use meaningful script names
- Add documentation comments
- Group related functionality

### SAP-Specific

- Use full transaction codes with /n prefix
- Remember SAP window indexing starts at 0
- Some fields require specific key sequences
- Test in development system first

## Keyboard Shortcuts

While not built-in, you can add keyboard shortcuts to Python scripts:

```python
from PyQt5.QtWidgets import QApplication, QKeySequence
from PyQt5.QtGui import QKeySequence
```

## Troubleshooting

### Application Won't Start

**Problem**: "ModuleNotFoundError: No module named 'PyQt5'"

**Solution**: Install PyQt5
```powershell
pip install PyQt5
```

**Problem**: "ModuleNotFoundError: No module named 'win32com'"

**Solution**: Install and configure pywin32
```powershell
pip install pywin32
python -m pip install --upgrade pywin32
python path\to\pywin32_postinstall.py -install
```

### SAP Connection Issues

**Problem**: "Error: Unable to find an active SAP session"

**Solution**:
- Launch SAP GUI first
- Log into SAP system
- Verify scripting is enabled in SAP
- Check SAP window title matches code

**Problem**: "Object not found" error

**Solution**:
- Verify object_id using SAP UI element inspection
- Use SAP's Scripting Wizard to get correct IDs
- Check window index [0], [1], etc. is correct
- Wait for screen to fully load before accessing

### Script Execution Issues

**Problem**: Script runs but no visible changes in SAP

**Solution**:
- Add print statements to verify execution
- Check script syntax in Editor tab
- Verify object IDs are correct
- Add pause times if screen loading slowly
- Check SAP permissions for user

**Problem**: Script gets stuck waiting for window

**Solution**:
- Increase window wait timeout in code
- Check window title exactly matches
- Verify action that should open window completes
- Close existing windows blocking navigation

### File Issues

**Problem**: "File not found" when opening script

**Solution**:
- Use Browse button instead of typing path
- Check file extension is .py
- Verify file hasn't been moved
- Check file permissions allow reading

**Problem**: "Permission denied" when saving

**Solution**:
- Check directory write permissions
- Verify scripts directory exists
- Use different directory in Settings
- Close any open file handles

## Getting Help

For additional assistance:

1. Check script error messages for details
2. Review SAP documentation for object IDs
3. Use SAP Scripting Wizard tool in SAP GUI
4. Test simple scripts before complex ones
5. Enable logging/debug output

## Advanced Features

### Custom Functions

Create reusable functions in scripts:

```python
def fill_form(field_id, value):
    SAP.sap_obj_value_set(field_id, value)
    SAP.sap_vkeys_send("Tab")

def click_button(button_id):
    SAP.sap_obj_select(button_id)
```

### Error Recovery

Implement retry logic:

```python
import time

max_attempts = 3
for attempt in range(max_attempts):
    try:
        SAP.sap_obj_value_set("usr/ctxt[0]", "DATA")
        break
    except SAP.SAPException:
        if attempt < max_attempts - 1:
            time.sleep(2)
        else:
            raise
```

### Data Integration

Read/write files for batch processing:

```python
import json

with open("input_data.json") as f:
    records = json.load(f)

for record in records:
    SAP.sap_obj_value_set("usr/ctxt[0]", record["id"])
    SAP.sap_obj_value_set("usr/ctxt[1]", record["value"])
```

This completes the user guide for SAP Script Manager. For detailed API documentation, refer to CODE_DOCUMENTATION.md.
