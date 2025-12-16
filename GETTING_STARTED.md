# 🚀 Getting Started with EyeCare AI Agent

## ✅ Complete Installation & Testing Guide

### Step 1: Verify Installation

Open PowerShell/Terminal in the project directory:

```powershell
# Check Python version
python --version
# Should show: Python 3.11.x or higher

# Check if dependencies are installed
pip list | Select-String "customtkinter|opencv-python|httpx"
```

### Step 2: Install Dependencies (if needed)

```powershell
pip install -r requirements.txt
```

### Step 3: Basic Configuration

The app works out-of-the-box with default settings, but you can customize:

**Option A: Use defaults** (Recommended for first run)

- Just run the app!

**Option B: Add AI features** (Optional)

1. Copy `.env.template` to `.env`
2. Add your OpenRouter API key
3. Restart app

### Step 4: First Run

```powershell
python main.py
```

**What should happen:**

1. ✅ Banner displays in console
2. ✅ "Initializing..." messages appear
3. ✅ Main window opens
4. ✅ Status shows "ACTIVE"
5. ✅ Test notification appears

**If something fails**, check the troubleshooting section below.

## 🧪 Testing the Application

### Test 1: Break Timer (Quick Test)

**Temporarily change break interval for testing:**

Edit `config.json`:

```json
{
  "break_settings": {
    "work_interval_minutes": 1,  ← Change from 20 to 1
    "break_duration_seconds": 20
  }
}
```

Restart app. You should get a break reminder in 1 minute.

**Remember to change back to 20 after testing!**

### Test 2: Light Detection

Click **"💡 Check Light"** button

**Expected results:**

- Window shows current lux level
- Status (Low/Optimal/High)
- Recommended brightness

**Troubleshooting:**

- If shows "time_based_fallback": Camera not available (OK, app still works)
- Try different camera_index in config.json (0, 1, or 2)

### Test 3: Manual Break

Click **"🛑 Take Break Now"**

**Expected results:**

- Break modal window appears
- Instructions displayed
- Can click "Done" or "Skip"

### Test 4: Pause/Resume

Click **"⏸️ Pause (1 hour)"**

**Expected results:**

- Button changes to "▶️ Resume"
- Next break shows 99:99 (paused)
- Click Resume to restart

### Test 5: Analytics

Click **"📊 Analytics"**

**Expected results:**

- Window shows today's stats
- Screen time, breaks, compliance
- Should have data after first break

### Test 6: System Tray

**Minimize window (click X)**

**Expected results:**

- Window hides
- Icon appears in system tray
- Right-click icon shows menu

**Restore:**

- Click tray icon
- Or right-click → "Show Dashboard"

### Test 7: AI Recommendations (if configured)

Wait 30 seconds after start

**Expected results:**

- AI panel shows recommendations
- Updates based on light conditions
- Shows actionable advice

**If no AI:**

- Panel shows rule-based advice
- Still functional, just simpler

## 📊 Verify Everything Works

Run the app for 5 minutes and check:

- [ ] Timer counting down
- [ ] Light level updates (every 30 sec)
- [ ] Screen time increases
- [ ] No error messages in console
- [ ] UI responsive

## 🔧 Troubleshooting Common Issues

### Issue: "Python not found"

**Windows:**

```powershell
# Use 'py' instead
py --version
py main.py
```

**Or add Python to PATH:**

1. Search "Environment Variables"
2. Edit PATH
3. Add `C:\Python311\` (your Python location)

### Issue: "Module not found: customtkinter"

```powershell
pip install customtkinter --upgrade
```

### Issue: Camera Error on Startup

**This is OK!** App automatically falls back to time-based light estimation.

**To fix (optional):**

1. Check camera permissions (Windows Settings → Privacy → Camera)
2. Try different camera index in config.json
3. Ensure no other app using camera

### Issue: No Notifications

```powershell
pip install plyer
```

**Windows:**

- Check Windows Settings → Notifications
- Ensure "Get notifications from apps" is ON

### Issue: Window Won't Show

**Check system tray** (bottom-right corner):

- App might be minimized to tray
- Click icon to restore

### Issue: High CPU Usage

Edit `config.json`:

```json
{
  "light_monitoring": {
    "check_interval_seconds": 60,  ← Increase from 30
    "enabled": false  ← Or disable camera
  }
}
```

### Issue: Database Errors

Delete database and restart:

```powershell
Remove-Item -Path "$env:USERPROFILE\.eyecare_agent\data\analytics.db"
```

App will create a new database.

## 📝 Check Logs

If something goes wrong, check logs:

```powershell
# Open log directory
explorer "$env:USERPROFILE\.eyecare_agent\logs"

# View today's log
Get-Content "$env:USERPROFILE\.eyecare_agent\logs\eyecare_$(Get-Date -Format 'yyyyMMdd').log"
```

Look for ERROR or CRITICAL messages.

## 🎯 Daily Usage Tips

### Morning Routine

1. Start the app
2. Check light level
3. Adjust lighting if needed
4. Begin working

### During Work

- Don't skip breaks
- Check analytics periodically
- Adjust brightness as needed

### End of Day

- Review analytics
- Check compliance rate
- Adjust settings if needed

### Weekly Review

- Export analytics
- Check trends
- Optimize settings

## 🚀 Advanced Usage

### Auto-Start on Boot

**Windows (Task Scheduler):**

```powershell
# Create basic task
# Program: python.exe
# Arguments: C:\path\to\EyeCare-AI-Agent\main.py
# Trigger: At log on
```

**Windows (Startup Folder):**

```powershell
# Create shortcut in:
shell:startup
```

### Run as Background Service

Use Windows Task Scheduler with "Run whether user is logged on or not"

### Custom Keyboard Shortcuts (Future)

Will be added in future version. For now, use mouse/tray icon.

## 📞 Getting Help

### Before Asking for Help

1. ✅ Check this document
2. ✅ Check [README.md](README.md)
3. ✅ Check [INSTALLATION.md](docs/INSTALLATION.md)
4. ✅ Check logs for errors
5. ✅ Try with default config.json

### Where to Get Help

- 📖 **Documentation**: Full docs in README.md
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yocho1/EyeCare-AI-Agent/issues)
- 💬 **Questions**: [GitHub Discussions](https://github.com/yocho1/EyeCare-AI-Agent/discussions)
- 📧 **Email**: support@eyecareai.com

### When Reporting Issues

Include:

- Python version (`python --version`)
- OS version (Windows 10/11, build number)
- Error message (full traceback)
- Log file (last 50 lines)
- What you were doing when error occurred

## 🎉 Success Checklist

After completing this guide, you should:

- [x] Installed all dependencies
- [x] Ran the application successfully
- [x] Received a break reminder
- [x] Checked light detection
- [x] Viewed analytics
- [x] Tested system tray
- [x] Know how to configure settings
- [x] Know where to get help

## 🌟 You're Ready!

Congratulations! You now have:

- ✅ Working eye care agent
- ✅ Break reminders every 20 minutes
- ✅ Light monitoring (if camera available)
- ✅ Analytics tracking
- ✅ Optional AI recommendations

**Take care of your eyes! 👁️✨**

---

**Next Steps:**

1. Use it for a full day
2. Check your analytics
3. Share with friends/colleagues
4. ⭐ Star the repo on GitHub
5. Consider contributing (see CONTRIBUTING.md)
