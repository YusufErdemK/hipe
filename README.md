![Hipe Banner](readme/hipe-bn.png)

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.13+-blue)

# HIPE: Instagram Stats Viewer

HIPE is a **Linux terminal tool** that fetches public Instagram profile statistics directly from your terminal. Quick, clean, and stylish. No login required!

---

## Features ✨

- 📊 Display Instagram profile stats (followers, following, posts, bio) in the terminal
- 💾 Export stats to JSON files for further analysis
- ✅ No authentication required - works with public profiles
- 🚀 Simple installation with `install.sh`
- 📌 Version info with `--version`
- 🎨 Clean, emoji-enhanced terminal output
- ⚡ Lightning-fast profile information retrieval

---

## Installation 

```bash
git clone https://github.com/USERNAME/hipe.git
cd hipe
chmod +x install.sh
./install.sh
```

### Requirements
- Python 3 or higher
- `pip` (Python package manager)

---

## Uninstallation

```bash
./install.sh -u
```

---

## Usage

### Display profile stats in terminal
```bash
hipe @username
```

### Save stats to JSON file
```bash
hipe @username output.json
```

This creates a JSON file with all profile information.

### Show version
```bash
hipe --version
```

---

## Example Output

## How It Works

HIPE uses Instagram's public API endpoint to fetch profile information. It doesn't require any authentication or credentials - only accesses publicly available data.

---

## License

MIT License - see LICENSE file for details

---



