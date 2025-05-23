# AI-INTEGRATED-RASPBERRY-PI

A Raspberry Pi-based quiz application designed for educational and entertainment purposes. This project allows users to create, manage, and participate in quizzes with ease.

## Features

- **Customizable Quizzes**: Create and manage your own quizzes.
- **User-Friendly Interface**: Simple and intuitive design for all age groups.
- **Real-Time Scoring**: Instant feedback on quiz performance.
- **Cross-Platform**: Compatible with Raspberry Pi and other devices.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/0cleopatra0/AI-integrated-Raspberry-Pi.git
    ```
2. Navigate to the project directory:
    ```bash
    cd AI-integrated-Raspberry-Pi
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the application:
    ```bash
    python app.py
    ```

## Usage

1. Launch the application.
2. Select or create a quiz.
3. Answer the questions and view your score.

## Requirements

- Raspberry Pi (or any compatible device)
- Python 3.7+
- Required Python libraries (see `requirements.txt`)

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add feature-name"
    ```
4. Push to your branch:
    ```bash
    git push origin feature-name
    ```
5. Open a pull request.
# Raspberry Pi 5 LLM API Project Setup

> 🧠 Uses Ollama for local LLM inference, Flask API for user interaction, and supports question-answering with dynamic intelligence levels.

## ⚙️ System Prerequisites

```bash
# 🔄 Update & upgrade system
sudo apt update && sudo apt upgrade -y

# 🧰 Install system dependencies
sudo apt install -y curl git python3 python3-pip python3-venv build-essential libssl-dev libffi-dev

# 🐳 Optional: Install Docker (for MongoDB, remove if not using)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER  # then reboot
```

## 🧠 Install & Run Ollama with a Model

```bash
# 📥 Download and install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# ✅ Pull a model (phi2 recommended for RPi5)
ollama pull phi2

# ▶️ Start Ollama service (usually auto-starts in background)
ollama run phi2
```

## 🌐 Set Up Python Flask API

```bash
# 🐍 Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 📦 Install required Python packages
pip install flask requests python-dotenv

# 💾 (Optional) If MongoDB is used, also install:
# pip install pymongo

# 🚀 Run Flask server
python app.py
```

## 🛠️ Auto-Start Script at Boot (Crontab)

```bash
# 🔧 Edit crontab for pi user
crontab -e

# ⬇️ Add this line at the end to start on boot
@reboot /home/pi/rpi_flask_api/startup_script.sh >> /home/pi/rpi_flask_api/startup.log 2>&1
```

## 📁 File Structure Example

```bash
rpi_flask_api/
├── app.py                # Flask API main script
├── startup_script.sh     # Bash script for boot-time setup
├── config.json           # Saved user config (user_id, intellect)
├── .env                  # Ollama/Mongo/Flask config
├── README.md             # This file
```

## 🧪 Test the API

```bash
# 🌐 Test root endpoint
curl http://localhost:5000/

# ❓ Ask a question (replace with your values)
curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" -d '{"user_id":"user1", "question":"What is Newton\'s second law?"}'

# 🧠 Set intellect level
curl -X PUT http://localhost:5000/user/user1 -H "Content-Type: application/json" -d '{"intellect":"high"}'

# 🔁 Reset user data
curl -X DELETE http://localhost:5000/reset/user1
```

## 🧹 Remove MongoDB + Docker (If not used)

```bash
# 🗑️ Stop and disable Docker
sudo systemctl stop docker
sudo systemctl disable docker

# ❌ Uninstall Docker and remove images
sudo apt remove docker docker-engine docker.io containerd runc -y
sudo rm -rf /var/lib/docker /etc/docker
sudo groupdel docker

# ❌ Remove MongoDB (if installed via apt)
sudo apt purge mongodb-org* -y
sudo rm -rf /var/log/mongodb
sudo rm -rf /var/lib/mongodb

# 🧹 Clean up
sudo apt autoremove -y
```

## 💾 Enable 8GB Swap (If needed for large models)

```bash
# ⚙️ Edit swap config
sudo nano /etc/dphys-swapfile

# 🔢 Change CONF_SWAPSIZE=1024 to:
CONF_SWAPSIZE=8192

# 💾 Restart swap service
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

## ✅ Done!

You can now run your Flask API + Ollama model locally on Raspberry Pi 5 and ask science/math questions with customizable intelligence levels.
## Contact

For questions or suggestions, feel free to reach out at **nidxaai@gmail.com**.
