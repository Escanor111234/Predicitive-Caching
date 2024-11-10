import os
import time
import csv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

class AccessHandler(FileSystemEventHandler):
    def __init__(self, csv_filename):
        self.access_counter = {}
        self.csv_filename = csv_filename
        self.initialize_csv()

    def initialize_csv(self):
        """Create a new CSV file with headers if it does not exist."""
        if not os.path.exists(self.csv_filename):
            with open(self.csv_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Added extra columns: File Extension, File Name Length
                writer.writerow(["File Path", "Access Time", "File Size (MB)", 
                                 "Access Count", "File Extension", 
                                 "File Name Length", "To Cache"])

    def on_modified(self, event):
        """Handle file modified events."""
        if not event.is_directory:
            self.log_access(event.src_path)

    def on_created(self, event):
        """Handle file created events."""
        if not event.is_directory:
            self.log_access(event.src_path)

    def log_access(self, file_path):
        current_time = datetime.now()
        
        # Extract file details
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert bytes to MB
        file_name = os.path.basename(file_path)
        file_name_length = len(file_name)
        file_extension = os.path.splitext(file_name)[1]
        
        # Update access count
        if file_path in self.access_counter:
            self.access_counter[file_path]["access_count"] += 1
        else:
            self.access_counter[file_path] = {
                "access_time": current_time,
                "file_size": file_size,
                "access_count": 1,
                "file_extension": file_extension,
                "file_name_length": file_name_length,
                "to_cache": 0  # Decision to cache, can implement logic here
            }

        # Example logic to mark for caching (e.g., accessed more than 5 times)
        if self.access_counter[file_path]["access_count"] > 5:
            self.access_counter[file_path]["to_cache"] = 1

        # Update the dataset with current file's access info
        self.update_dataset(file_path)

    def update_dataset(self, file_path):
        """Append new data to the CSV file."""
        access_info = self.access_counter[file_path]
        access_time_str = access_info["access_time"].strftime('%Y-%m-%d %H:%M:%S')

        # Write to CSV in append mode
        with open(self.csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([file_path, access_time_str, 
                             f"{access_info['file_size']:.2f}",  # Format size as MB
                             access_info["access_count"], 
                             access_info["file_extension"], 
                             access_info["file_name_length"], 
                             access_info["to_cache"]])

def monitor_directory(path_to_watch, csv_filename):
    """Monitor the specified directory for file access events."""
    event_handler = AccessHandler(csv_filename)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    
    print(f"Monitoring {path_to_watch} for file access events...")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    directory_to_monitor = r"C:\Users\akash\Downloads"  # Change to your directory path
    output_csv_file = r"C:\Users\akash\OneDrive\Documents\coding\C++\file_access_log1.csv"  # Change to your CSV file path

    monitor_directory(directory_to_monitor, output_csv_file)
