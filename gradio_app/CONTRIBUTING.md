# 🤝 Contributing to 3D Anime Chatbot

First off, thank you for considering contributing to 3D Anime Chatbot! It's people like you that make this project great.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- ✅ Be respectful and inclusive
- ✅ Accept constructive criticism
- ✅ Focus on what is best for the community
- ✅ Show empathy towards others
- ❌ No harassment or trolling
- ❌ No spam or self-promotion

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of Python and JavaScript
- Familiarity with Gradio (helpful but not required)

### Quick Start

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/gpt-anime.git
   cd gpt-anime/gradio_app
   ```
3. Set up development environment:
   ```bash
   bash setup.sh
   ```

---

## 💡 How to Contribute

### Types of Contributions

We welcome many types of contributions:

#### 🐛 Bug Fixes
Found a bug? Great! Please report it or fix it.

#### ✨ New Features
Have an idea for a new feature? We'd love to hear about it!

#### 📝 Documentation
Improving documentation is always appreciated.

#### 🎨 UI/UX Improvements
Make the interface more beautiful and user-friendly.

#### 🌍 Translations
Help make the chatbot multilingual.

#### 🧪 Testing
Write tests to improve code coverage.

---

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/gpt-anime.git
cd gpt-anime/gradio_app
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 5. Run Development Server

```bash
python app.py
```

Visit http://localhost:7860 to see your changes.

---

## 📏 Coding Standards

### Python Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line Length**: Maximum 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Use double quotes for strings
- **Naming**:
  - Functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`

### JavaScript Code Style

- **Indentation**: 4 spaces
- **Semicolons**: Required
- **Quotes**: Single quotes for strings
- **Naming**:
  - Functions: `camelCase`
  - Constants: `UPPER_CASE`

### Example Python Code

```python
def generate_response(user_input: str) -> str:
    """
    Generate a response based on user input.

    Args:
        user_input: The user's message

    Returns:
        Generated response string
    """
    if not user_input:
        return "Please provide input."

    # Process input
    response = process_input(user_input)

    return response
```

### Example JavaScript Code

```javascript
function updateStatus(text, type = 'ready') {
    const statusElement = document.getElementById('status');

    statusElement.textContent = text;

    if (type === 'speaking') {
        statusElement.classList.add('speaking');
    }
}
```

---

## 🔍 Code Review Process

All submissions require review. We use GitHub pull requests for this purpose.

### What We Look For

- ✅ Code follows style guidelines
- ✅ Tests pass (if applicable)
- ✅ Documentation is updated
- ✅ Commit messages are clear
- ✅ No unnecessary files included

---

## 📤 Submitting Changes

### 1. Commit Your Changes

```bash
git add .
git commit -m "feat: add awesome new feature"
```

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: add voice input support
fix: resolve avatar loading issue on mobile
docs: update installation instructions
style: format code according to PEP 8
```

### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request

1. Go to the original repository
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill in the PR template
5. Submit!

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How did you test this?

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Added tests (if applicable)
```

---

## 🐛 Reporting Bugs

### Before Submitting

1. Check existing issues
2. Try latest version
3. Collect information

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Screenshots**
If applicable

**Environment:**
 - OS: [e.g. Windows 10]
 - Browser: [e.g. Chrome 96]
 - Python Version: [e.g. 3.9]

**Additional Context**
Any other information
```

---

## 💡 Feature Requests

### Before Submitting

1. Check if feature already exists
2. Check if someone else requested it
3. Consider if it fits project scope

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution you'd like**
What you want to happen

**Describe alternatives you've considered**
Other solutions you thought about

**Additional context**
Any other information, mockups, etc.
```

---

## 🎯 Priority Labels

We use labels to prioritize work:

- 🔴 **critical**: Security issues, major bugs
- 🟠 **high**: Important features, significant bugs
- 🟡 **medium**: Nice-to-have features
- 🟢 **low**: Minor improvements, documentation

---

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

### Top Contributors

Special recognition for:
- 10+ merged PRs
- Major feature implementations
- Significant bug fixes
- Excellent documentation

---

## 📞 Getting Help

### Where to Ask

- **General Questions**: GitHub Discussions
- **Bug Reports**: GitHub Issues
- **Security Issues**: Email security@gpt-anime.com
- **Chat**: Join our Discord server

### Response Times

- Security issues: Within 24 hours
- Bugs: Within 3 days
- Features: Within 1 week
- Documentation: Within 1 week

---

## 📚 Additional Resources

- [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Gradio Documentation](https://gradio.app/docs/)
- [Three.js Documentation](https://threejs.org/docs/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

**Happy Coding! 🚀**
