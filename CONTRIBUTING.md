# Contributing to EyeCare AI Agent

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

1. Check if the bug is already reported in [Issues](https://github.com/yocho1/EyeCare-AI-Agent/issues)
2. If not, create a new issue with:
   - Clear title
   - Detailed description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Environment info (OS, Python version)

### Suggesting Features

1. Check [existing feature requests](https://github.com/yocho1/EyeCare-AI-Agent/issues?q=is%3Aissue+label%3Aenhancement)
2. Create new issue with:
   - Clear use case
   - Expected behavior
   - Why it would be useful
   - Possible implementation ideas

### Code Contributions

1. **Fork the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/EyeCare-AI-Agent.git
   cd EyeCare-AI-Agent
   ```

2. **Create a branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**

   - Follow the code style
   - Add tests if applicable
   - Update documentation

4. **Test your changes**

   ```bash
   python -m pytest tests/
   python main.py  # Manual testing
   ```

5. **Commit your changes**

   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

6. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Fill in the template
   - Link related issues

## Code Style

### Python

- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Keep functions focused and small

### Example

```python
def calculate_eye_strain(screen_time: float, break_compliance: float) -> str:
    """
    Calculate eye strain level based on usage metrics.

    Args:
        screen_time: Hours of screen time
        break_compliance: Percentage of breaks taken (0-100)

    Returns:
        Strain level: "low", "medium", or "high"
    """
    if screen_time > 8 or break_compliance < 50:
        return "high"
    elif screen_time > 6 or break_compliance < 70:
        return "medium"
    return "low"
```

### Commit Messages

Format: `<type>: <description>`

Types:

- `Add`: New feature
- `Fix`: Bug fix
- `Update`: Update existing feature
- `Remove`: Remove code/feature
- `Docs`: Documentation only
- `Refactor`: Code restructuring
- `Test`: Add/update tests
- `Style`: Code style changes

Examples:

- `Add: Webcam-based light detection`
- `Fix: Break timer not resetting after pause`
- `Update: Improve AI prompt templates`
- `Docs: Add installation guide for Linux`

## Project Structure

```
src/
├── core/          # Core business logic
├── ai/            # AI integration
├── hardware/      # Hardware interfaces
├── ui/            # User interface
└── utils/         # Utility functions
```

### Adding New Features

1. **Core Feature**: Add to `src/core/`
2. **AI Feature**: Add to `src/ai/`
3. **UI Feature**: Add to `src/ui/`
4. **Hardware**: Add to `src/hardware/`

### Adding Tests

Create test file: `tests/test_your_feature.py`

```python
import unittest
from src.your_module import YourClass

class TestYourFeature(unittest.TestCase):
    def test_something(self):
        result = YourClass().method()
        self.assertEqual(result, expected_value)
```

## Documentation

### Code Documentation

- Add docstrings to all public functions
- Include type hints
- Add inline comments for complex logic

### User Documentation

- Update README.md for major features
- Add to INSTALLATION.md if setup changes
- Update QUICKSTART.md for user-facing features

## Review Process

1. **Automated Checks** (Future)

   - Code style (black, flake8)
   - Tests pass
   - Type checking (mypy)

2. **Manual Review**

   - Code quality
   - Feature completeness
   - Documentation
   - Testing

3. **Feedback**
   - Address review comments
   - Update PR as needed
   - Discuss if disagreement

## Community Guidelines

### Be Respectful

- Welcoming to all contributors
- Constructive criticism
- Professional communication

### Be Helpful

- Answer questions
- Review PRs
- Share knowledge

### Be Patient

- Maintainers are volunteers
- Reviews take time
- Discussion leads to better code

## Getting Help

- **Questions**: [GitHub Discussions](https://github.com/yocho1/EyeCare-AI-Agent/discussions)
- **Chat**: [Discord Server](#) (Coming soon)
- **Email**: contribute@eyecareai.com

## Recognition

Contributors will be:

- Listed in [Contributors](https://github.com/yocho1/EyeCare-AI-Agent/graphs/contributors)
- Mentioned in release notes
- Added to CONTRIBUTORS.md

## Areas Needing Help

- 🐛 Bug fixes
- 📝 Documentation improvements
- 🌍 Translations (i18n)
- 🎨 UI/UX improvements
- 🧪 Test coverage
- 📱 Mobile app development
- 🔌 Browser extension
- 🎨 Icon/asset design

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making EyeCare AI Agent better! 🙏
