# 🧹 Folder Cleanup Script

A simple and customizable script to help you keep your folders clean by automatically moving and deleting old files based on flexible rules.

---

## ✨ Features

* 📁 **Automatically moves files** older than a specified number of days to an exclusion queue
* 🗑️ **Deletes files** from the exclusion queue after another specified period
* ⚙️ Fully **configurable via a JSON settings file**
* 🧾 **Logs all actions** performed (moves, deletions, errors)
* 💻 Easy to use and automate with `cron`

---

## 🚀 How It Works

1. **Move Phase**

   Files (and optionally folders) in your cleanup folder that haven’t been accessed for a set number of days are **moved to the exclusion queue**.

2. **Delete Phase**

   Files and folders in the exclusion queue that remain untouched for another configured period are **permanently deleted**.

3. **Logging**

   All actions are **logged to a file** for easy tracking and debugging.

---

## ⚙️ Setup & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/guilhermelcosta/download-cleanup-script.git
cd download-cleanup-script
```

---

### 2. Configure the Settings

Edit or create the `cleanup_settings.json` file in the project directory with your desired values:

```json
{
  "move_delay": 30,
  "exclusion_delay": 60,
  "should_move_folder": true,
  "cleanup_folder_name": "Downloads",
  "exclusion_folder_name": "exclusion_queue",
  "cleanup_log_name": "cleanup_log.txt",
  "cleanup_folder_path": "/home/your_user/Downloads",
  "exclusion_folder_path": "/home/your_user/Downloads/exclusion_queue",
  "cleanup_log_path": "/home/your_user/Downloads/exclusion_queue/cleanup_log.txt"
}
```

If this file is missing or partially filled, the script will use **default values**:

| Setting                 | Default              |
| ----------------------- | -------------------- |
| `move_delay`            | 30 days              |
| `exclusion_delay`       | 60 days              |
| `should_move_folder`    | `false` (only files) |
| `cleanup_folder_name`   | `"Downloads"`        |
| `exclusion_folder_name` | `"exclusion_queue"`  |
| `cleanup_log_name`      | `"cleanup_log.txt"`  |

---

### 3. Run the Script

```bash
python cleanup_script.py
```

or

```bash
python3 cleanup_script.py
```
---

## 🔄 Automating with Crontab

To run the script automatically, you can use `cron`, a built-in Linux scheduler.

### Open Your Crontab

```bash
crontab -e
```

### Option A: Run Once at Startup

```cron
@reboot /usr/bin/python3 /home/your_user/download-cleanup-script/cleanup_script.py
```

### Option B: Run Daily at 8 AM

```cron
0 8 * * * /usr/bin/python3 /home/your_user/download-cleanup-script/cleanup_script.py
```

### Option C: Run Every Hour

```cron
0 * * * * /usr/bin/python3 /home/your_user/download-cleanup-script/cleanup_script.py
```

You can customize the timing using [cron syntax](https://crontab.guru/).

> 💡 Tip: To ensure the script actually runs, you can redirect its output to a log file:
>
> ```cron
> @reboot /usr/bin/python3 /path/to/cleanup_script.py >> /path/to/cron_log.txt 2>&1
> ```

---

## 🛠️ Configuration Options Explained

| Key                     | Description                                                         |
| ----------------------- | ------------------------------------------------------------------- |
| `move_delay`            | Days before moving files to the exclusion queue                     |
| `exclusion_delay`       | Days before deleting files from the exclusion queue                 |
| `should_move_folder`    | If `true`, folders are also moved and deleted                       |
| `cleanup_folder_name`   | Name of the folder to clean (usually `"Downloads"`)                 |
| `exclusion_folder_name` | Folder used as a temporary holding area (e.g., `"exclusion_queue"`) |
| `cleanup_log_name`      | File name for logging actions (e.g., `"cleanup_log.txt"`)           |

---

## 🧪 Testing & Debugging

To manually test or debug the script, simply run:

```bash
python cleanup_script.py
```

or

```bash
python3 cleanup_script.py
```

Make sure you have the correct paths and permissions for the folders involved.

---

## 📄 Requirements

* Python **3.6 or later**

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repository, open issues, or submit pull requests with improvements.
