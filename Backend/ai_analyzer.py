import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()

class AIAnalyzer:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        
    def analyze_problem(self, user_problem, diagnostics_data):
        """Analyze the problem using Claude with full system context"""
        
        # Format diagnostics for Claude
        diagnostics_summary = self._format_diagnostics(diagnostics_data)
        
        system_prompt = """You are a system-aware technical diagnostic assistant. 
You have access to ACTUAL system state data including logs, processes, and configurations.

Your job:
1. Analyze the REAL system data provided
2. Identify the ROOT CAUSE of the issue
3. Provide SPECIFIC, step-by-step solutions based on the actual system state
4. Include verification commands after each step
5. Warn about any risky operations
6. Provide rollback instructions if needed

Format your response as:
## 🔍 Diagnosis
[What you found in the actual system data]

## 🎯 Root Cause
[The actual problem identified]

## ✅ Solution
[Step-by-step fix with exact commands for this system]

## 🔄 Verification
[How to verify the fix worked]

## ⚠️ Rollback (if needed)
[How to undo changes if something goes wrong]

Be specific, use actual paths/versions from the diagnostics, and never give generic advice."""

        user_message = f"""User's Problem: {user_problem}

ACTUAL SYSTEM DIAGNOSTICS:
{diagnostics_summary}

Please analyze this REAL system data and provide a specific solution."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            return {
                "success": True,
                "analysis": message.content[0].text,
                "usage": {
                    "input_tokens": message.usage.input_tokens,
                    "output_tokens": message.usage.output_tokens
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _format_diagnostics(self, data):
        """Format diagnostics data for Claude"""
        
        formatted = f"""
=== SYSTEM INFORMATION ===
OS: {data['basic_info']['os']} {data['basic_info']['os_version']}
Platform: {data['basic_info']['platform']}
Architecture: {data['basic_info']['architecture']}
Python: {data['basic_info']['python_version'].split()[0]}

=== RESOURCE USAGE ===
CPU: {data['resources']['cpu_percent']}%
Memory: {data['resources']['memory_percent']}%
Disk: {data['resources']['disk_percent']}%

Top CPU Processes:
"""
        for proc in data['resources']['top_processes'][:5]:
            formatted += f"- {proc['name']} (PID {proc['pid']}): {proc['cpu_percent']}% CPU\n"
        
        formatted += "\n=== COMMAND AVAILABILITY ===\n"
        for cmd, available in data['command_availability'].items():
            status = "✓ Available" if available else "✗ Not found"
            formatted += f"{cmd}: {status}\n"
        
        formatted += "\n=== ENVIRONMENT VARIABLES ===\n"
        for var, value in data['environment'].items():
            formatted += f"{var}: {value}\n"
        
        formatted += "\n=== RECENT SYSTEM LOGS (Last 30 entries) ===\n"
        for log_source in data['recent_logs']:
            formatted += f"\n--- {log_source['source']} ---\n"
            # Limit log content to prevent token overflow
            content = log_source['content']
            if len(content) > 3000:
                content = content[-3000:]  # Last 3000 chars
            formatted += content + "\n"
        
        return formatted

if __name__ == "__main__":
    # Test the analyzer
    analyzer = AIAnalyzer()
    
    # Mock diagnostics for testing
    mock_diagnostics = {
        "user_problem": "pip install fails",
        "basic_info": {
            "os": "Linux",
            "os_version": "5.15.0",
            "platform": "Linux-5.15.0-Ubuntu",
            "architecture": "x86_64",
            "python_version": "3.10.0"
        },
        "resources": {
            "cpu_percent": 25.0,
            "memory_percent": 60.0,
            "disk_percent": 75.0,
            "top_processes": [
                {"name": "python", "pid": 1234, "cpu_percent": 15.0}
            ]
        },
        "command_availability": {
            "python": True,
            "pip": True
        },
        "environment": {
            "PATH": "/usr/local/bin:/usr/bin",
            "PYTHONPATH": "Not set"
        },
        "recent_logs": [
            {"source": "test", "content": "No errors found"}
        ]
    }
    
    result = analyzer.analyze_problem("pip install fails with permission error", mock_diagnostics)
    print(json.dumps(result, indent=2))
