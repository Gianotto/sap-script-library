"""
SAP Script: Batch Processing Example
Purpose: Demonstrates processing multiple records in a loop
Created: 2024

This script shows how to:
- Process multiple records from a list
- Reuse automation functions
- Track processing status
- Handle errors gracefully
"""

import SAP
import time
from datetime import datetime


class SAPBatchProcessor:
    """Handles batch processing of records in SAP.
    
    This class encapsulates batch processing logic, tracking success/failure
    of individual records and providing detailed reporting.
    """
    
    def __init__(self):
        """Initialize the batch processor."""
        self.processed_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.results = []
    
    def process_batch(self, records, transaction_code):
        """Process a batch of records through SAP.
        
        Args:
            records: List of dictionaries containing record data.
                    Each dict should have: {"id": "...", "amount": "...", ...}
            transaction_code: SAP transaction code to navigate to.
        
        Returns:
            Boolean indicating all records processed (True even if some failed).
        """
        print(f"Starting batch processing of {len(records)} records")
        print(f"Transaction: {transaction_code}")
        print("-" * 60)
        
        try:
            SAP.sap_sess_attach("SAP Easy Access")
            print("Connected to SAP")
            
            for idx, record in enumerate(records, 1):
                record_result = self.process_single_record(
                    record, transaction_code
                )
                self.results.append(record_result)
                
                if record_result["success"]:
                    self.success_count += 1
                    status = "SUCCESS"
                else:
                    self.failed_count += 1
                    status = "FAILED"
                
                self.processed_count = idx
                print(f"[{idx}/{len(records)}] Record {record['id']}: {status}")
        
        except SAP.SAPException as e:
            print(f"SAP error during batch processing: {e.message}")
            return False
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return False
        
        return True
    
    def process_single_record(self, record, transaction_code):
        """Process a single record.
        
        Args:
            record: Dictionary with record data.
            transaction_code: SAP transaction to execute.
        
        Returns:
            Dictionary with processing result.
        """
        result = {
            "record_id": record.get("id"),
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "error": None
        }
        
        try:
            # Navigate to transaction if not already there
            SAP.sap_obj_value_set("usr/ctxt[0]", transaction_code)
            SAP.sap_vkeys_send("Enter")
            time.sleep(1)
            
            # Fill in record data
            SAP.sap_obj_value_set("usr/ctxt[0]", record.get("id", ""))
            time.sleep(0.3)
            
            SAP.sap_obj_value_set("usr/ctxt[1]", record.get("amount", ""))
            time.sleep(0.3)
            
            SAP.sap_obj_value_set("usr/ctxt[2]", record.get("description", ""))
            time.sleep(0.3)
            
            # Submit the record
            SAP.sap_obj_select("usr/btn[0]")
            time.sleep(1)
            
            result["success"] = True
        
        except SAP.SAPException as e:
            result["error"] = e.message
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def print_summary(self):
        """Print processing summary."""
        print("\n" + "=" * 60)
        print("BATCH PROCESSING SUMMARY")
        print("=" * 60)
        print(f"Total Records: {self.processed_count}")
        print(f"Successful: {self.success_count}")
        print(f"Failed: {self.failed_count}")
        
        if self.failed_count > 0:
            print("\nFailed Records:")
            for result in self.results:
                if not result["success"]:
                    print(f"  - {result['record_id']}: {result['error']}")
        
        print("=" * 60)


def prepare_test_data():
    """Prepare sample records for batch processing.
    
    Returns:
        List of dictionaries with test data.
    """
    records = [
        {"id": "CUST001", "amount": "1000.00", "description": "Invoice Payment"},
        {"id": "CUST002", "amount": "2500.50", "description": "Purchase Order"},
        {"id": "CUST003", "amount": "750.25", "description": "Credit Memo"},
        {"id": "CUST004", "amount": "3200.00", "description": "Advance Payment"},
        {"id": "CUST005", "amount": "1500.75", "description": "Return Goods"},
    ]
    return records


def main():
    """Main execution function."""
    print("\n" + "=" * 60)
    print("SAP Batch Processing Script")
    print("=" * 60 + "\n")
    
    # Prepare test data
    records = prepare_test_data()
    
    # Create processor
    processor = SAPBatchProcessor()
    
    # Process batch
    success = processor.process_batch(records, "ZT001")
    
    # Print summary
    processor.print_summary()
    
    return success


if __name__ == "__main__":
    try:
        success = main()
        exit_code = 0 if success else 1
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit_code = 2
    
    print(f"\nScript exit code: {exit_code}")
    exit(exit_code)
