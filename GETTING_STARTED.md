# Getting Started - SAP Script Manager

Welcome to SAP Script Manager! This guide helps you get started in 5 minutes.

## 📂 Project Structure

```
SAP-scripting/
├── app/              ← 🚀 Execute here (run_sap_manager.bat)
├── docs/             ← 📖 Read documentation here
├── examples/         ← 💡 Copy examples from here
├── sap_scripts/      ← 💾 Your scripts save here
└── config/           ← ⚙️ Configuration here
```

## ⚡ Quick Start (5 minutes)

### 1. Start Application
```bash
# Option A: Double-click
app/run_sap_manager.bat

# Option B: PowerShell
.\run.ps1

# Option C: Direct Python
python app/sap_gui_manager.py
```

### 2. Connect to SAP
1. Click **"Session Manager"** tab
2. Click **"Refresh Sessions"**
3. Select a SAP session
4. Click **"Connect"**

### 3. Create a Script
1. Click **"Script Editor"** tab
2. Click **"New Script"**
3. Enter a name: `MyScript`
4. Paste code:
```python
import SAP

try:
    SAP.sap_sess_attach("SAP Easy Access")
    print("✅ Connected to SAP!")
except Exception as e:
    print(f"❌ Error: {e}")
```

5. Click **"Run Script"**
6. See result in **"Script Executor"** tab

## 📖 Documentation

### For Beginners
- 📋 [QUICK_START.md](docs/QUICK_START.md) - 5 minutes
- 🚀 [USER_GUIDE.md](docs/USER_GUIDE.md) - Complete guide

### For Installation
- 📦 [INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) - Step by step

### For Development
- 💻 [CODE_DOCUMENTATION.md](docs/CODE_DOCUMENTATION.md) - API reference
- 🏗️ [EVALUATION_AND_PYTHON_PORT.md](docs/EVALUATION_AND_PYTHON_PORT.md) - Design

### Indexes
- 🗺️ [DOCUMENTATION_INDEX.md](docs/DOCUMENTATION_INDEX.md) - Navigate docs
- 📊 [PROJECT_DELIVERY_SUMMARY.md](docs/PROJECT_DELIVERY_SUMMARY.md) - Deliverables

## 💡 Examples

Copy examples from `/examples`:

### Basic Automation
```bash
# See:
examples/example_automation.py
```

### Batch Processing
```bash
# See:
examples/batch_processing_example.py
```

## 📝 Create Your Scripts

Your scripts save in: **`sap_scripts/`**

```python
# sap_scripts/my_script.py

import sys
sys.path.insert(0, '../app')
import SAP

# Your code here
SAP.sap_sess_attach("SAP Easy Access")
# ... automation ...
```

## ✅ Setup Checklist

- [ ] Python 3.6+ installed
- [ ] PyQt5 and pywin32 installed (`pip install -r config/requirements.txt`)
- [ ] pywin32 configured (`python -m Scripts.pywin32_postinstall -install`)
- [ ] SAP GUI Scripting enabled
- [ ] Tested Session Manager (Connect button)
- [ ] Created first script

All items checked? You're ready!

## 🎯 Common Workflow

### Approach 1: Manual
1. Session Manager: Connect
2. Script Editor: Write code
3. Script Executor: Execute
4. See result

### Approach 2: Recording
1. Transaction Recorder: Start recording
2. Perform actions in SAP (Ctrl+Alt to capture clicks)
3. Transaction Recorder: Stop recording
4. Generates Python script automatically
5. Edit and refine in Script Editor
6. Execute when ready

### Approach 3: Examples
1. Copy from `/examples`
2. Adapt to your needs
3. Test in Script Editor
4. Execute when it works

## 🛠️ Troubleshooting

### "Python not found"
```bash
# Install from: https://www.python.org
# Check: "Add Python to PATH" during installation
# Restart the script launcher
```

### "SAP not found"
```bash
# 1. Open SAP GUI
# 2. Customize Local Layout → Options → Scripting
# 3. Check "Enable Scripting"
# 4. Try again
```

### "SAP module not found"
```bash
# Add to your script:
import sys
sys.path.insert(0, '../app')
import SAP
```

### "pywin32 doesn't work"
```powershell
# Run as admin:
python -m Scripts.pywin32_postinstall -install

# Or directly:
pip install --upgrade pywin32
```

## 📞 More Help

- **Documentation:** See `docs/` for complete guides
- **Examples:** Study code in `examples/`
- **Troubleshooting:** See "Troubleshooting" section in each guide

## 🚀 Next Steps

1. ✅ Setup everything
2. 📖 Read [docs/QUICK_START.md](docs/QUICK_START.md)
3. 💻 Create your first script in Script Editor
4. 🎯 Automate your first SAP process
5. 📚 Learn more features in [docs/USER_GUIDE.md](docs/USER_GUIDE.md)

---

**Structure Ready** ✓
**Complete Documentation** ✓
**Examples Provided** ✓

Happy automation!

