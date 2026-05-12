# 🧠 AI Powered System Assistant

An AI-driven system diagnostic assistant that analyzes real system information, logs, processes, and configurations using the Claude API to identify issues and provide intelligent troubleshooting solutions.

---

# 🚀 Features

* 🔍 Collects real-time system diagnostics
* 🖥️ Analyzes CPU, memory, disk usage, and running processes
* 📄 Reads recent system logs
* ⚡ Detects command availability and environment configuration
* 🤖 Uses Claude AI for intelligent root cause analysis
* 🛠️ Provides step-by-step solutions with verification commands
* ⚠️ Includes rollback instructions for risky operations

---

# 🏗️ Tech Stack

* Python
* Anthropic Claude API
* python-dotenv
* JSON
* System Diagnostic Utilities

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/phanivighnasri/AI_Powered_System_Assistant.git
cd AI_Powered_System_Assistant
```

---

## 2️⃣ Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root and add your Anthropic API key:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

---

# ▶️ Running the Project

```bash
python ai_analyzer.py
```

---

# 🧪 Example Workflow

1. User reports a system issue
2. System diagnostics are collected
3. Claude AI analyzes the system state
4. Root cause is identified
5. Step-by-step solution is generated
6. Verification and rollback instructions are provided

---

# 📌 Example Output

```json
{
  "success": true,
  "analysis": "Root cause identified...",
  "usage": {
    "input_tokens": 1200,
    "output_tokens": 450
  }
}
```

---

# 🔒 Security Notes

* Never expose your `.env` file publicly
* API keys are securely loaded using environment variables
* `.env` should be included in `.gitignore`

Example `.gitignore`:

```bash
.env
__pycache__/
venv/
```

---

# 🎯 Future Improvements

* 🌐 Web dashboard for diagnostics
* 📊 Visualization of system metrics
* 🧠 Multi-model AI support
* 🖥️ Cross-platform optimization
* 🔔 Real-time alert system
* 📁 Automated log categorization

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

# 👨‍💻 Author

Developed by Phani Vighna Sri Kadali, Shreya Egurla, Charitha Aella

---

# ⭐ Support

If you found this project helpful, consider giving it a star on GitHub.
