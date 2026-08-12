"""
SAP Script: Example Data Entry Automation
Purpose: Demonstrates common SAP automation patterns
Created: 2024

This script shows how to:
- Connect to SAP
- Navigate to a transaction
- Fill form fields
- Submit data
- Handle errors
"""

import SAP
import time


def connect_to_sap():
    """Connect to the SAP system.
    
    Establishes connection to SAP GUI and logs into Easy Access.
    
    Returns:
        Boolean indicating successful connection.
    """
    try:
        SAP.sap_sess_attach("SAP Easy Access")
        print("Successfully connected to SAP")
        return True
    except SAP.SAPException as e:
        print(f"Connection error: {e.message}")
        return False


def navigate_to_transaction(transaction_code):
    """Navigate to a specific SAP transaction.
    
    Args:
        transaction_code: The SAP transaction code (e.g., "ZT001").
    
    Returns:
        Boolean indicating successful navigation.
    """
    try:
        # Enter transaction code in command field
        SAP.sap_obj_value_set("usr/ctxt[0]", transaction_code)
        print(f"Entered transaction code: {transaction_code}")
        
        # Press Enter to navigate
        SAP.sap_vkeys_send("Enter")
        print("Navigating to transaction...")
        
        # Wait for screen to load
        time.sleep(2)
        return True
    except SAP.SAPException as e:
        print(f"Navigation error: {e.message}")
        return False


def fill_form_data(field_mappings):
    """Fill multiple form fields with provided data.
    
    Args:
        field_mappings: Dictionary mapping field IDs to values.
                       Example: {"usr/ctxt[0]": "VALUE1", "usr/ctxt[1]": "VALUE2"}
    
    Returns:
        Boolean indicating successful completion.
    """
    try:
        for field_id, value in field_mappings.items():
            SAP.sap_obj_value_set(field_id, value)
            print(f"Field {field_id} set to: {value}")
            time.sleep(0.5)  # Small pause between fields
        
        print("Form filled successfully")
        return True
    except SAP.SAPException as e:
        print(f"Form fill error: {e.message}")
        return False


def submit_form(button_id="usr/btn[0]"):
    """Submit the form by clicking submit button.
    
    Args:
        button_id: Object ID of submit button (default: first button).
    
    Returns:
        Boolean indicating successful submission.
    """
    try:
        SAP.sap_obj_select(button_id)
        print("Form submitted")
        time.sleep(1)
        return True
    except SAP.SAPException as e:
        print(f"Submit error: {e.message}")
        return False


def check_for_errors():
    """Check SAP status bar for error messages.
    
    Returns:
        Tuple of (has_error: bool, message: str).
    """
    try:
        # Read status bar message (adjust object ID as needed)
        message = SAP.sap_obj_value_get("usr/sbar[0]")
        
        if "error" in str(message).lower():
            return True, str(message)
        return False, str(message)
    except SAP.SAPException:
        # Status bar might not exist, return no error
        return False, ""


def main():
    """Main execution function.
    
    Demonstrates complete workflow:
    1. Connect to SAP
    2. Navigate to transaction
    3. Fill form data
    4. Submit form
    5. Check results
    """
    print("=" * 60)
    print("SAP Automation Script Started")
    print("=" * 60)
    
    # Step 1: Connect
    if not connect_to_sap():
        print("Failed to connect to SAP")
        return False
    
    # Step 2: Navigate
    if not navigate_to_transaction("ZT001"):
        print("Failed to navigate to transaction")
        return False
    
    # Step 3: Prepare data
    data_to_enter = {
        "usr/ctxt[0]": "CUSTOMER001",
        "usr/ctxt[1]": "John Doe",
        "usr/ctxt[2]": "1000.00"
    }
    
    # Step 4: Fill form
    if not fill_form_data(data_to_enter):
        print("Failed to fill form")
        return False
    
    # Step 5: Submit form
    if not submit_form():
        print("Failed to submit form")
        return False
    
    # Step 6: Check for errors
    has_error, message = check_for_errors()
    if has_error:
        print(f"Error after submission: {message}")
        return False
    
    print("=" * 60)
    print("Script completed successfully")
    print("=" * 60)
    return True


if __name__ == "__main__":
    try:
        success = main()
        exit_code = 0 if success else 1
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit_code = 2
    
    exit(exit_code)
