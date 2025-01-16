# Vigilant Scanner

**Vigilant Scanner (vgls)** is a Python-based CLI tool designed for monitoring file integrity, detecting changes in directories, and identifying potential security threats. This tool offers an efficient solution to track modifications, additions, and deletions in directories, making it ideal for system administrators, developers, and security professionals.

---

## 🚀 Features

- **File Integrity Monitoring**: Detect changes in file content, metadata, and structure.
- **Change Detection**: Identify newly added, modified, or deleted files between scans.
- **Malware Detection**: Monitor directories for unauthorized or suspicious changes.
- **Database Integration**: Store and compare file metadata using SQLite.
- **Extensible CLI**: Intuitive commands for initialization, scanning, and updating.
- **Log Analysis** *(In Progress)*: Analyze logs for security threats and anomalies (coming soon).

---

## 🛠 Installation

Ensure Python 3.10 or later is installed. Then, install Vigilant Scanner using the steps below:

```bash
pip install vigilant-scanner
```

---

## 📋 Usage

### CLI Commands

1. **Initialize the Database**
   Create a snapshot of the current directory state and store metadata in the database:
   ```bash
   vgls init <directory>
   ```
   Example:
   ```bash
   vgls init /path/to/directory
   ```

2. **Scan and Compare**
   Scan the directory and compare results with the last snapshot:
   ```bash
   vgls scan <directory>
   ```
   Example:
   ```bash
   vgls scan /path/to/directory
   ```

3. **Update the Database**
   Update the database with the current state of the directory:
   ```bash
   vgls update <directory>
   ```
   Example:
   ```bash
   vgls update /path/to/directory
   ```

4. **Generate Reports** *(Placeholder)*
   Generate a detailed report of detected changes (coming soon):
   ```bash
   vgls report
   ```

---

## ⚙️ How It Works

1. **Initialization (`init`)**
   - Scans a directory and stores metadata (file path, hash, size, permissions, etc.) in a SQLite database.

2. **Scanning and Comparison (`scan`)**
   - Scans the directory again and compares the current state with the stored metadata.
   - Outputs new, modified, and deleted files.

3. **Updating the Database (`update`)**
   - Updates the database to reflect the latest directory state.
   - Inserts new files, updates modified files, and removes deleted files.

---

## 📝 Example Workflow

```bash
# Initialize the database with the current state of a directory
vgls init /var/www

# Perform a scan to detect changes
vgls scan /var/www

# Update the database after legitimate changes are made (deploy was conducted etc.)
vgls update /var/www
```

---

## 📋 Requirements

- Python 3.10+
- typer

---

## 🛠 Development

To contribute or run the tool locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/ivpel/vigilant-scanner.git
   ```

2. Navigate to the project directory:
   ```bash
   cd vigilant-scanner
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run tests:
   ```bash
   pytest
   ```

---

## 📜 License

This project is licensed under the GNU General Public License v3 or later (GPLv3+). See the [LICENSE](LICENSE) file for details.

---

## 💬 Support

If you encounter any issues, feel free to open a ticket on the [GitHub Bug Tracker](https://github.com/ivpel/vigilant-scanner/issues).

---

## 🔗 Links

- **Homepage**: [Vigilant Scanner on GitHub](https://github.com/ivpel/vigilant-scanner)
- **Bug Tracker**: [Report Issues](https://github.com/ivpel/vigilant-scanner/issues)

