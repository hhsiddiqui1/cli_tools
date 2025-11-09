# CLI Tools

A powerful command-line interface (CLI) tool that leverages Google Gemini AI and other integrated tools to streamline development workflows, automate tasks, and enhance productivity.

## Overview

This CLI tool provides an intelligent interface for interacting with various APIs and services, with Google Gemini AI integration for enhanced automation and decision-making capabilities. The tool is designed to be extensible, allowing you to add new integrations and workflows as needed.

## Features

- 🤖 **Google Gemini AI Integration**: Leverage Google's Gemini AI for intelligent automation and assistance
- 🔧 **Extensible Architecture**: Easy to add new tools and integrations
- 📊 **Monoova Payment Integration**: Built-in support for Monoova payment API workflows
- 🛠️ **Multiple Tool Support**: Integrate with various APIs and services
- 📝 **Comprehensive Documentation**: Detailed documentation and flow diagrams included

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (recommended: Python 3.10 or higher)
- **pip** (Python package manager)
- **Git** (for version control)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/hhsiddiqui1/cli_tools.git
cd cli_tools
```

### 2. Set Up Python Virtual Environment (Recommended)

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

*(Note: If `requirements.txt` doesn't exist yet, create it with the necessary dependencies)*

### 4. Configure API Keys

Create a `.env` file in the root directory to store your API keys:

```bash
# .env file
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
MONOOVA_API_KEY=your_monoova_api_key_here
# Add other API keys as needed
```

**Important**: Never commit your `.env` file to version control. It should be listed in `.gitignore`.

## Usage

### Basic Commands

Once installed, you can use the CLI tool with various commands:

```bash
# Get help and see available commands
python cli_tool.py --help

# Run with Gemini AI assistance
python cli_tool.py --gemini "your query here"

# Execute Monoova integration workflows
python cli_tool.py monoova --action <action_name>

# List all available tools
python cli_tool.py tools --list
```

### Using Google Gemini Integration

The tool integrates with Google Gemini AI to provide intelligent assistance:

```bash
# Ask Gemini a question
python cli_tool.py gemini --query "Analyze the payment flow"

# Generate code or documentation
python cli_tool.py gemini --generate "Create a payment handler function"

# Get recommendations
python cli_tool.py gemini --recommend "Best practices for API integration"
```

### Monoova Integration

Work with Monoova payment APIs:

```bash
# Initialize a payout
python cli_tool.py monoova payout --amount 100.00 --destination <account>

# Verify an account
python cli_tool.py monoova verify --account <account_details>

# Check account balance
python cli_tool.py monoova balance

# View transaction history
python cli_tool.py monoova transactions --limit 10
```

## Project Structure

```
cli_tools/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env                               # Environment variables (not in git)
├── .gitignore                         # Git ignore rules
├── cli_tool.py                        # Main CLI entry point
├── monoova_integration/               # Monoova payment integration
│   ├── GEMINI.md                      # Gemini AI integration docs
│   ├── requirements.md                # Functional requirements
│   ├── analysis.md                    # Technical analysis
│   ├── *.plantuml                     # Flow diagrams
│   └── openapi*.yaml                  # API specifications
└── docs/                              # Additional documentation
```

## Configuration

### Environment Variables

The tool uses environment variables for configuration. Create a `.env` file with:

- `GOOGLE_GEMINI_API_KEY`: Your Google Gemini API key
- `MONOOVA_API_KEY`: Your Monoova API key (if using Monoova features)
- `MONOOVA_ENVIRONMENT`: `sandbox` or `production` (default: `sandbox`)

### Configuration File

You can also create a `config.yaml` file for more advanced configuration:

```yaml
gemini:
  api_key: ${GOOGLE_GEMINI_API_KEY}
  model: gemini-pro
  temperature: 0.7

monoova:
  api_key: ${MONOOVA_API_KEY}
  environment: sandbox
  base_url: https://sand-api.monoova.com
```

## Development

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_cli_tool.py
```

### Adding New Tools

To add a new tool integration:

1. Create a new module in the `tools/` directory
2. Implement the tool interface
3. Register it in the main CLI tool
4. Update the documentation

### Code Style

This project follows PEP 8 style guidelines. Use a linter:

```bash
# Install linting tools
pip install flake8 black

# Format code
black .

# Check code style
flake8 .
```

## Documentation

For detailed documentation on specific features:

- **Monoova Integration**: See `monoova_integration/requirements.md` and `monoova_integration/analysis.md`
- **Gemini AI Usage**: See `monoova_integration/GEMINI.md`
- **API Specifications**: See OpenAPI YAML files in `monoova_integration/`
- **Flow Diagrams**: See PlantUML files (`.plantuml`) in `monoova_integration/`

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError` when running commands
- **Solution**: Ensure you've activated the virtual environment and installed dependencies

**Issue**: API key errors
- **Solution**: Verify your `.env` file exists and contains valid API keys

**Issue**: Connection timeout
- **Solution**: Check your internet connection and API endpoint URLs

### Getting Help

- Check the documentation in the `monoova_integration/` folder
- Review error messages carefully
- Ensure all prerequisites are installed

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security

- **Never commit API keys or secrets** to the repository
- Use environment variables or secure secret management
- Keep dependencies up to date
- Review code changes for security vulnerabilities

## License

This project is open source. Please refer to the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on the [GitHub repository](https://github.com/hhsiddiqui1/cli_tools).

## Acknowledgments

- Google Gemini AI for intelligent automation capabilities
- Monoova for payment API integration
- All contributors and users of this tool

---

**Note**: This tool is under active development. Some features may be experimental or subject to change.

