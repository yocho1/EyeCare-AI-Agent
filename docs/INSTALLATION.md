# Installation Guide - EyeCare AI Agent

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Windows Installation](#windows-installation)
3. [macOS Installation](#macos-installation)
4. [Linux Installation](#linux-installation)
5. [Virtual Environment Setup](#virtual-environment-setup)
6. [API Configuration](#api-configuration)
7. [Verification](#verification)
8. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements

- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **Python**: 3.11 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB free space
- **Camera**: Optional (for light detection)
- **Internet**: Required for AI features

### Recommended Requirements

- Python 3.11+
- 8GB RAM
- Webcam with 720p resolution
- Fast internet connection
- OpenRouter API account (for AI)

## Windows Installation

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```

### Step 2: Install Git (Optional)

1. Download from [git-scm.com](https://git-scm.com/)
2. Run installer with default settings
3. Verify:
   ```bash
   git --version
   ```

### Step 3: Clone or Download Project

**Option A: Using Git**

```bash
git clone https://github.com/yocho1/EyeCare-AI-Agent.git
cd EyeCare-AI-Agent
```

**Option B: Download ZIP**

1. Download ZIP from GitHub
2. Extract to desired location
3. Open PowerShell in that folder

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

If you get an error, try:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Step 5: Configure (Optional)

1. Copy environment template:

   ```bash
   copy .env.template .env
   ```

2. Edit `.env` with your favorite text editor
3. Add OpenRouter API key if you have one

### Step 6: Run Application

```bash
python main.py
```

## macOS Installation

### Step 1: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python

```bash
brew install python@3.11
```

### Step 3: Clone Repository

```bash
git clone https://github.com/yocho1/EyeCare-AI-Agent.git
cd EyeCare-AI-Agent
```

### Step 4: Install Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 5: Grant Camera Permissions

1. Go to System Preferences → Security & Privacy
2. Click Camera tab
3. Allow Terminal/Python to access camera

### Step 6: Run Application

```bash
python3 main.py
```

## Linux Installation

### Step 1: Install Python and Dependencies

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install python3.11 python3-pip python3-tk python3-dev
sudo apt install libopencv-dev python3-opencv
```

**Fedora:**

```bash
sudo dnf install python311 python3-pip python3-tkinter
sudo dnf install opencv opencv-python
```

**Arch Linux:**

```bash
sudo pacman -S python python-pip tk opencv
```

### Step 2: Clone Repository

```bash
git clone https://github.com/yocho1/EyeCare-AI-Agent.git
cd EyeCare-AI-Agent
```

### Step 3: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 4: Set Up Camera Access

Add your user to video group:

```bash
sudo usermod -a -G video $USER
```

Log out and log back in for changes to take effect.

### Step 5: Run Application

```bash
python3 main.py
```

## Virtual Environment Setup

### Why Use Virtual Environment?

- Isolates dependencies
- Prevents conflicts
- Cleaner installation

### Windows

```bash
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py

# Deactivate when done
deactivate
```

### macOS/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py

# Deactivate when done
deactivate
```

## API Configuration

### Get OpenRouter API Key

1. Visit [openrouter.ai](https://openrouter.ai/)
2. Sign up for free account
3. Go to [Keys](https://openrouter.ai/keys)
4. Create new API key
5. Copy the key

### Configure Application

1. Copy template:

   ```bash
   cp .env.template .env
   ```

2. Edit `.env`:

   ```env
   OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
   OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct
   ```

3. Save file

### Available Models

- `meta-llama/llama-3.1-8b-instruct` (Default, Free)
- `anthropic/claude-3.5-sonnet` (Premium)
- `openai/gpt-4o` (Premium)
- `openai/gpt-4o-mini` (Budget)
- `mistralai/mixtral-8x7b-instruct` (Mid-range)

## Verification

### Test Installation

```bash
python main.py
```

You should see:

1. Banner with version info
2. Main window opens
3. Status shows "ACTIVE"
4. No error messages

### Test Components

1. **Break Timer**: Wait 20 minutes (or change config for testing)
2. **Light Detection**: Check "💡 Check Light" button
3. **Notifications**: Should receive test notification
4. **AI (if configured)**: Check recommendations panel

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'customtkinter'"**

```bash
pip install customtkinter
```

**Issue: Camera not working**

- Try different camera_index (0, 1, 2) in config.json
- Check camera permissions
- App works without camera (uses time-based estimation)

**Issue: Notifications not showing**

```bash
pip install plyer
```

**Issue: "Python not found"**

- Add Python to PATH
- Use `py` instead of `python` on Windows

## Next Steps

1. **Configure Settings**: Edit `config.json` for your preferences
2. **Set Up API**: Add OpenRouter key for AI features
3. **Test Features**: Try all buttons and panels
4. **Auto-Start**: Set up to run on system startup
5. **Calibrate Camera**: For accurate light readings

## Getting Help

- **Documentation**: See [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/yocho1/EyeCare-AI-Agent/issues)
- **Community**: [Discussions](https://github.com/yocho1/EyeCare-AI-Agent/discussions)

## Updates

To update to latest version:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

**Installation complete! Enjoy healthier eyes! 👁️✨**
