# SAP Script Manager - Installation and Startup Guide

## Complete Setup Process

This guide walks through the complete installation, configuration, and first launch of SAP Script Manager.

## Prerequisite Check

Before installing, verify you have:

1. **Windows Operating System**
   - Windows XP or later
   - Check: Open PowerShell, run `[System.Environment]::OSVersion`

2. **Python 3.6 or Higher**
   - Download from python.org if not installed
   - Check: Run `python --version` in PowerShell

3. **SAP GUI Access**
   - SAP GUI client installed and working
   - Access to SAP system (development/test)
   - Active SAP user account

4. **Administrator Privileges**
   - May be needed for pywin32 configuration
   - Have admin account available

## Step 1: Install Python Dependencies

### Open PowerShell

1. Press Win+X
2. Select "Windows PowerShell (Admin)"
3. Or search for "PowerShell" and run as Administrator

### Navigate to Project Directory

```powershell
cd "C:\Dev\SAP-scripting"
```

Replace with actual path if different.

### Install Required Packages

```powershell
pip install -r requirements.txt
```

This installs:
- PyQt5 (GUI framework)
- pywin32 (Windows COM interface)

**Expected output**: "Successfully installed PyQt5 and pywin32"

### Verify Installation

```powershell
python -c "import PyQt5; print('PyQt5 installed')"
python -c "import win32com; print('pywin32 installed')"
```

Both commands should print success messages.

## Step 2: Configure pywin32

The pywin32 package requires COM registration for SAP integration.

### Find Python Site-Packages

```powershell
python -c "import site; print(site.getsitepackages()[0])"
```

This prints the full path. Copy it. Example:
`C:\Users\YourName\AppData\Local\Programs\Python\Python39\Lib\site-packages`

### Run Post-Install Script

```powershell
# Replace path with output from previous command
python "C:\Users\YourName\AppData\Local\Programs\Python\Python39\Lib\site-packages\pywin32_postinstall.py" -install
```

**Expected output**: "Registered pywin32..."

If you get an error about permissions, run PowerShell as Administrator.

## Step 3: Configure SAP GUI for Scripting

This is a one-time configuration in SAP GUI.

### Launch SAP GUI

1. Open SAP Logon or SAP GUI client
2. Verify you can log in to your SAP system
3. Select any system and log in

### Enable Scripting

1. After login, locate the toolbar
2. Click **"Customize Local Layout"** button (usually in top right)
3. In the menu, click **"Options"**
4. A dialog opens with tabs
5. Click the **"Scripting"** tab
6. You should see message: **"Scripting is installed!"**
7. Check the box: **"Enable Scripting"** ✓
8. Optionally uncheck notification boxes
9. Click **"OK"**

### Verify Scripting is Enabled

1. Back in SAP, click "Customize Local Layout" again
2. Click "Script Development Tools"
3. Select "Do a Hit Test on the Window"
4. Move mouse to any UI element
5. You should see "Scripting Wizard" window appear
6. Scripting is working!
7. Close this window

## Step 4: Launch the Application

### Start Application

In PowerShell, while in the SAP-scripting directory:

```powershell
python sap_gui_manager.py
```

**Expected output**: Application window opens with 5 tabs

### Window Features

You see:
- **Title**: "SAP Script Manager"
- **Tabs**: Session Manager, Script Editor, Transaction Recorder, Script Executor, Settings
- **Status Bar**: At bottom showing application status

The application is running!

## Step 5: Test Basic Functionality

### Test Session Connection

1. In the application, go to **"Session Manager"** tab
2. Click **"Refresh Sessions"** button
3. If SAP GUI is open and you're logged in, you see session listed
4. Click to select it
5. Click **"Connect to Session"**
6. Status bar shows: "Connected to session: ..."

Success! Connection is working.

### Test Script Creation

1. Go to **"Script Editor"** tab
2. Click **"New Script"**
3. Name it "TestScript"
4. Edit text to say `print("Hello from SAP Script Manager")`
5. Click **"Run Script"**
6. Go to **"Script Executor"** tab
7. See output: "Hello from SAP Script Manager"

Success! Script execution works.

## Step 6: Load Example Scripts

Example scripts are provided in the `sap_scripts` directory.

### View Example Script

1. Go to **"Script Editor"** tab
2. Click **"Open Script"**
3. Navigate to `sap_scripts` directory
4. Select `example_automation.py`
5. Click **"Open"**

The example script loads showing:
- How to connect to SAP
- How to navigate transactions
- How to fill forms
- How to handle errors

### View Batch Processing Example

1. Click **"Open Script"** again
2. Select `batch_processing_example.py`
3. This shows how to process multiple records

Both scripts are fully commented and demonstrate real workflows.

## Configuration File

After running the application once, a configuration file is created:

**File**: `sap_manager_settings.json`

Contains:
```json
{
  "scripts_directory": "sap_scripts",
  "connection_timeout": 30,
  "auto_save": true
}
```

This file persists your settings between sessions.

## Troubleshooting Installation

### Problem: "ModuleNotFoundError: No module named 'PyQt5'"

**Solution**:
```powershell
pip install PyQt5 --upgrade
```

Then try launching again.

