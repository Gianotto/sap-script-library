# SAP Script Manager - Professional SAP Automation GUI

A comprehensive Python application for managing, creating, executing, and recording SAP automation scripts. The application provides an intuitive graphical interface for automating SAP transactions and processes.

## 📁 Project Organization

This project is organized in a clear, professional structure:

```
SAP-scripting/
├── app/              ← Código da aplicação (execute run_sap_manager.bat)
├── docs/             ← Documentação completa
├── examples/         ← Scripts de exemplo comentados
├── config/           ← Dependências (requirements.txt)
├── sap_scripts/      ← Seus scripts aqui
└── PROJECT_STRUCTURE.md  ← Explicação da estrutura
```

**Start here:** See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for complete directory guide.

## Features

### Core Capabilities

- **Session Management**: Connect to, create, and manage multiple SAP GUI sessions
- **Script Editor**: Full-featured Python editor with syntax highlighting
- **Transaction Recorder**: Record SAP user interactions and generate scripts automatically
- **Script Executor**: Execute scripts with real-time output monitoring
- **Error Handling**: Comprehensive error reporting and debugging information
- **Settings Management**: Configure application preferences and defaults

### What You Can Automate

- Navigate to any SAP transaction
- Fill form fields with values
- Click buttons and select menu options
- Read data from SAP screens
- Wait for specific windows or responses
- Perform repetitive processes at scale
- Create reusable automation scripts
- Chain multiple transactions together
- Process batches of data

## System Requirements

### Software

- **Windows Operating System**: XP or later
- **Python**: 3.6 or higher
- **SAP GUI**: Release 6.40 or later
- **SAP System Access**: Active user account with appropriate permissions

### Hardware

- Minimum: 2GB RAM, dual-core processor
- Recommended: 4GB RAM, quad-core processor
- Storage: 500MB for application and scripts

## Installation

### Quick Install

```powershell
# Clone or download the project
cd SAP-scripting

# Install Python dependencies
pip install -r requirements.txt

# Configure pywin32
python -m pip install --upgrade pywin32
python -c "import site; print(site.getsitepackages()[0])" # Get site-packages path
python path\to\site-packages\pywin32_postinstall.py -install
```

### Detailed Installation

For step-by-step instructions, see QUICK_START.md.

## SAP Configuration

Before using the application, enable scripting in SAP GUI:

1. Open SAP GUI and log into any system
2. Click "Customize Local Layout" (toolbar icon)
3. Select "Options"
4. Go to "Scripting" tab
5. Verify message shows "Scripting is installed!"
6. Check "Enable Scripting" checkbox
7. Uncheck notification options if preferred
8. Click OK

This is a one-time configuration per SAP GUI installation.

## Quick Start

### Launch the Application

```powershell
python sap_gui_manager.py
```

### Create Your First Script

1. Click "Session Manager" tab → "Refresh Sessions"
2. Select a session → "Connect to Session"
3. Click "Script Editor" tab → "New Script"
4. Name it "HelloSAP"
5. Click "Run Script"

Your first automation runs successfully.

For a complete walkthrough, see QUICK_START.md.

## Application Tabs

### Session Manager

Connect and manage SAP sessions:

- **Refresh Sessions**: List available SAP sessions
- **Connect to Session**: Attach to specific session
- **Create New Session**: Open new SAP session
- **View Details**: See session information

### Script Editor

Create and edit Python automation scripts:

- **New Script**: Start script from template
- **Open Script**: Load existing script
- **Save Script**: Persist script to file
- **Run Script**: Execute directly
- **Syntax Highlighting**: Color-coded Python code

### Transaction Recorder

Record SAP interactions and generate scripts:

- **Start Recording**: Begin capturing actions
- **Add Action**: Manually record steps
- **Generate Script**: Create executable code
- **View Actions**: See recorded steps

Automatically converts your SAP steps into runnable Python code.

### Script Executor

Execute scripts and monitor results:

- **Select Script**: Browse to script file
- **Execute Script**: Run script in separate thread
- **View Output**: Real-time execution output
- **Clear Output**: Reset display

Executes without freezing the UI.

### Settings

Configure application behavior:

- **Scripts Directory**: Where to save/load scripts
- **Connection Timeout**: Max wait for SAP response
- **Auto-save**: Automatic script saving
- **Save Settings**: Persist preferences

## Core Automation Functions

All scripts use functions from the SAP module:

### Session Control

```python
SAP.sap_sess_attach("SAP Easy Access")      # Connect to session
SAP.sap_sess_create("ZMY_TRANS")            # Create new session
```

### Object Interaction

```python
SAP.sap_obj_value_set("usr/ctxt[0]", "DATA")  # Set field value
value = SAP.sap_obj_value_get("usr/ctxt[0]")  # Read field value
SAP.sap_obj_select("usr/btn[0]")               # Click button
SAP.sap_obj_deselect("usr/chk[0]")             # Uncheck checkbox
```

