# 👁️✨ EyeCare AI Agent Pro

<div align="center">

**Professional Eye Care Application with AI-Powered Recommendations & Ambient Light Detection**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)](https://github.com/TomSchimansky/CustomTkinter)

</div>

## 🌟 Features

### Core Features

- **Smart Break Scheduling**: 20-minute intervals with 20-second rest reminders (20-20-20 rule)
- **Ambient Light Monitoring**: Real-time light detection using webcam or time-based estimation
- **AI-Powered Recommendations**: Personalized eye care advice using OpenRouter (Llama, GPT-4, Claude)
- **Dynamic Adjustments**: Auto-adjust break frequency based on light conditions
- **Eye Strain Prediction**: Track and predict eye strain based on usage patterns

### AI Integration

- Multiple AI model support (Llama 3.1, Claude 3.5, GPT-4o)
- Context-aware recommendations
- Light condition analysis
- Break exercise suggestions
- Eye strain advice

### Light Detection

- Webcam-based ambient light analysis
- Lux estimation with calibration support
- Time-based fallback estimation
- Auto-brightness recommendations
- Light status indicators (Optimal, Low, High, Very Low)

### Analytics & Tracking

- Screen time monitoring
- Break compliance tracking
- Light condition history
- Daily and weekly summaries
- Export functionality

### Modern UI

- Clean, professional interface built with CustomTkinter
- Dark/Light theme support
- Real-time status cards
- Progress indicators
- AI recommendation panel
- System tray integration

## 📋 Requirements

- **Python**: 3.11 or higher
- **Operating System**: Windows (primary), macOS, Linux (with modifications)
- **Webcam**: Optional (for ambient light detection)
- **OpenRouter API Key**: Optional (for AI features)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yocho1/EyeCare-AI-Agent.git
cd EyeCare-AI-Agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys (Optional)

Copy the environment template:

```bash
copy .env.template .env
```

Edit `.env` and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct
```

**Note**: AI features will work with fallback rule-based recommendations if no API key is provided.

### 4. Run the Application

```bash
python main.py
```

**Current defaults (for testing):**

- Break interval set to **1 minute** (`break_settings.work_interval_minutes` in config.json) so you can see the popup quickly. Set this back to 20 for normal use.
- Light monitoring is **disabled** in `config.json` to reduce CPU load. Set `light_monitoring.enabled` to `true` to re-enable.

## 📖 User Guide

### First Run

1. **Launch the application** - Run `python main.py`
2. **Allow camera access** (optional) - For ambient light detection
3. **Configure settings** - Adjust break intervals, notifications, etc.
4. **Start monitoring** - The agent begins tracking immediately

### Understanding the Dashboard

#### Status Cards

- **STATUS**: Shows if the agent is active, paused, or stopped
- **LIGHT**: Current ambient light level in lux and status
- **EYE STRAIN**: Predicted strain level (Low/Medium/High)
- **NEXT BREAK**: Countdown to next break reminder

#### Real-Time Monitoring

- **Light Level**: Visual indicator of current ambient lighting
- **Screen Time**: Total screen time for today
- **Eye Strain Risk**: Calculated from breaks and light conditions

#### AI Recommendations

Personalized suggestions based on:

- Current light conditions
- Break compliance
- Screen time
- Time of day

### Break Reminders

When a break is due:

1. **Notification appears** with sound (if enabled)
2. **Modal window shows** with instructions
3. **Follow 20-20-20 rule**: Look 20 feet away for 20 seconds
4. Click **"Done"** to record completion or **"Skip"** if busy

### Controls

- **Take Break Now**: Immediately trigger a break
- **Pause (1 hour)**: Temporarily disable reminders
- **Analytics**: View detailed statistics
- **Check Light**: Manual light level check

### System Tray

Right-click the tray icon for quick access:

- Show Dashboard
- Pause for 1 hour
- Take Break Now
- Light Analysis
- Exit

## ⚙️ Configuration

### config.json

Main configuration file with all settings:

```json
{
  "break_settings": {
    "work_interval_minutes": 20,
    "break_duration_seconds": 20,
    "enable_breaks": true
  },
  "light_monitoring": {
    "enabled": true,
    "camera_index": 0,
    "check_interval_seconds": 30,
    "optimal_lux_min": 300,
    "optimal_lux_max": 500
  },
  "ai_settings": {
    "enabled": true,
    "model": "meta-llama/llama-3.1-8b-instruct",
    "temperature": 0.3
  }
}
```

### Light Calibration

For accurate light readings:

1. Place a lux meter next to your webcam
2. Note the actual lux reading
3. In the app, go to Settings → Calibrate Light Sensor
4. Enter the known lux value
5. The system adjusts its calculations

### Optimal Lighting Levels

- **Very Low (<100 lux)**: Risk of eye strain
- **Low (100-300 lux)**: Suboptimal
- **Optimal (300-500 lux)**: Recommended for screen work
- **High (500-1000 lux)**: May cause glare
- **Very High (>1000 lux)**: Potential discomfort

## 🤖 AI Models

### Supported Models

1. **Llama 3.1 8B** (Default)

   - Fast, efficient
   - Good for general recommendations
   - Cost-effective

2. **Claude 3.5 Sonnet**

   - High-quality responses
   - Excellent understanding
   - More expensive

3. **GPT-4o**

   - State-of-the-art
   - Best recommendations
   - Highest cost

4. **Mixtral 8x7B**
   - Good balance
   - Multilingual support
   - Mid-range cost

### Changing Models

Edit `.env`:

```env
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

Or in `config.json`:

```json
{
  "ai_settings": {
    "model": "openai/gpt-4o"
  }
}
```

## 📊 Analytics

### Data Tracked

- Screen time (per session and daily)
- Break frequency and compliance
- Light conditions (lux readings)
- Eye strain indicators
- Weekly trends

### Export Data

```python
# In Analytics panel
Export → JSON file saved to .eyecare_agent/data/
```

### Database Location

SQLite database: `~/.eyecare_agent/data/analytics.db`

## 🛠️ Troubleshooting

### Camera Not Working

1. Check camera permissions
2. Try different camera index (0, 1, 2) in config.json
3. Ensure no other app is using the camera
4. Fallback: App uses time-based estimation automatically

### AI Not Responding

1. Verify API key in `.env`
2. Check internet connection
3. Try different model
4. Fallback: Rule-based recommendations work without AI

### Notifications Not Showing

1. Check notification permissions (Windows Settings)
2. Verify `show_notifications: true` in config
3. Install plyer: `pip install plyer`

### High CPU Usage

1. Increase `check_interval_seconds` in config (30-60)
2. Disable camera-based light detection
3. Reduce AI query frequency

## 🔧 Advanced Usage

### Running as Windows Service

Use NSSM (Non-Sucking Service Manager):

```bash
nssm install EyeCareAI "C:\Python311\python.exe" "C:\path\to\main.py"
nssm start EyeCareAI
```

### Auto-Start on Boot

Windows:

1. Press `Win+R`
2. Type `shell:startup`
3. Create shortcut to `main.py`

### Custom Exercises

Add exercises in `src/ai/prompts.py`:

```python
EXERCISE_PROMPTS = {
    "custom_exercise": """
    Your custom exercise instructions here...
    """
}
```

## 📁 Project Structure

```
EyeCare-AI-Agent/
├── main.py                 # Application entry point
├── config.json            # Main configuration
├── requirements.txt       # Dependencies
├── .env.template         # API key template
│
├── src/
│   ├── core/             # Core functionality
│   │   ├── agent.py      # Main orchestrator
│   │   ├── scheduler.py  # Break scheduler
│   │   ├── notifier.py   # Notifications
│   │   └── analytics.py  # Data tracking
│   │
│   ├── ai/               # AI integration
│   │   ├── openrouter_client.py
│   │   └── prompts.py
│   │
│   ├── hardware/         # Hardware interfaces
│   │   ├── camera_manager.py
│   │   ├── light_monitor.py
│   │   └── screen_brightness.py
│   │
│   ├── ui/              # User interface
│   │   ├── main_window.py
│   │   └── system_tray.py
│   │
│   └── utils/           # Utilities
│       ├── config_manager.py
│       ├── theme_manager.py
│       └── audio_player.py
│
├── tests/               # Unit tests
└── docs/               # Documentation
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI
- [OpenRouter](https://openrouter.ai/) for AI API access
- [OpenCV](https://opencv.org/) for camera integration
- The open-source community

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yocho1/EyeCare-AI-Agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yocho1/EyeCare-AI-Agent/discussions)
- **Email**: support@eyecareai.com

## 🗺️ Roadmap

- [ ] Mobile companion app
- [ ] Cloud sync
- [ ] Team/Enterprise features
- [ ] Browser extension
- [ ] Posture detection
- [ ] Blue light analysis
- [ ] Custom notification sounds
- [ ] Multi-monitor support
- [ ] Voice commands

---

<div align="center">

**Made with ❤️ for healthier eyes**

[⭐ Star us on GitHub](https://github.com/yocho1/EyeCare-AI-Agent) | [🐛 Report Bug](https://github.com/yocho1/EyeCare-AI-Agent/issues) | [💡 Request Feature](https://github.com/yocho1/EyeCare-AI-Agent/issues)

</div>
