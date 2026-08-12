# SAP Script Manager - Project Structure

## Organization Overview

The project is organized into thematic directories for easy navigation and maintenance:

```
SAP-scripting/
│
├── app/                           ← Main Application
│   ├── sap_gui_manager.py         (Graphical Interface)
│   ├── SAP.py                     (Automation Library)
│   └── run_sap_manager.bat        (Launcher - execute this file)
│
├── docs/                          ← Complete Documentation
│   ├── README.md                  (Start - read first!)
│   ├── QUICK_START.md             (5-minute Guide)
│   ├── INSTALLATION_GUIDE.md      (Step-by-step Installation)
│   ├── USER_GUIDE.md              (Complete Manual)
│   ├── CODE_DOCUMENTATION.md      (Technical Reference)
│   ├── EVALUATION_AND_PYTHON_PORT.md (Design Analysis)
│   ├── PROJECT_DELIVERY_SUMMARY.md   (What Was Delivered)
│   └── DOCUMENTATION_INDEX.md     (Documentation Index)
│
├── examples/                      ← Example Scripts
│   ├── example_automation.py      (Basic Automation Patterns)
│   └── batch_processing_example.py (Batch Processing)
│
├── config/                        ← Configuration
│   └── requirements.txt           (Python Dependencies)
│
├── sap_scripts/                   ← Your Scripts (User Area)
│   └── (Your .py files here)
│
├── README.md                      ← Quick Guide (root)
├── SAP.au3                        ← Original AutoIt3 Code (reference)
├── .gitignore                     ← Git Configuration
└── PROJECT_STRUCTURE.md           ← This file
```

## Directory Descriptions

### /app
**Contains:** Application source code

- **sap_gui_manager.py** - Main application with PyQt5 interface
  - Manages main window
  - Implements 5 tabs (Session Manager, Script Editor, Recorder, Executor, Settings)
  - 1800+ lines of documented code

- **SAP.py** - SAP automation library
  - 15 core functions to control SAP GUI
  - COM interface with pywin32
  - 600+ lines of code with type hints

- **run_sap_manager.bat** - Executable launcher
  - Execute this file with double-click to start
  - Detects Python automatically
  - Validates dependencies

### /docs
**Contains:** Complete documentation for all audiences

| File | For Whom | Time |
|------|----------|------|
| QUICK_START.md | Beginners - start here! | 5 min |
| INSTALLATION_GUIDE.md | Step-by-step installation | 15 min |
| USER_GUIDE.md | End users | 30 min |
| CODE_DOCUMENTATION.md | Developers | 45 min |
| EVALUATION_AND_PYTHON_PORT.md | Architects | 20 min |
| DOCUMENTATION_INDEX.md | Documentation navigation | 5 min |
| PROJECT_DELIVERY_SUMMARY.md | Project overview | 15 min |

**Total:** 4200+ lines of professional documentation

### /examples
**Contains:** Commented example scripts

- **example_automation.py** (200 lines)
  - Connect to SAP
  - Navigate to transaction
  - Fill forms
  - Submit data
  - Error handling

- **batch_processing_example.py** (250 lines)
  - Multiple record processing
  - Class-based structure
  - Results tracking
  - Summary reports

Copy and adapt these examples for your scripts!

### /config
**Contains:** Configuration files

- **requirements.txt**
  - Required Python dependencies
  - PyQt5 >= 5.15.0
  - pywin32 >= 300

Install with: `pip install -r config/requirements.txt`

### /sap_scripts
**Contains:** Your scripts (user area)

- This directory is for YOUR Python scripts
- Application creates/saves scripts here by default
- .gitignore ignores your scripts (privacy)
- Synchronize with version control when desired

## How to Use This Structure

### To Get Started

1. **Read:** `docs/QUICK_START.md` (5 minutes)
2. **Install:** Follow `docs/INSTALLATION_GUIDE.md`
3. **Execute:** Double-click `app/run_sap_manager.bat`
4. **Consult:** `docs/USER_GUIDE.md` as needed

### To Develop

1. **Study:** `docs/CODE_DOCUMENTATION.md`
2. **Examine:** Source code in `/app`
3. **Copy:** Examples from `/examples`
4. **Create:** Your scripts in `/sap_scripts`

### To Extend

1. **Understand:** `docs/EVALUATION_AND_PYTHON_PORT.md`
2. **Modify:** Code in `/app` (carefully!)
3. **Test:** With examples in `/examples`

## Import Structure

Files expect the following structure:

```python
# In sap_gui_manager.py (in app/)
import SAP  # Imports app/SAP.py from same directory

# In your scripts (in sap_scripts/)
import sys
sys.path.insert(0, '../app')  # Adds app/ to path
import SAP
```

The `run_sap_manager.bat` file configures PYTHONPATH automatically.

## Root Files

### README.md
- Quick reference guide
- Doesn't duplicate docs/ (which has complete version)
- Useful for Git repository

### SAP.au3
- Original AutoIt3 code
- Kept for historical reference
- Not necessary for operation

### .gitignore
- Git configuration
- Ignores Python cache (__pycache__)
- Ignores your scripts (privacy)
- Ignores settings.json (local configuration)

## Conventions

### File Naming
- Python: `snake_case.py`
- Markdown: `UPPER_CASE.md`
- Batch: `snake_case.bat`

### Code Organization
- One class per file when possible
- Functions grouped by type
- Docstrings in English
- Type hints on all functions

### Documentation
- Markdown for all docs
- Titles with #, ##, ###
- Code in \``` blocks
- Examples with line numbers

## Maintenance

### Adding New Example
1. Create file in `/examples`
2. Add descriptive comments
3. Document usage in `docs/DOCUMENTATION_INDEX.md`

### Updating Documentation
1. Edit file in `/docs`
2. Maintain consistent format
3. Update index if necessary

### Changing Source Code
1. Modify file in `/app`
2. Update docstrings
3. Consider impact on docs/

### Adding Dependency
1. Add to `config/requirements.txt`
2. Update `docs/INSTALLATION_GUIDE.md`
3. Test clean installation

## Next Steps

1. **Navigate:** Explore the directories
2. **Read:** Start at `docs/QUICK_START.md`
3. **Execute:** Run `app/run_sap_manager.bat`
4. **Learn:** Use `docs/USER_GUIDE.md`
5. **Create:** Your scripts in `sap_scripts/`

## Support

- **Quick Help:** See `docs/QUICK_START.md`
- **Complete Instructions:** Consult `docs/USER_GUIDE.md`
- **Technical Reference:** Study `docs/CODE_DOCUMENTATION.md`
- **Troubleshooting:** Look in docs (section "Troubleshooting")

---

**Professional Structure** ✓
**Production Ready** ✓
**Well Documented** ✓

Start with `docs/QUICK_START.md`!
