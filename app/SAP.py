"""
SAP Automation UDF Library for Python
File: SAP.py
Description: A collection of functions for creating, attaching to, reading from and manipulating SAP
Author: Python Port (Original: seangriffin for AutoIt3)
Version: 1.0
Based on AutoIt3 Version: V0.4
Last Update: 2024

Requirements:
    - Python 3.6+
    - pywin32 (pip install pywin32)
    - SAP GUI Release 6.40+
    - SAP GUI Scripting interface enabled
      (From the SAP GUI, select "Customize Local Layout" button on toolbar,
       then "Options". Go to "Scripting" tab. The message "Scripting is installed!" 
       MUST BE DISPLAYED. Select "Enable Scripting", and deselect 
       "Notify when a script attaches to a running GUI" and
       "Notify when a script opens a connection")

Changelog:
    v1.0 - Initial Python port with all core functionality
"""

import re
import time
import win32com.client as win32com
from typing import Union, List, Dict, Optional, Tuple, Any
import sys

# Global Constants
SAP_VKEY = [
    "Enter", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",
    "F11", "F12",
    "Shift+F1", "Shift+F2", "Shift+F3", "Shift+F4", "Shift+F5", "Shift+F6",
    "Shift+F7", "Shift+F8", "Shift+F9",
    "Shift+Ctrl+0", "Shift+F11", "Shift+F12",
    "Ctrl+F1", "Ctrl+F2", "Ctrl+F3", "Ctrl+F4", "Ctrl+F5", "Ctrl+F6",
    "Ctrl+F7", "Ctrl+F8", "Ctrl+F9", "Ctrl+F10",
    "Ctrl+F11", "Ctrl+F12",
    "Ctrl+Shift+F1", "Ctrl+Shift+F2", "Ctrl+Shift+F3", "Ctrl+Shift+F4",
    "Ctrl+Shift+F5", "Ctrl+Shift+F6", "Ctrl+Shift+F7", "Ctrl+Shift+F8",
    "Ctrl+Shift+F9", "Ctrl+Shift+F10", "Ctrl+Shift+F11", "Ctrl+Shift+F12",
    "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
    "", "", "", "", "",
    "Ctrl+E", "Ctrl+F", "Ctrl+A", "Ctrl+D", "Ctrl+N", "Ctrl+O", "Shift+D",
    "Ctrl+I", "Shift+I", "Alt+B",
    "Ctrl+Page up", "Page up", "Page down", "Ctrl+Page down", "Ctrl+G",
    "Ctrl+R", "Ctrl+P",
    "", "", "", "", "", "", "", "Shift+F10", "", "", "", "", ""
]

# Global Variables
sap_connection = None
sap_session = None
sap_window_num = None
sap_object_id = None
sap_object_value = None
sap_error_notify = True
sap_error_handler = None
sap_user_error_handler = None


class SAPException(Exception):
    """Custom exception for SAP automation errors"""
    def __init__(self, error_code: int, message: str):
        self.error_code = error_code
        self.message = message
        super().__init__(f"SAP Error {error_code}: {message}")


