# Quick Start Guide - EyeCare AI Agent

## 5-Minute Setup

### 1. Install Python (if not installed)

```bash
# Check if Python is installed
python --version

# If not, download from python.org (3.11+)
```

### 2. Install Application

```bash
# Clone or download the repository
git clone https://github.com/yocho1/EyeCare-AI-Agent.git
cd EyeCare-AI-Agent

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Application

```bash
python main.py
```

That's it! The application will start with default settings.

## First Use

### What You'll See

1. **Main Dashboard** opens automatically
2. **Status Cards** at the top show:

   - Agent status (Active/Paused)
   - Current light level
   - Eye strain level
   - Next break countdown

3. **Monitoring Section** displays:

   - Light level progress bar
   - Screen time today
   - Eye strain risk

4. **AI Recommendations** (bottom panel)
   - Personalized advice
   - Updates every 30 seconds

### Basic Controls

- **🛑 Take Break Now**: Start a break immediately
- **⏸️ Pause (1 hour)**: Disable reminders temporarily
- **📊 Analytics**: View your statistics
- **💡 Check Light**: Manual light level check

## Using the 20-20-20 Rule

Every 20 minutes, you'll receive a reminder:

1. **Notification appears** (with sound)
2. **Modal window shows** instructions
3. **Look away** from screen
4. **Focus on object** 20 feet (6 meters) away
5. **Hold for 20 seconds**
6. Click **"Done"** when finished

## Optional: Add AI Features

### Get Free API Key

1. Visit [openrouter.ai](https://openrouter.ai/)
2. Sign up (takes 1 minute)
3. Get API key from [Keys page](https://openrouter.ai/keys)

### Configure

```bash
# Copy template
copy .env.template .env

# Edit .env and add your key:
OPENROUTER_API_KEY=your_key_here
```

Restart the application to enable AI recommendations.

## Tips for Best Results

### Lighting

- Aim for 300-500 lux (comfortable office lighting)
- Avoid direct sunlight on screen
- Use the "Check Light" button regularly

### Breaks

- Don't skip breaks (builds bad habits)
- Stand up and stretch during breaks
- Look at distant objects (relaxes eye muscles)

### Settings

Edit `config.json` to customize:

- Break interval (default: 20 minutes)
- Break duration (default: 20 seconds)
- Light check frequency (default: 30 seconds)

## Common Scenarios

### Working from Home

```json
{
  "work_interval_minutes": 20,
  "enable_breaks": true,
  "auto_pause_on_idle": true
}
```

### Intense Coding Session

```json
{
  "work_interval_minutes": 15,
  "break_duration_seconds": 30
}
```

### Presentation/Meeting

Click **"Pause (1 hour)"** button

### Gaming

Not recommended, but:

```json
{
  "work_interval_minutes": 30,
  "break_duration_seconds": 10
}
```

## System Tray

### Minimize to Tray

- Close window (X button) → App moves to tray
- Click tray icon → Restore window

### Right-Click Menu

- Show Dashboard
- Pause for 1 hour
- Take Break Now
- Light Analysis
- Exit

## Keyboard Shortcuts (Future Feature)

- `Ctrl+B`: Take break now
- `Ctrl+P`: Pause/Resume
- `Ctrl+L`: Check light
- `Ctrl+Q`: Quit

## Health Tips

### Good Habits

- ✅ Take every break
- ✅ Look at distant objects
- ✅ Blink frequently
- ✅ Proper lighting (300-500 lux)
- ✅ Screen 20-26 inches away
- ✅ Top of screen at eye level

### Bad Habits to Avoid

- ❌ Skipping breaks
- ❌ Working in dark rooms
- ❌ Screen too close (<20 inches)
- ❌ Screen too bright or dim
- ❌ Ignoring eye strain symptoms

### When to See a Doctor

- Persistent eye pain
- Blurred vision that doesn't improve
- Frequent headaches
- Red, irritated eyes
- Double vision

## Troubleshooting

### App Won't Start

```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### No Notifications

- Check Windows notification settings
- Ensure `show_notifications: true` in config.json
- Run: `pip install plyer`

### Camera Not Working

- Grant camera permissions
- Try different camera index (0, 1, 2)
- App works without camera (time-based mode)

### High CPU Usage

Increase check intervals in config.json:

```json
{
  "check_interval_seconds": 60,
  "camera_enabled": false
}
```

## Getting More Help

- 📖 Full Documentation: [README.md](../README.md)
- 🔧 Installation Guide: [INSTALLATION.md](INSTALLATION.md)
- 🐛 Report Issues: [GitHub Issues](https://github.com/yocho1/EyeCare-AI-Agent/issues)
- 💬 Community: [Discussions](https://github.com/yocho1/EyeCare-AI-Agent/discussions)

## Updates

Stay updated:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

**You're all set! Take care of your eyes! 👁️✨**

**Next Steps:**

1. Let the app run for a full day
2. Check your analytics tomorrow
3. Adjust settings to your preference
4. Share with friends and colleagues
