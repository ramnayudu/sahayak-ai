# Contributing to Project Sahayak

We welcome contributions to Project Sahayak! This guide will help you get started.

## 🎯 Project Mission

Empowering rural Indian teachers with AI-driven solutions for multi-grade classroom management.

## 🤝 How to Contribute

### Types of Contributions

1. **Code Contributions**
   - Bug fixes
   - New features
   - Performance improvements
   - UI/UX enhancements

2. **Documentation**
   - API documentation
   - User guides
   - Setup instructions
   - Educational content

3. **Testing**
   - Manual testing
   - Automated test writing
   - Bug reporting
   - Performance testing

4. **Educational Content**
   - Prompt engineering
   - Template creation
   - Subject matter expertise
   - Cultural localization

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+
- Git
- Basic understanding of React and FastAPI
- Interest in educational technology

### Setup Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/sahayak-ai.git
   cd sahayak-ai
   ```

2. **Set up frontend**
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   # Configure your environment variables
   npm run dev
   ```

3. **Set up backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Configure your environment variables
   uvicorn main:app --reload
   ```

4. **Set up local AI models (optional)**
   ```bash
   cd models
   chmod +x setup.sh
   ./setup.sh
   ```

## 📝 Development Guidelines

### Code Style

#### Frontend (React/JavaScript)
- Use ESLint and Prettier for code formatting
- Follow React functional component patterns
- Use meaningful component and variable names
- Write JSDoc comments for complex functions

#### Backend (Python)
- Follow PEP 8 style guidelines
- Use Black for code formatting
- Use type hints where possible
- Write docstrings for all functions and classes

### Git Workflow

1. **Create a new branch** for your feature/fix
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** with clear, focused commits
   ```bash
   git add .
   git commit -m "feat: add lesson plan generation for mathematics"
   ```

3. **Push your branch** and create a pull request
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Convention

We use conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test additions or modifications
- `chore:` - Maintenance tasks

Examples:
```
feat: add multi-grade lesson plan generation
fix: resolve Firebase authentication issue
docs: update API documentation for lesson endpoints
style: format code according to PEP 8
```

## 🧪 Testing

### Frontend Testing
```bash
cd frontend
npm run test
npm run test:coverage
```

### Backend Testing
```bash
cd backend
pytest
pytest --cov=. --cov-report=html
```

### Manual Testing
- Test with different grade combinations
- Verify offline mode functionality
- Check responsive design on mobile devices
- Test with limited internet connectivity

## 📚 Educational Context

### Understanding Rural Indian Education

When contributing, keep in mind:

1. **Multi-grade classrooms** - One teacher manages multiple grade levels
2. **Limited resources** - Basic materials, inconsistent internet
3. **Language diversity** - Multiple regional languages
4. **Cultural sensitivity** - Content should be culturally appropriate
5. **Practical constraints** - Solutions must work in real classroom conditions

### Subject Matter Guidelines

- Follow NCF (National Curriculum Framework) guidelines
- Use age-appropriate language and concepts
- Include cultural references relevant to rural India
- Consider resource limitations in activities
- Ensure content is inclusive and accessible

## 🎨 UI/UX Guidelines

### Design Principles

1. **Simplicity** - Clean, uncluttered interfaces
2. **Accessibility** - Works on basic smartphones and tablets
3. **Offline-first** - Core functionality available without internet
4. **Performance** - Fast loading even on slow connections
5. **Localization** - Support for multiple Indian languages

### Component Standards

- Use semantic HTML elements
- Ensure keyboard navigation
- Provide appropriate ARIA labels
- Test with screen readers
- Optimize for touch interfaces

## 🔧 API Development

### RESTful API Guidelines

1. **Consistent naming** - Use noun-based endpoints
2. **HTTP methods** - GET, POST, PUT, DELETE appropriately
3. **Status codes** - Use standard HTTP status codes
4. **Error handling** - Provide clear error messages
5. **Documentation** - Update OpenAPI/Swagger docs

### Data Models

- Use Pydantic models for request/response validation
- Include appropriate field validation
- Provide clear field descriptions
- Handle edge cases gracefully

## 🤖 AI/ML Contributions

### Prompt Engineering

- Test prompts with real educational scenarios
- Consider cultural context in prompt design
- Optimize for both online and offline models
- Include grade-level appropriateness

### Model Integration

- Support multiple AI providers
- Implement graceful fallbacks
- Monitor response quality
- Consider ethical AI principles

## 📖 Documentation

### What to Document

1. **Code changes** - Update relevant documentation
2. **API changes** - Update OpenAPI specifications
3. **New features** - Add user guides and examples
4. **Setup changes** - Update installation instructions

### Documentation Style

- Use clear, simple language
- Include code examples
- Provide step-by-step instructions
- Add screenshots for UI changes

## 🐛 Bug Reports

### How to Report Bugs

1. **Check existing issues** first
2. **Use the bug report template**
3. **Provide detailed reproduction steps**
4. **Include environment information**
5. **Add screenshots or logs if helpful**

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g. iOS, Android, Windows]
- Browser: [e.g. chrome, safari]
- Version: [e.g. 22]

**Additional context**
Any other context about the problem.
```

## 💡 Feature Requests

### Before Submitting

1. **Check roadmap** and existing issues
2. **Consider educational impact**
3. **Think about rural constraints**
4. **Propose implementation approach**

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Educational context**
How would this help rural teachers and students?

**Implementation ideas**
Any ideas on how this could be implemented.
```

## 🎓 Educational Content Guidelines

### Lesson Plan Templates

- Follow structured format
- Include multiple grade levels
- Provide material alternatives
- Consider time constraints
- Add assessment methods

### Cultural Sensitivity

- Use inclusive language
- Respect regional differences
- Avoid cultural stereotypes
- Include diverse examples
- Consider local contexts

## 🌟 Recognition

Contributors will be recognized in:
- README acknowledgments
- Release notes
- Project website
- Conference presentations

## 📞 Getting Help

- **Discord**: Join our community server
- **Email**: sahayak.ai@gmail.com
- **Issues**: GitHub issues for bugs and features
- **Discussions**: GitHub discussions for questions

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Project Sahayak! Together, we can make quality education accessible to every rural classroom in India. 🇮🇳