def sap_sess_attach(win_title: str = "SAP Easy Access", sap_transaction: str = None) -> bool:
    """
    Attaches to an existing session of SAP.
    
    Args:
        win_title: The title of the SAP window (within the session) to attach to.
                   "SAP Easy Access" is used if not provided.
                   May be a substring of the full window title.
        sap_transaction: Optional SAP transaction to run after attaching.
                        A "/n" will be inserted at the beginning if not provided.
    
    Returns:
        True on success, False on failure
        
    Raises:
        SAPException: If unable to find an active SAP session or window
    """
    global sap_connection, sap_session, sap_window_num
    
    if sap_connection is None:
        try:
            sapgui = win32com.GetObject("SAPGUI")
            sapapp = sapgui.GetScriptingEngine
        except Exception as e:
            raise SAPException(1, f"Unable to find an active SAP session. Make sure you are logged into SAP "
                                 f"and have GUI Scripting enabled. Error: {str(e)}")
        
        if sapapp.Children.Count == 0:
            raise SAPException(1, "Unable to find an active SAP session. Make sure you are logged into SAP "
                                 "and have GUI Scripting enabled.")
        
        sap_connection = sapapp.Children(0)
    
    # Wait 20 seconds for the window to exist
    win_wait_start = time.time()
    while not sap_win_exists(win_title):
        if time.time() - win_wait_start > 20:
            raise SAPException(2, f"Unable to find the window with title '{win_title}' to attach to.")
        time.sleep(0.1)
    
    # Check each session for the window title
    for sap_sess_num in range(sap_connection.Sessions.Count):
        sap_session = sap_connection.Children(sap_sess_num)
        
        # Check each window in each session for the window title
        for sap_window_num_tmp in range(sap_session.Children.Count):
            window_text = sap_session.findById(f"wnd[{sap_window_num_tmp}]").Text
            if re.search(f".*{re.escape(win_title)}.*", window_text):
                sap_window_num = sap_window_num_tmp
                
                if sap_transaction is not None:
                    if not sap_transaction.startswith("/n"):
                        sap_transaction = "/n" + sap_transaction
                    
                    sap_session.findById("wnd[0]/tbar[0]/okcd").Text = sap_transaction
                    sap_session.findById("wnd[0]").sendVKey(0)
                
                return True
    
    return False


def sap_sess_create(sap_transaction: str = None) -> bool:
    """
    Creates a new session in SAP.
    
    Args:
        sap_transaction: Optional SAP transaction to run in the new session
    
    Returns:
        True on success, False on failure
    """
    global sap_connection, sap_session
    
    if sap_connection is None or sap_session is None:
        raise SAPException(1, "Session not attached. Call sap_sess_attach() first.")
    
    num_sess_old = sap_connection.Sessions.Count
    sap_session.CreateSession
    
    # Wait for new session to be created
    timeout = time.time() + 10
    while sap_connection.Sessions.Count == num_sess_old:
        if time.time() > timeout:
            raise SAPException(1, "Timeout while creating new session")
        time.sleep(0.1)
    
    sap_session = sap_connection.Children(sap_connection.Sessions.Count - 1)
    sap_session.findById("wnd[0]").maximize
    
    if sap_transaction is not None:
        sap_session.findById("wnd[0]/tbar[0]/okcd").Text = sap_transaction
        sap_session.findById("wnd[0]").sendVKey(0)
    
    return True


def sap_vkeys_send(vkeys: str) -> bool:
    """
    Sends virtual keys to the currently attached session of SAP.
    
    Args:
        vkeys: A comma-separated sequence of virtual keys to send.
               See SAP_VKEY array for available keys.
    
    Returns:
        True on success, False on failure
    """
    global sap_session, sap_window_num
    
    if sap_session is None or sap_window_num is None:
        raise SAPException(1, "Session not attached. Call sap_sess_attach() first.")
    
    vkey_list = [v.strip() for v in vkeys.split(",")]
    
    for i, vkey in enumerate(vkey_list):
        if i == 0:  # Skip first empty element from split
            continue
        
        try:
            vkey_id = SAP_VKEY.index(vkey)
            sap_session.findById(f"wnd[{sap_window_num}]").sendVKey(vkey_id)
        except ValueError:
            raise SAPException(1, f"Invalid virtual key: {vkey}")
    
    return True


def sap_vkeys_send_until_win_exists(keys: str, win_title: str) -> bool:
    """
    Sends virtual keys to the currently attached session of SAP until a window exists.
    
    Args:
        keys: The sequence of keys to repeatedly send
        win_title: The title of the SAP window to wait for
    
    Returns:
        True on success, False on failure
    """
    timeout = time.time() + 60
    while not sap_win_exists(win_title):
        if time.time() > timeout:
            return False
        sap_vkeys_send(keys)
        time.sleep(0.1)
    
    return True


