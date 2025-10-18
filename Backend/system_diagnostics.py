import psutil
import platform
import subprocess
import os
import json
from datetime import datetime
import sys

class SystemDiagnostics:
    def __init__(self):
        self.os_type = platform.system()
        
    def get_basic_info(self):
        """Get basic system information"""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "platform": platform.platform(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": sys.version,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_process_info(self):
        """Get running processes and resource usage"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage, get top 10
        top_cpu = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:10]
        
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "top_processes": top_cpu
        }
    
    def get_network_info(self):
        """Get network status"""
        try:
            connections = psutil.net_connections(kind='inet')
            return {
                "active_connections": len(connections),
                "network_stats": dict(psutil.net_io_counters()._asdict())
            }
        except:
            return {"error": "Network info access denied"}
    
    def get_recent_logs(self, lines=50):
        """Get recent system logs"""
        logs = []
        
        if self.os_type == "Linux":
            try:
                result = subprocess.run(
                    ["journalctl", "-n", str(lines), "--no-pager"],
                    capture_output=True, text=True, timeout=5
                )
                logs.append({"source": "journalctl", "content": result.stdout})
            except:
                pass
                
            # Try dmesg
            try:
                result = subprocess.run(
                    ["dmesg", "-T"], capture_output=True, text=True, timeout=5
                )
                logs.append({"source": "dmesg", "content": result.stdout[-5000:]})
            except:
                pass
                
        elif self.os_type == "Darwin":  # macOS
            try:
                result = subprocess.run(
                    ["log", "show", "--predicate", "eventMessage contains 'error'", 
                     "--style", "syslog", "--last", "1h"],
                    capture_output=True, text=True, timeout=5
                )
                logs.append({"source": "macOS log", "content": result.stdout[-5000:]})
            except:
                pass
                
        elif self.os_type == "Windows":
            try:
                result = subprocess.run(
                    ["powershell", "-Command", 
                     "Get-EventLog -LogName System -Newest 50 | Format-List"],
                    capture_output=True, text=True, timeout=5
                )
                logs.append({"source": "Windows Event Log", "content": result.stdout})
            except:
                pass
        
        return logs
    
    def check_command_availability(self, commands):
        """Check if specific commands are available"""
        availability = {}
        for cmd in commands:
            try:
                if self.os_type == "Windows":
                    result = subprocess.run(
                        ["where", cmd], capture_output=True, timeout=2
                    )
                else:
                    result = subprocess.run(
                        ["which", cmd], capture_output=True, timeout=2
                    )
                availability[cmd] = result.returncode == 0
            except:
                availability[cmd] = False
        return availability
    
    def get_environment_vars(self):
        """Get relevant environment variables"""
        relevant_vars = ['PATH', 'PYTHONPATH', 'NODE_PATH', 'JAVA_HOME', 
                        'HOME', 'USER', 'SHELL', 'LANG']
        return {var: os.environ.get(var, "Not set") for var in relevant_vars}
    
    def run_diagnostics(self, user_problem="", relevant_commands=None):
        """Run complete diagnostics"""
        if relevant_commands is None:
            relevant_commands = ['python', 'pip', 'node', 'npm', 'git', 'docker']
        
        diagnostics = {
            "user_problem": user_problem,
            "basic_info": self.get_basic_info(),
            "resources": self.get_process_info(),
            "network": self.get_network_info(),
            "environment": self.get_environment_vars(),
            "command_availability": self.check_command_availability(relevant_commands),
            "recent_logs": self.get_recent_logs(30)
        }
        
        return diagnostics

if __name__ == "__main__":
    # Test the diagnostics
    diag = SystemDiagnostics()
    result = diag.run_diagnostics("Testing diagnostics collection")
    print(json.dumps(result, indent=2, default=str))