### Property Access

```python
SAP.sap_obj_property_set(id, "text", "value")   # Set property
result = SAP.sap_obj_property_get(id, "text")   # Read property
```

### Input Simulation

```python
SAP.sap_vkeys_send("Enter")                 # Send virtual key
SAP.sap_vkeys_send_until_win_exists("Enter", "Program List")  # Wait for window
```

### Window Operations

```python
exists = SAP.sap_win_exists("Program Output")   # Check window exists
SAP.sap_win_close("Program Output")             # Close window
```

## Script Examples

### Navigate to Transaction

```python
import SAP

SAP.sap_sess_attach("SAP Easy Access")
SAP.sap_obj_value_set("usr/ctxt[0]", "SE38")
SAP.sap_vkeys_send("Enter")
print("Navigated to SE38 transaction")
```

### Fill Form and Submit

```python
import SAP

SAP.sap_sess_attach("SAP Easy Access")

# Fill first field
SAP.sap_obj_value_set("usr/ctxt[0]", "MyProgram")

# Fill second field
SAP.sap_obj_value_set("usr/ctxt[1]", "Production")

# Click Execute button
SAP.sap_obj_select("usr/btn[0]")

print("Form submitted successfully")
```

### Process Multiple Records

```python
import SAP

records = ["Record001", "Record002", "Record003"]

SAP.sap_sess_attach("SAP Easy Access")

for record in records:
    SAP.sap_obj_value_set("usr/ctxt[0]", record)
    SAP.sap_obj_select("usr/btn[0]")
    print(f"Processed: {record}")

print("All records processed")
```

### Error Handling

```python
import SAP

try:
    SAP.sap_sess_attach("SAP Easy Access")
    SAP.sap_obj_value_set("usr/ctxt[0]", "InvalidData")
    
except SAP.SAPException as e:
    print(f"SAP Error: {e.message} (Code: {e.error_code})")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

## Documentation

Comprehensive documentation is provided:

### For Users

- **QUICK_START.md**: Get running in 5 minutes
- **USER_GUIDE.md**: Complete usage instructions
- **QUICK_START.md**: Common tasks and examples

### For Developers

- **CODE_DOCUMENTATION.md**: Detailed API documentation
- **EVALUATION_AND_PYTHON_PORT.md**: Architecture and design
- Inline code comments throughout

## File Structure

```
SAP-scripting/
├── sap_gui_manager.py               Main application (1800+ lines)
├── SAP.py                           Automation library (600+ lines)
├── requirements.txt                 Python dependencies
├── sap_manager_settings.json        Application settings
│
├── README.md                        This file (project overview)
├── QUICK_START.md                   5-minute setup guide
├── USER_GUIDE.md                    Complete usage documentation
├── CODE_DOCUMENTATION.md            API and component documentation
├── EVALUATION_AND_PYTHON_PORT.md    Architecture and design notes
│
└── sap_scripts/                     Scripts directory
    ├── example_script.py            Sample automation
    ├── recorded_script.py           Generated from recording
    └── (your scripts)               Your automation scripts
```

## Architecture

The application uses a modular design:

```
User Interface (PyQt5)
    ↓
Components (SessionManager, ScriptEditor, etc.)
    ↓
Automation Library (SAP.py)
    ↓
Windows COM Interface (pywin32)
    ↓
SAP GUI Scripting
    ↓
SAP ERP System
```

Each component has clear responsibilities:

- **PythonSyntaxHighlighter**: Code highlighting
- **SessionManager**: SAP session lifecycle
- **ScriptEditor**: File operations
- **TransactionRecorder**: Action recording
- **ScriptExecutor**: Script execution in thread
- **SAPScriptManagerApp**: Main UI coordination

## Performance Characteristics

- **Startup Time**: 2-3 seconds
- **Script Execution**: Variable (dependent on SAP response times)
- **UI Response**: Immediate (scripts run in separate thread)
- **Memory Usage**: 200-300MB typical
- **Maximum Sessions**: Unlimited (limited by SAP system)

## Known Limitations

- Windows-only (SAP GUI Scripting requires Windows)
- Requires SAP GUI 6.40 or later
- Scripts cannot access web-based transactions
- Limited to GUI automation (no backend functions)
- Recording requires manual action entry (not mouse tracking)

## Troubleshooting

### Installation Issues

**PyQt5 installation fails**
- Ensure Python 3.6 or higher
- Try: `pip install PyQt5 --upgrade`

**pywin32 configuration fails**
- Run as Administrator
- Verify Python installation path
- Reinstall: `pip uninstall pywin32; pip install pywin32`

### Runtime Issues

**"Unable to find an active SAP session"**
- Open SAP GUI
- Log into any system
- Verify scripting is enabled
- Refresh sessions in application

**"Object not found" errors**
- Verify object_id using SAP Scripting Wizard
- Check window index (usually [0])
- Wait longer for screens to load
- Verify correct SAP transaction

**Scripts freeze or hang**
- Increase connection timeout in Settings
- Add explicit wait times with time.sleep()
- Check if SAP is unresponsive
- Verify object IDs are correct

### SAP Configuration

**"Scripting is not installed" message**
- Install SAP GUI scripting support
- Contact SAP system administrator
- Restart SAP GUI after installation
- Verify with "Customize Local Layout"

## Development

### Adding New Features

1. Add methods to relevant component class
2. Create UI elements in tab creation method
3. Connect signals to handlers
4. Test with sample data
5. Document in code comments

### Extending Functionality

The application can be extended for:

- Additional automation libraries
- Different ERP systems
- Custom UI layouts
- Advanced scheduling
- Database integration
- API endpoints

### Testing

Create test scripts in `sap_scripts/tests/`:

```python
# test_basic_automation.py
import SAP