def sap_obj_select(object_id: str) -> bool:
    """
    Selects an object within the currently attached session of SAP.
    
    Args:
        object_id: The short ID of the object to select
    
    Returns:
        True on success, False on failure
    """
    global sap_session, sap_window_num, sap_object_id
    
    if sap_session is None or sap_window_num is None:
        raise SAPException(1, "Session not attached. Call sap_sess_attach() first.")
    
    sap_object_id = object_id
    full_id = f"wnd[{sap_window_num}]/{object_id}"
    obj = sap_session.findById(full_id)
    
    # GuiButton
    if "/btn" in object_id:
        obj.press()
    # GuiRadioButton
    elif "/rad" in object_id:
        obj.select()
    # GuiCheckBox
    elif "/chk" in object_id:
        obj.selected = True
    # GuiMenubar
    elif "mbar/" in object_id:
        obj.select()
    # GuiLabel
    elif "/lbl" in object_id:
        # If the GuiLabel is not an expanded twistie, select it
        if str(obj.text) != "5":
            obj.setFocus()
            obj.caretPosition = 1
            sap_vkeys_send("F2")
    
    return True


def sap_obj_deselect(object_id: str) -> bool:
    """
    Deselects an object within the currently attached session of SAP.
    
    Args:
        object_id: The short ID of the object to deselect
    
    Returns:
        True on success, False on failure
    """
    global sap_session, sap_window_num, sap_object_id
    
    if sap_session is None or sap_window_num is None:
        raise SAPException(1, "Session not attached. Call sap_sess_attach() first.")
    
    sap_object_id = object_id
    full_id = f"wnd[{sap_window_num}]/{object_id}"
    obj = sap_session.findById(full_id)
    
    # GuiCheckBox or GuiRadioButton
    if "/rad" in object_id or "/chk" in object_id:
        obj.selected = False
    # GuiLabel
    elif "/lbl" in object_id:
        # If the GuiLabel is not a collapsed twistie, deselect it
        if str(obj.text) != "4":
            obj.setFocus()
            obj.caretPosition = 1
            sap_vkeys_send("F2")
    
    return True


def sap_obj_value_set(object_id: str, object_value: str) -> bool:
    """
    Sets the value of an object within the currently attached session of SAP.
    
    Args:
        object_id: The short ID of the object
        object_value: The value to set
    
    Returns:
        True on success, False on failure
    """
    global sap_session, sap_window_num, sap_object_id, sap_object_value
    
    if sap_session is None or sap_window_num is None:
        raise SAPException(1, "Session not attached. Call sap_sess_attach() first.")
    
    sap_object_id = object_id
    sap_object_value = object_value
    full_id = f"wnd[{sap_window_num}]/{object_id}"
    obj = sap_session.findById(full_id)
    
    # GuiComboBox - set key property
    if "/cmb" in object_id:
        obj.key = object_value
    # All other objects - set text property
    elif "/chk" in object_id or "/ctxt" in object_id or \
         "/okcd" in object_id or "/pwd" in object_id or "/txt" in object_id:
        obj.text = object_value
    
    return True


def sap_obj_value_get(object_id: str = "usr") -> Union[str, List[List[str]], int]:
    """
    Get the value of an object within the currently attached session of SAP.
    
    Args:
        object_id: The short ID of the object to get the value of.
                   GuiUserArea ("usr") is used if not provided.
    
    Returns:
        The value/text of the object (string for most objects, 2D array for GuiUserArea)
        Returns 0 on failure
    """
    global sap_session, sap_window_num, sap_object_id
    
    if sap_session is None or sap_window_num is None:
        raise SAPException(1, "Session not attached. Call sap_sess_attach() first.")
    
    sap_object_id = object_id
    full_id = f"wnd[{sap_window_num}]/{object_id}"
    obj = sap_session.findById(full_id)
    
    # GuiComboBox - get key property
    if "/cmb" in object_id:
        return obj.key
    # GuiUserArea - get children
    elif object_id == "usr":
        object_children = obj.Children
        
        # Get character extents
        max_charleft = 0
        max_chartop = 0
        
        for child in object_children:
            if child.CharLeft > max_charleft:
                max_charleft = child.CharLeft
            if child.CharTop > max_chartop:
                max_chartop = child.CharTop
        
        # Create output array
        child_text = [[None for _ in range(max_charleft + 1)] for _ in range(max_chartop + 1)]
        
        # Populate array
        for child in object_children:
            child_text[child.CharTop][child.CharLeft] = child.Text
        
        return child_text
    # All other objects - get text property
    elif "/btn" in object_id or "/chk" in object_id or "/ctxt" in object_id or \
         "/lbl" in object_id or "/okcd" in object_id or "/pwd" in object_id or \
         "/rad" in object_id or "/sbar" in object_id or "/txt" in object_id:
        return obj.text
    
    return 0


