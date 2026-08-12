# SAP Script Manager - Quick Start Guide

Get up and running with SAP Script Manager in 5 minutes.

## Prerequisites

Ensure these are installed:
- Windows OS
- Python 3.6 or higher
- SAP GUI with scripting enabled
- Active SAP system login

## 5-Minute Setup

**Step 1: Install (2 minutes)**

```powershell
pip install -r requirements.txt
python -m pip install --upgrade pywin32
```

**Step 2: Enable SAP Scripting (1 minute)**

In SAP GUI:
1. Click "Customize Local Layout"
2. Go to Options → Scripting
3. Verify "Scripting is installed!" message
4. Check "Enable Scripting"
5. Click OK

**Step 3: Launch Application (30 seconds)**

```powershell
python sap_gui_manager.py
```

**Step 4: Test Connection (1.5 minutes)**

1. Go to "Session Manager" tab
2. Click "Refresh Sessions"
3. Select a session
4. Click "Connect to Session"
5. See confirmation in status bar

## Your First Script

**Step 1: Create Script**

1. Click "Script Editor" tab
2. Click "New Script"
3. Name it "MyFirstScript"

**Step 2: Write Code**

Replace template content with:

```python
import SAP

def main():
    try:
        SAP.sap_sess_attach("SAP Easy Access")
        
        print("Connected to SAP successfully")
        
        # Get current window title
        if SAP.sap_win_exists("SAP Easy Access"):
            print("Easy Access window found")
        
    except SAP.SAPException as e:
        print(f"Error: {e.message}")

if __name__ == "__main__":
    main()
```

**Step 3: Run Script**

1. Click "Run Script"
2. Go to "Script Executor" tab
3. See output: "Connected to SAP successfully"

Congratulations! Your first SAP automation script ran successfully.

## Common Actions

### Navigate to Transaction

```python
import SAP

SAP.sap_sess_attach("SAP Easy Access")

# Enter transaction code
SAP.sap_obj_value_set("usr/ctxt[0]", "SE38")

# Press Enter
SAP.sap_vkeys_send("Enter")
```

### Fill Form Field

```python
# Enter value in field
SAP.sap_obj_value_set("usr/ctxt[0]", "MyValue")

# Move to next field
SAP.sap_vkeys_send("Tab")

# Enter another value
SAP.sap_obj_value_set("usr/ctxt[1]", "AnotherValue")
```

### Click Button

```python
# Click button by ID
SAP.sap_obj_select("usr/btn[0]")
```

### Wait for Screen

```python
import time

# Add 2-second pause
time.sleep(2)

# Or wait until specific window appears
SAP.sap_vkeys_send_until_win_exists("Enter", "Report Output")
```

### Get Field Value

```python
# Read current value
value = SAP.sap_obj_value_get("usr/ctxt[0]")
print(f"Current value: {value}")
```

## Recording a Script

Automate SAP steps by recording them:

1. Go to "Transaction Recorder" tab
2. Click "Start Recording"
3. Add actions:
   - "object_set": usr/ctxt[0]:ZSE38
   - "key_send": Enter
   - "pause": 2
   - "object_set": usr/ctxt[1]:MYPROGRAM
   - "object_select": usr/btn[0]
4. Click "Stop Recording"
5. Enter name "MyRecorded"
6. Click "Generate Script"

Script automatically loads in editor with all your actions.

## Next Steps

1. Explore "Transaction Recorder" tab to learn recording
2. Read "USER_GUIDE.md" for complete documentation
3. Review "CODE_DOCUMENTATION.md" for API details
4. Create scripts for your SAP processes
5. Combine multiple scripts for complex workflows

## File Structure

```
SAP-scripting/
├── sap_gui_manager.py          Main application
├── SAP.py                       Core automation library
├── requirements.txt             Dependencies
├── README.md                    Project overview
├── QUICK_START.md              This file
├── USER_GUIDE.md               Complete user documentation
├── CODE_DOCUMENTATION.md       Developer documentation
├── EVALUATION_AND_PYTHON_PORT.md  Architecture overview
└── sap_scripts/                Scripts directory
    ├── MyFirstScript.py
    ├── MyRecorded.py
    └── (your scripts here)
```

## Common Errors and Solutions

**Error: "Unable to find an active SAP session"**
- Solution: Open SAP GUI first and log in

**Error: "Object not found"**
- Solution: Verify object_id is correct using SAP Scripting Wizard

**Error: "ModuleNotFoundError"**
- Solution: Run `pip install -r requirements.txt`

**Script gets stuck waiting**
- Solution: Increase timeout or check if window actually opens

## Key Keyboard Shortcuts in Editor

- Ctrl+A: Select all
- Ctrl+C: Copy
- Ctrl+V: Paste
- Ctrl+Z: Undo
- Ctrl+Y: Redo

## Need Help?

1. Check error messages in output
2. Review similar examples in USER_GUIDE.md
3. Test with simpler scripts first
4. Verify SAP configuration and access

## Quick Reference

### Essential Functions

```python
# Connection
SAP.sap_sess_attach(window_title)
SAP.sap_sess_create(transaction)

# Object interaction
SAP.sap_obj_value_set(id, value)
SAP.sap_obj_value_get(id)
SAP.sap_obj_select(id)

# Input
SAP.sap_vkeys_send(keys)

# Window check
SAP.sap_win_exists(title)
```

### Virtual Keys

```
"Enter"         - Execute
"Escape"        - Cancel
"Tab"           - Next field
"Shift+Tab"     - Previous field
"F1"-"F12"      - Function keys
"Ctrl+S"        - Save
"Ctrl+A"        - Select all
"Page up"       - Previous page
"Page down"     - Next page
```

## Congratulations!

You're now ready to automate your SAP processes with Python.

Create scripts, test them, and integrate them into your workflows.

For advanced usage, consult the full USER_GUIDE.md documentation.

Happy automating!
