# 10k
A TUI app to track your ten thousand hours towards mastering a certain skill


### “I fear not the man who has practiced 10,000 kicks once, but I fear the man who has practiced one kick 10,000 times.” ~Bruce Lee

This TUI app (written in 2021) is built on the idea that true mastery of any skill takes 10,000 hours of deliberate practice. It's a curses based TUI tool to track your practice hours toward 10,000 hours of mastery, using a MySQL database for storage. 

---

## 📝 Features

* Record hours or minutes spent practicing.
* Live timer to track practice sessions.
* Progress bars for weekly, monthly, yearly, and total hours.
* Settings menu to change goals, initial hours, skill name, and manage data.
* Privacy options: change username/password.
* Simple text-based UI using `curses`.

---

## ⚙️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://your.repo.url/ten-thousand-hours.git
   cd ten-thousand-hours
   ```

2. **Ensure you have Python 3.6+**:

   ```bash
   python3 --version
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Install the CLI script**:

   ```bash
   # Normal install
   pip install .

   # Or editable mode (for development)
   pip install -e .
   ```

   This will install the `tenk-hours` command.

---

## 🔧 Configuration

Before running the tool, configure your MySQL credentials. By default, the script connects using:

```python
# tenk.py (database connection section)
conn = mycon.connect(
    user="root",      # <-- MySQL username
    password="",      # <-- MySQL password
    host="localhost"
)
```

Edit directly in `tenk.py`:

  1. Open `tenk.py` in an editor.
  2. Locate the `mycon.connect(...)` call near the top of the file.
  3. Replace `user` and `password` values accordingly.

## 🚀 Usage

After installation, simply run:

```bash
tenk-hours
```

This will:

1. Connect (or create) the `10k` database in MySQL.
2. Prompt you for your name, password, and initial settings (first run only).
3. Show the main menu to log hours, start a timer, view progress, or change settings.

---

## ⌨️ Commands

* **Log hours manually**: Choose *Enter hours spent today*.
* **Start timer**: Choose *Start tracking hours spent*.
* **Show progress**: Choose *Show your progress towards mastery*.
* **Settings**: Change goals, initial hours, skill name, or clear data.
* **Privacy**: Change username/password.
* **Exit**: Quit the application.

---

## 📂 Project Structure

```
├── tenk.py           # Main script
├── requirements.txt  # Python dependencies
├── setup.py          # Install script
└── README.md         # This file
```

---

##  License

This project is shared with the community without any warranty. Use at your own discretion.

