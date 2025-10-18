from flask import Flask, request, jsonify
from flask_cors import CORS
from system_diagnostics import SystemDiagnostics
from ai_analyzer import AIAnalyzer
import json

app = Flask(__name__)
CORS(app)

diagnostics = SystemDiagnostics()
analyzer = AIAnalyzer()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "System Diagnostic Assistant"})

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    """Main endpoint to diagnose a problem"""
    try:
        data = request.json
        user_problem = data.get('problem', '')
        relevant_commands = data.get('commands', ['python', 'pip', 'node', 'npm', 'git'])
        
        if not user_problem:
            return jsonify({"error": "Problem description is required"}), 400
        
        # Step 1: Collect system diagnostics
        print(f"Collecting diagnostics for: {user_problem}")
        diagnostics_data = diagnostics.run_diagnostics(user_problem, relevant_commands)
        
        # Step 2: Analyze with AI
        print("Analyzing with AI...")
        analysis_result = analyzer.analyze_problem(user_problem, diagnostics_data)
        
        if not analysis_result['success']:
            return jsonify({
                "error": "AI analysis failed",
                "details": analysis_result.get('error')
            }), 500
        
        # Step 3: Return results
        return jsonify({
            "success": True,
            "problem": user_problem,
            "diagnosis": analysis_result['analysis'],
            "system_info": {
                "os": diagnostics_data['basic_info']['os'],
                "platform": diagnostics_data['basic_info']['platform'],
                "cpu_usage": diagnostics_data['resources']['cpu_percent'],
                "memory_usage": diagnostics_data['resources']['memory_percent']
            },
            "token_usage": analysis_result['usage']
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/system-info', methods=['GET'])
def system_info():
    """Get basic system information"""
    try:
        basic_info = diagnostics.get_basic_info()
        resources = diagnostics.get_process_info()
        
        return jsonify({
            "success": True,
            "system": basic_info,
            "resources": resources
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/quick-check', methods=['POST'])
def quick_check():
    """Quick check for command availability"""
    try:
        data = request.json
        commands = data.get('commands', [])
        
        availability = diagnostics.check_command_availability(commands)
        
        return jsonify({
            "success": True,
            "availability": availability
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting System Diagnostic Assistant Backend...")
    print("API will be available at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
