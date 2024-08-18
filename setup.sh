pip install pyautogen # pip install pyautogen[gemini,retrievechat,lmm]
pip install 'litellm[proxy]'
pip install pyqt5
sudo apt install python3-pyqt5
sudo apt install qttools5-dev-tools
sudo apt install pyqt5-dev-tools

curl -fsSL https://ollama.com/install.sh | sh
# ollama pull phi3:mini-128k
# ollama pull phi3:medium-128k
# ollama pull phi3:14b-medium-128k-instruct-q6_K
ollama pull llama3.1:8b-instruct-q8_0