def sap_obj_find_by_value(object_id: str = "usr", object_value: str = "", 
                         match_type: int = 0, instance: int = 1, 
                         object_offset: int = 0) -> Union[str, int]:
    """
    Find a SAP object based on its value.
    
    Args:
        object_id: The short ID of the object to search within (default: "usr")
        object_value: The value of the object to find
        match_type: 0 = exact match, 1 = substring match
        instance: Which instance to return if multiple matches found
        object_offset: An offset to the object to return
    
    Returns:
        The short ID of the object found, or 0 on failure
    """
    global sap_session, sap_window_num, sap_object_id, sap_object_value
    
    if sap_session is None or sap_window_num is None:
        raise SAPException(1, "Session not attached. Call sap_sess_attach() first.")
    
    sap_object_id = object_id
    sap_object_value = object_value
    
    full_id = f"wnd[{sap_window_num}]/{object_id}"
    obj = sap_session.findById(full_id)
    object_children = obj.Children
    
    object_found = False
    instance_count = instance
    
    for i in range(object_children.Count):
        child_text = object_children.item(i + 1).text
        
        # Check if it matches
        if match_type == 0 and child_text == object_value:
            object_found = True
        elif match_type == 1 and object_value in child_text:
            object_found = True
        
        if object_found:
            instance_count -= 1
            if instance_count > 0:
                object_found = False
            else:
                # Found the right instance
                found_obj = object_children.item(i + 1 + object_offset)
                found_id = found_obj.id
                # Extract short ID
                found_id = found_id[found_id.find("/wnd[") + 5:]
                found_id = found_id[found_id.find("/") + 1:]
                return found_id
    
    return 0


def sap_obj_property_set(object_id: str, object_property: str, object_value: Any) -> bool:
    """
    Sets the value of an object property within the currently attached session of SAP.
    
    Args:
        object_id: The short ID of the object
        object_property: The property to set
        object_value: The value to set the property to
    
    Returns:
        True on success, False on failure
    """
    global sap_session, sap_window_num, sap_object_id, sap_object_value
    
    if sap_session is None or sap_window_num is None:
        raise SAPException(1, "Session not attached. Call sap_sess_attach() first.")
    
    sap_object_id = object_id
    sap_object_value = object_value
    full_id = f"wnd[{sap_window_num}]/{object_id}"
    obj = sap_session.findById(full_id)
    
    # Text property (universal)
    if object_property == "text":
        obj.text = object_value
    # Checkbox selected
    elif "/chk" in object_id and object_property == "selected":
        obj.selected = object_value
    # Label or text caret position
    elif ("/lbl" in object_id or "/txt" in object_id) and object_property == "caretPosition":
        obj.caretPosition = object_value
    # ComboBox key or value
    elif "/cmb" in object_id and object_property == "key":
        obj.key = object_value
    elif "/cmb" in object_id and object_property == "value":
        obj.value = object_value
    # OkCode opened
    elif "/okcd" in object_id and object_property == "opened":
        obj.opened = object_value
    # Grid properties
    elif "/cntlGRID" in object_id:
        setattr(obj, object_property, object_value)
    
    return True