def test_session_attach():
    try:
        result = SAP.sap_sess_attach("SAP Easy Access")
        assert result == True
        print("Test passed: Session attachment")
    except Exception as e:
        print(f"Test failed: {str(e)}")
```

Run with: `python test_basic_automation.py`

## Best Practices

### Script Development

- Start with simple scripts
- Test each function independently
- Use meaningful variable names
- Add comments for complex logic
- Handle exceptions properly
- Log important steps

### Performance

- Use shortest effective pause times
- Minimize unnecessary waits
- Reuse sessions when possible
- Close unused windows
- Process data efficiently

### Reliability

- Use absolute object identifiers
- Verify window existence before access
- Implement retry logic for transient errors
- Test in development first
- Monitor execution output

### Maintenance

- Keep scripts version controlled
- Document automation purpose
- Update scripts when SAP changes
- Archive old scripts
- Schedule regular testing

## Security Considerations

- Scripts can read/write data in SAP
- Store sensitive data securely (not in scripts)
- Use configuration files for credentials
- Restrict file access to authorized users
- Monitor script execution
- Audit all automated changes

Example secure configuration:

```python
import json

with open("secure_config.json") as f:
    config = json.load(f)

SAP.sap_sess_attach(config["sap_user"])
```

## Support and Resources

### Documentation

- Full documentation in repository
- Inline code comments throughout
- Examples in QUICK_START.md
- API reference in CODE_DOCUMENTATION.md

### Community

- Share scripts with team members
- Document lessons learned
- Maintain script library
- Provide feedback on features

### SAP Resources

- SAP Scripting Wizard (in SAP GUI)
- SAP GUI documentation
- SAP Developer Network (SDN)
- SAP consulting partners

## Version Information

**Application Version**: 1.0
**SAP Module Version**: 1.0 (Based on AutoIt3 v0.4 port)
**Python Version**: 3.6+
**PyQt5 Version**: 5.15.0+
**pywin32 Version**: 300+

## License and Attribution

SAP Scripting GUI Manager
- Original AutoIt3 library by seangriffin (2009)
- Python port and GUI application (2024)

## Changelog

### Version 1.0 (2024)

- Complete GUI application for SAP automation
- Session manager for multi-session support
- Python script editor with syntax highlighting
- Transaction recorder for action recording
- Script executor with real-time monitoring
- Settings management and persistence
- Comprehensive documentation and examples
- Full source code with extensive comments

## Future Roadmap

Planned enhancements:

- Web-based interface for remote access
- Advanced scheduling and job management
- Integration with workflow systems
- Database integration for data mapping
- Enhanced transaction recording with mouse tracking
- Multi-language support
- Plugin architecture for extensibility
- Cloud deployment options

## Getting Help

1. Check QUICK_START.md for immediate answers
2. Review USER_GUIDE.md for detailed instructions
3. Search CODE_DOCUMENTATION.md for API details
4. Test with simpler scripts
5. Verify SAP configuration
6. Consult SAP Scripting Wizard in SAP GUI

## Contributing

Contributions are welcome:

- Report bugs with reproduction steps
- Suggest features with use cases
- Share scripts and examples
- Improve documentation
- Provide feedback on usability

## Conclusion

SAP Script Manager provides a powerful, user-friendly platform for automating SAP processes. Whether you need simple transaction automation or complex multi-step workflows, this tool simplifies development and execution.

Start with the Quick Start guide, explore the interface, create your first script, and build towards your automation goals.

Happy automating!

---

**For complete usage instructions, see USER_GUIDE.md**

**For API documentation, see CODE_DOCUMENTATION.md**

**For quick start, see QUICK_START.md**
