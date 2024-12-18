# repominify

A Python package that optimizes codebase representations for Large Language Models (LLMs) by generating compact, context-rich summaries that minimize token usage while preserving essential structural information.

[![PyPI version](https://badge.fury.io/py/repominify.svg)](https://badge.fury.io/py/repominify)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI Downloads](https://img.shields.io/pypi/dm/repominify)](https://pypi.org/project/repominify/)
[![Python Versions](https://img.shields.io/pypi/pyversions/repominify)](https://pypi.org/project/repominify/)

## Overview

repominify helps you provide detailed context about your codebase to LLMs without consuming excessive space in their context windows. It processes Repomix output to create optimized representations that maintain critical structural information while significantly reducing token usage. This enables more efficient and effective code-related conversations with AI models by maximizing the amount of useful context that can fit within token limits.

⚠️ Warning: repominify performs deep code analysis which can be resource-intensive for large codebases. Please start with a small subset of your code to understand the process and resource requirements.

## Features

- **Automatic Dependency Management**
  - Checks and installs Node.js and npm dependencies
  - Automatically installs Repomix if not present
  - Handles version compatibility checks

- **Code Analysis**
  - Parses and analyzes code structure
  - Extracts imports, classes, and functions
  - Captures function signatures and docstrings
  - Identifies and extracts constants and environment variables
  - Builds dependency graphs
  - Performance optimized for large codebases

- **Multiple Output Formats**
  - GraphML for visualization tools
  - JSON for web-based tools
  - YAML for statistics
  - Text for human-readable analysis

- **Rich Code Context**
  - Complete function/method signatures
  - Full docstrings with parameter descriptions
  - Constants and their values
  - Environment variables and configurations
  - Module-level documentation
  - Import relationships
  - Class hierarchies and dependencies

- **Size Optimization**
  - Generates minified code structure representation
  - Provides detailed size reduction statistics
  - Shows character and token reduction percentages
  - Maintains semantic meaning while reducing size

- **Security Awareness**
  - Detects potentially sensitive patterns
  - Provides security recommendations
  - Flags suspicious file content
  - Helps maintain security best practices

- **Debug Support**
  - Comprehensive logging
  - Performance tracking
  - Detailed error messages

## Installation

```bash
pip install repominify
```

## Requirements

- Python 3.7 or higher
- Node.js 12+ (will be checked during runtime)
- npm 6+ (will be checked during runtime)
- Repomix (will be installed automatically if not present)

## Usage

### Command Line

```bash
# Basic usage
repominify path/to/repomix-output.txt

# Specify output directory
repominify path/to/repomix-output.txt -o output_dir

# Enable debug logging
repominify path/to/repomix-output.txt --debug
```

### Python API

```python
from repominify import CodeGraphBuilder, ensure_dependencies, configure_logging

# Enable debug logging (optional)
configure_logging(debug=True)

# Check dependencies
if ensure_dependencies():
    # Create graph builder
    builder = CodeGraphBuilder()
    
    # Parse the Repomix output file
    file_entries = builder.parser.parse_file("repomix-output.txt")
    
    # Build the graph
    graph = builder.build_graph(file_entries)
    
    # Save outputs and get comparison
    text_content, comparison = builder.save_graph(
        "output_directory",
        input_file="repomix-output.txt"
    )
    
    # Print comparison
    print(comparison)
```

### Example Output

```
Analysis Complete!
📊 File Stats:
────────────────
  Total Files: 29
  Total Chars: 143,887
 Total Tokens: 14,752
       Output: input.txt
     Security: ✔ No suspicious files detected

📊 File Stats:
────────────────
  Total Files: 29
  Total Chars: 26,254
 Total Tokens: 3,254
       Output: code_graph.txt
     Security: ✔ No suspicious files detected

📈 Comparison:
────────────────
 Char Reduction: 81.8%
Token Reduction: 77.9%
Security Notes: ✔ No issues found
```

## Output Files

When you run repominify, it generates several files in your output directory:

- `code_graph.graphml`: Graph representation in GraphML format
- `code_graph.json`: Graph data in JSON format for web visualization
- `graph_statistics.yaml`: Statistical analysis of the codebase
- `code_graph.txt`: Human-readable text representation including:
  - Module structure and dependencies
  - Function signatures and docstrings
  - Class definitions and hierarchies
  - Constants and their values
  - Environment variables
  - Import relationships

## Project Structure

```
repominify/
├── repominify/         # Source code
│   ├── graph.py        # Graph building and analysis
│   ├── parser.py       # Repomix file parsing
│   ├── types.py        # Core types and data structures
│   ├── exporters.py    # Graph export functionality
│   ├── formatters.py   # Text representation formatting
│   ├── dependencies.py # Dependency management
│   ├── logging.py      # Logging configuration
│   ├── stats.py        # Statistics and comparison
│   ├── constants.py    # Shared constants
│   ├── exceptions.py   # Custom exceptions
│   ├── cli.py         # Command-line interface
│   └── __init__.py    # Package initialization
├── tests/             # Test suite
│   ├── test_end2end.py # End-to-end tests
│   └── data/          # Test data files
├── setup.py          # Package configuration
├── LICENSE           # MIT License
└── README.md         # This file
```

## Code Style

The project follows these coding standards for consistency and maintainability:

- Comprehensive docstrings with Examples sections for all public APIs
- Type hints for all functions, methods, and class attributes
- Custom exceptions for proper error handling and reporting
- Clear separation of concerns between modules
- Consistent code formatting and naming conventions
- Detailed logging with configurable debug support

## Development

To set up for development:

```bash
# Clone the repository
git clone https://github.com/mikewcasale/repominify.git
cd repominify

# Install in development mode with test dependencies
pip install -e '.[dev]'

# Run tests
pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. By contributing to this project, you agree to abide by its terms.

Please ensure your code follows the project's coding standards, including proper docstrings, type hints, and error handling.

## Authors

**Mike Casale**
- Email: mike@casale.xyz
- GitHub: [@mikewcasale](https://github.com/mikewcasale)
- Website: [casale.xyz](https://casale.xyz)

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project makes use of or was influenced by several excellent open source projects:

- [Repomix](https://github.com/yamadashy/repomix) - Our analysis pipeline integrates with this Node.js tool for initial code scanning
- [NetworkX](https://networkx.org/) - Core graph algorithms and data structures
- [PyYAML](https://pyyaml.org/) - YAML file handling
- [GraphRAG Accelerator](https://github.com/Azure-Samples/graphrag-accelerator) - Graph-based code analysis patterns and implementation concepts

## How to Get Help

- For bugs and feature requests, please [open an issue](https://github.com/mikewcasale/repominify/issues)
- For usage questions, please [start a discussion](https://github.com/mikewcasale/repominify/discussions)
- For security concerns, please email security@casale.xyz directly