def sap_obj_property_get(object_id: str, object_property: str) -> Any:
    """
    Get the value of an object property within the currently attached session of SAP.
    
    Args:
        object_id: The short ID of the object
        object_property: The property to get
    
    Returns:
        The value of the property, or 0 on failure
    """
    global sap_session, sap_window_num, sap_object_id
    
    if sap_session is None or sap_window_num is None:
        raise SAPException(1, "Session not attached. Call sap_sess_attach() first.")
    
    sap_object_id = object_id
    full_id = f"wnd[{sap_window_num}]/{object_id}"
    obj = sap_session.findById(full_id)
    
    try:
        return getattr(obj, object_property)
    except AttributeError:
        return 0


def sap_win_exists(win_title: str) -> bool:
    """
    Checks for the existence of a SAP window.
    
    Args:
        win_title: The title of the SAP window to check.
                   May be a substring of the full window title.
    
    Returns:
        True if window exists, False otherwise
    """
    global sap_connection
    
    if sap_connection is None:
        return False
    
    # Check each session for the window title
    for sap_sess_num in range(sap_connection.Sessions.Count):
        sap_sess = sap_connection.Children(sap_sess_num)
        
        # Check each window in each session
        for sap_window_num_tmp in range(sap_sess.Children.Count):
            try:
                window_text = sap_sess.findById(f"wnd[{sap_window_num_tmp}]").Text
                if re.search(f".*{re.escape(win_title)}.*", window_text):
                    return True
            except:
                pass
    
    return False


def sap_win_close(win_title: str) -> bool:
    """
    Closes a SAP window.
    
    Args:
        win_title: The title of the SAP window to close.
                   May be a substring of the full window title.
    
    Returns:
        True on success, False on failure
    """
    global sap_connection
    
    if sap_connection is None:
        return False
    
    # Check each session for the window title
    for sap_sess_num in range(sap_connection.Sessions.Count):
        sap_sess = sap_connection.Children(sap_sess_num)
        
        # Check each window in each session
        for sap_window_num_tmp in range(sap_sess.Children.Count):
            try:
                window_obj = sap_sess.findById(f"wnd[{sap_window_num_tmp}]")
                if re.search(f".*{re.escape(win_title)}.*", window_obj.Text):
                    window_obj.close()
                    return True
            except:
                pass
    
    return False


def sap_error_handler_register(function_name: str = "sap_internal_error_handler") -> bool:
    """
    Register and enable a SAP COM error handler.
    
    Args:
        function_name: The name of the error handler function to use
    
    Returns:
        True on success, False on failure
    """
    global sap_user_error_handler, sap_error_handler
    
    sap_user_error_handler = function_name
    # In Python, error handling is typically done via exceptions
    # This is a placeholder for COM error handling
    return True


def sap_internal_error_handler(error_code: int, error_description: str, 
                               error_source: str = "", error_help_context: int = 0):
    """
    Internal SAP COM error handler.
    
    Args:
        error_code: The error code
        error_description: The error description
        error_source: The source of the error
        error_help_context: Help context for the error
    """
    global sap_object_id, sap_object_value
    
    error_output = f"""
COM Error Encountered in SAP Automation Script:
  Object ID: {sap_object_id}
  Object Value: {sap_object_value}
  Error Code: {error_code}
  Error Description: {error_description}
  Error Source: {error_source}
  Help Context: {error_help_context}
"""
    print(error_output, file=sys.stderr)
    return True


# Backward compatibility aliases
sap_sess_attach = sap_sess_attach
sap_sess_create = sap_sess_create
sap_vkeys_send = sap_vkeys_send
sap_vkeys_send_until_win_exists = sap_vkeys_send_until_win_exists
sap_obj_select = sap_obj_select
sap_obj_deselect = sap_obj_deselect
sap_obj_value_set = sap_obj_value_set
sap_obj_value_get = sap_obj_value_get
sap_obj_find_by_value = sap_obj_find_by_value
sap_obj_property_set = sap_obj_property_set
sap_obj_property_get = sap_obj_property_get
sap_win_exists = sap_win_exists
sap_win_close = sap_win_close
sap_error_handler_register = sap_error_handler_register
