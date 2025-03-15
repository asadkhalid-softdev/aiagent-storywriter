from collections import deque
import time
import json
import os
import logging
import psutil
import threading
from pathlib import Path
import sys

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from config.config import OUTPUT_DIR


class PerformanceMonitor:
    def __init__(self, max_history=100):
        """
        Initialize the performance monitor.
        
        Args:
            max_history (int): Maximum number of operations to keep in history
        """
        self.operation_history = deque(maxlen=max_history)
        self.monitoring = False
        self.monitor_thread = None
        self.resource_usage = []
        self.sampling_interval = 1  # seconds
    
    def start_operation(self, operation_name):
        """
        Start tracking an operation.
        
        Args:
            operation_name (str): Name of the operation
        """
        start_time = time.time()
        self.operation_history.append({
            "operation": operation_name,
            "start_time": start_time,
            "end_time": None,
            "duration": None
        })
        logging.info(f"Started operation: {operation_name}")
    
    def end_operation(self, operation_name):
        """
        End tracking an operation.
        
        Args:
            operation_name (str): Name of the operation
        """
        end_time = time.time()
        for op in reversed(self.operation_history):
            if op["operation"] == operation_name and op["end_time"] is None:
                op["end_time"] = end_time
                op["duration"] = end_time - op["start_time"]
                logging.info(f"Ended operation: {operation_name}, Duration: {op['duration']:.2f} seconds")
                break
    
    def start_monitoring(self):
        """
        Start monitoring system resource usage.
        """
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_resources)
            self.monitor_thread.daemon = True  # Make thread exit when main program exits
            self.monitor_thread.start()
            logging.info("Started resource monitoring")
    
    def stop_monitoring(self):
        """
        Stop monitoring system resource usage.
        """
        if self.monitoring:
            self.monitoring = False
            if self.monitor_thread:
                self.monitor_thread.join(timeout=2)  # Wait up to 2 seconds for thread to finish
            logging.info("Stopped resource monitoring")
    
    def _monitor_resources(self):
        """
        Monitor system resource usage in a separate thread.
        """
        while self.monitoring:
            try:
                usage = {
                    "timestamp": time.time(),
                    "cpu": psutil.cpu_percent(interval=None),
                    "memory": psutil.virtual_memory().percent,
                    "disk": psutil.disk_usage('/').percent
                }
                self.resource_usage.append(usage)
                logging.debug(f"Resource usage: {usage}")
            except Exception as e:
                logging.error(f"Error monitoring resources: {str(e)}")
            
            time.sleep(self.sampling_interval)
    
    def get_operation_stats(self):
        """
        Get statistics about completed operations.
        
        Returns:
            dict: Operation statistics
        """
        stats = {}
        for op in self.operation_history:
            if op["duration"] is not None:
                op_name = op["operation"]
                if op_name not in stats:
                    stats[op_name] = {
                        "count": 0,
                        "total_time": 0,
                        "min_time": float('inf'),
                        "max_time": 0
                    }
                
                stats[op_name]["count"] += 1
                stats[op_name]["total_time"] += op["duration"]
                stats[op_name]["min_time"] = min(stats[op_name]["min_time"], op["duration"])
                stats[op_name]["max_time"] = max(stats[op_name]["max_time"], op["duration"])
        
        # Calculate averages
        for op_name in stats:
            stats[op_name]["avg_time"] = stats[op_name]["total_time"] / stats[op_name]["count"]
        
        return stats
    
    def save_performance_data(self, output_dir=None):
        """
        Save performance data to JSON files.
        
        Args:
            output_dir (str, optional): Directory to save files. If None, uses logs directory.
            
        Returns:
            tuple: Paths to the saved files
        """
        if output_dir is None:
            output_dir = os.path.join(str(Path(__file__).parent.parent), "logs")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save operation history
        history_path = os.path.join(output_dir, "operation_history.json")
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(list(self.operation_history), f, indent=2)
        
        # Save resource usage
        usage_path = os.path.join(output_dir, "resource_usage.json")
        with open(usage_path, "w", encoding="utf-8") as f:
            json.dump(self.resource_usage, f, indent=2)
        
        # Save operation stats
        stats_path = os.path.join(output_dir, "operation_stats.json")
        with open(stats_path, "w", encoding="utf-8") as f:
            json.dump(self.get_operation_stats(), f, indent=2)
        
        logging.info(f"Saved performance data to {output_dir}")
        return (history_path, usage_path, stats_path)


if __name__ == "__main__":
    # Configure basic logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Test the PerformanceMonitor
    monitor = PerformanceMonitor()
    monitor.start_monitoring()
    
    # Simulate a few operations
    monitor.start_operation("Story Generation")
    time.sleep(2)  # Simulate operation duration
    monitor.end_operation("Story Generation")
    
    monitor.start_operation("Image Generation")
    time.sleep(3)  # Simulate operation duration
    monitor.end_operation("Image Generation")
    
    monitor.start_operation("Story Generation")
    time.sleep(1.5)  # Simulate operation duration
    monitor.end_operation("Story Generation")
    
    # Stop monitoring and save data
    monitor.stop_monitoring()
    monitor.save_performance_data()
    
    # Print stats
    print("Operation Statistics:")
    stats = monitor.get_operation_stats()
    for op_name, op_stats in stats.items():
        print(f"  {op_name}:")
        print(f"    Count: {op_stats['count']}")
        print(f"    Average Time: {op_stats['avg_time']:.2f} seconds")
        print(f"    Min Time: {op_stats['min_time']:.2f} seconds")
        print(f"    Max Time: {op_stats['max_time']:.2f} seconds")