### Problem: "pywin32 post install failed"

**Solution**:
1. Run PowerShell as Administrator
2. Re-run: `python "path\to\pywin32_postinstall.py" -install`

### Problem: "Unable to find an active SAP session"

**Solution**:
1. Ensure SAP GUI is running
2. Log into SAP system
3. Return to application
4. Click "Refresh Sessions"

### Problem: "Scripting is not installed" message in SAP

**Solution**:
1. Consult SAP system administrator
2. SAP GUI scripting support may need to be installed
3. This is a system configuration, not application issue

### Problem: Application won't start

**Solution**:
```powershell
# Verify Python works
python --version

# Verify imports work
python -c "from PyQt5 import QtWidgets"
python -c "import win32com.client"

# If imports fail, reinstall:
pip uninstall PyQt5 pywin32
pip install -r requirements.txt
```

## First Automation Script

Now that installation is complete, try your first automation:

### Create Script in Editor

1. Go to Script Editor tab
2. Click "New Script"
3. Name it "FirstAutomation"
4. Replace template with:

```python
import SAP

try:
    SAP.sap_sess_attach("SAP Easy Access")
    print("Connected to SAP successfully!")
    
except SAP.SAPException as e:
    print(f"Error: {e.message}")
```

### Run the Script

1. Click "Run Script"
2. Switch to "Script Executor" tab
3. See output: "Connected to SAP successfully!"

Your first SAP automation runs!

## Next Steps After Installation

1. **Read Quick Start** (`QUICK_START.md`)
   - 5-minute introduction to features

2. **Review User Guide** (`USER_GUIDE.md`)
   - Complete instructions for each tab
   - Common workflows
   - Tips and tricks

3. **Study Examples** (`sap_scripts` directory)
   - example_automation.py
   - batch_processing_example.py

4. **Create Your First Script**
   - Navigate to transaction
   - Fill some forms
   - Submit data

5. **Try Recording**
   - Use Transaction Recorder tab
   - Record your SAP steps
   - Generate script automatically

6. **Explore Advanced Features**
   - See CODE_DOCUMENTATION.md for all functions
   - Build complex workflows
   - Integrate with your processes

## File Organization

After setup, your directory looks like:

```
SAP-scripting/
├── sap_gui_manager.py          (Application - don't modify)
├── SAP.py                      (Library - don't modify)
├── requirements.txt            (Dependencies - reference)
├── sap_manager_settings.json   (Your settings - auto-created)
│
├── README.md                   (Read first for overview)
├── QUICK_START.md             (Read for quick introduction)
├── USER_GUIDE.md              (Detailed instructions)
├── CODE_DOCUMENTATION.md      (Technical reference)
│
└── sap_scripts/               (Your scripts here)
    ├── example_automation.py
    ├── batch_processing_example.py
    └── (your new scripts)
```

## Uninstallation

To remove the application:

```powershell
# Remove Python packages
pip uninstall PyQt5 pywin32

# Delete application directory
Remove-Item -Recurse "C:\Dev\SAP-scripting"
```

Your scripts in `sap_scripts` directory remain unless you delete them.

## Getting Help

### Built-in Help

1. Status bar shows messages for each action
2. Each tab has descriptive labels
3. Tool tips on buttons describe their function
4. Output windows show execution details

### Documentation Resources

- **Quick questions**: See QUICK_START.md
- **How-to guide**: See USER_GUIDE.md
- **API reference**: See CODE_DOCUMENTATION.md
- **Examples**: See sap_scripts directory

### Troubleshooting

1. Check error messages in output window
2. Read the troubleshooting sections in USER_GUIDE.md
3. Verify SAP GUI connection in Session Manager tab
4. Review example scripts for similar operations

## System Performance

### During Usage

- Application uses 200-300MB memory
- Script execution runs in separate thread (no freezing)
- File operations are fast (< 1 second)
- SAP interaction speed depends on SAP system response time

### Optimization Tips

- Close unused SAP sessions
- Run scripts during off-peak times
- Add pause times between SAP actions
- Monitor system resources if processing large batches

## Security Considerations

- Scripts run with your SAP user permissions
- Sensitive data (passwords) should use configuration files
- Script files should be version-controlled
- Restrict access to scripts directory
- Audit script execution in logs

## Support

If you encounter issues:

1. Verify all prerequisites are installed
2. Check error messages carefully
3. Review USER_GUIDE.md troubleshooting section
4. Test with example scripts first
5. Verify SAP GUI connectivity

## Success Indicators

You know installation is successful when:

✅ Application window opens without errors
✅ Session Manager can "Refresh Sessions"
✅ Script Editor can create and edit scripts
✅ Script Executor can run test scripts
✅ Settings can be saved and loaded

All five items confirmed means successful installation!

## Conclusion

The application is now installed and ready to use. You can:

- Create Python scripts for SAP automation
- Record SAP transactions
- Execute scripts on demand
- Manage multiple SAP sessions
- Track script execution
- Configure application settings

Begin with QUICK_START.md for a 5-minute introduction, then explore USER_GUIDE.md for complete documentation.

Happy automating!

---

**Installation Complete** ✓

Next: Read QUICK_START.md to begin using the application.
