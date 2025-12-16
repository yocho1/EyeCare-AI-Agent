"""
EyeCare AI Agent - System Check Script

Run this script to verify your installation and system compatibility.
"""
import sys
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python_version():
    """Check Python version"""
    print("\n🐍 Checking Python version...")
    version = sys.version_info
    
    if version.major == 3 and version.minor >= 11:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Requires 3.11+)")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required = {
        'customtkinter': 'CustomTkinter',
        'PIL': 'Pillow',
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'httpx': 'httpx'
    }
    
    optional = {
        'plyer': 'plyer (notifications)',
        'pystray': 'pystray (system tray)',
        'pygame': 'pygame (audio)',
        'screen_brightness_control': 'screen-brightness-control'
    }
    
    missing_required = []
    missing_optional = []
    
    # Check required
    for module, package in required.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - REQUIRED")
            missing_required.append(package)
    
    # Check optional
    print("\n   Optional dependencies:")
    for module, package in optional.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ⚠️  {package} - optional")
            missing_optional.append(package)
    
    return missing_required, missing_optional

def check_config_files():
    """Check if config files exist"""
    print("\n📄 Checking configuration files...")
    
    files = {
        'config.json': 'Main configuration',
        'requirements.txt': 'Dependencies list',
        '.env.template': 'Environment template'
    }
    
    all_exist = True
    
    for file, desc in files.items():
        path = Path(file)
        if path.exists():
            print(f"   ✅ {file} - {desc}")
        else:
            print(f"   ❌ {file} - {desc} (Missing)")
            all_exist = False
    
    # Check .env (optional)
    env_path = Path('.env')
    if env_path.exists():
        print(f"   ✅ .env - API configuration (found)")
    else:
        print(f"   ⚠️  .env - API configuration (not configured, will use fallback)")
    
    return all_exist

def check_camera():
    """Check if camera is available"""
    print("\n📷 Checking camera access...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                print("   ✅ Camera detected and accessible")
                return True
            else:
                print("   ⚠️  Camera detected but cannot capture")
                return False
        else:
            print("   ⚠️  No camera detected (will use time-based fallback)")
            return False
            
    except ImportError:
        print("   ⚠️  OpenCV not installed (camera features disabled)")
        return False
    except Exception as e:
        print(f"   ⚠️  Camera check failed: {e}")
        return False

def check_directories():
    """Check if required directories exist"""
    print("\n📁 Checking project structure...")
    
    dirs = [
        'src',
        'src/core',
        'src/ai',
        'src/hardware',
        'src/ui',
        'src/utils',
        'tests',
        'docs'
    ]
    
    all_exist = True
    
    for dir_path in dirs:
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ❌ {dir_path}/ (Missing)")
            all_exist = False
    
    return all_exist

def check_api_config():
    """Check API configuration"""
    print("\n🤖 Checking AI configuration...")
    
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if api_key and api_key != 'your_api_key_here':
        print("   ✅ OpenRouter API key configured")
        print(f"   📝 Key: {api_key[:20]}...")
        
        model = os.getenv('OPENROUTER_MODEL', 'meta-llama/llama-3.1-8b-instruct')
        print(f"   📝 Model: {model}")
        return True
    else:
        print("   ⚠️  OpenRouter API key not configured")
        print("   ℹ️  AI features will use rule-based fallback")
        return False

def test_import_main():
    """Test if main modules can be imported"""
    print("\n🔍 Testing module imports...")
    
    sys.path.insert(0, str(Path(__file__).parent / 'src'))
    
    modules = [
        'src.core.agent',
        'src.core.scheduler',
        'src.ai.openrouter_client',
        'src.hardware.camera_manager',
        'src.ui.main_window'
    ]
    
    all_ok = True
    
    for module in modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except Exception as e:
            print(f"   ❌ {module}: {str(e)[:50]}")
            all_ok = False
    
    return all_ok

def main():
    """Run all system checks"""
    
    print("\n")
    print("╔═══════════════════════════════════════════════════════╗")
    print("║        EyeCare AI Agent - System Check               ║")
    print("╚═══════════════════════════════════════════════════════╝")
    
    checks = []
    
    # Run all checks
    checks.append(("Python Version", check_python_version()))
    
    missing_req, missing_opt = check_dependencies()
    checks.append(("Dependencies", len(missing_req) == 0))
    
    checks.append(("Config Files", check_config_files()))
    checks.append(("Project Structure", check_directories()))
    checks.append(("Camera", check_camera()))
    checks.append(("API Config", check_api_config()))
    checks.append(("Module Imports", test_import_main()))
    
    # Summary
    print_header("SUMMARY")
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    for name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {name}")
    
    print(f"\n   Passed: {passed}/{total}")
    
    # Final verdict
    print_header("VERDICT")
    
    if passed == total:
        print("\n   🎉 ALL CHECKS PASSED!")
        print("   ✅ Your system is ready to run EyeCare AI Agent")
        print("\n   Next steps:")
        print("   1. Run: python main.py")
        print("   2. Check the dashboard")
        print("   3. Enjoy healthier eyes! 👁️✨")
        return True
        
    elif passed >= total - 2:
        print("\n   ⚠️  MINOR ISSUES DETECTED")
        print("   ✅ Application will run but some features may be limited")
        
        if missing_req:
            print("\n   📦 Install missing dependencies:")
            print(f"      pip install {' '.join(missing_req)}")
        
        print("\n   You can still run: python main.py")
        return True
        
    else:
        print("\n   ❌ CRITICAL ISSUES DETECTED")
        print("   ⚠️  Application may not run correctly")
        
        if missing_req:
            print("\n   📦 Install required dependencies:")
            print(f"      pip install -r requirements.txt")
        
        print("\n   📖 See INSTALLATION.md for detailed setup instructions")
        return False

if __name__ == "__main__":
    try:
        success = main()
        print("\n")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Check interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error during check: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
