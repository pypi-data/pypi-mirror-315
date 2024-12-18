# Commit Cartographer 🗺️

A Python tool that generates visual representations of Git repository activity by analyzing commit patterns across directories and files.

## Features

- 🔍 **Intelligent Analysis**: Analyzes commit patterns across your repository's structure
- 📊 **Multiple Visualization Styles**: 
  - Mermaid flowcharts with directory relationships
  - ASCII tree view for terminal-friendly output
- 🎨 **Smart Coloring**: Uses color gradients in Mermaid mode to represent commit density
- 🌳 **Configurable Depth**: Supports up to 4 levels of directory nesting
- 📁 **Flexible Output**: Choose between showing only directories or including individual files
- 🚀 **Easy Integration**: Works as a CLI tool or can be imported as a Python package

## Installation

Install from PyPI using pip:

```
pip install commit-cartographer
```

## Usage

### Command Line Interface

The package installs a `cmap` command that you can use directly:

```
# Basic usage (creates mermaid diagram)
cmap

# Specify a repository path
cmap -p /path/to/repo

# Generate a tree view instead of mermaid
cmap --style tree

# Include files in the output (works with both styles)
cmap --verbose

# Customize the output file
cmap -o my-diagram.md
```

### Options

- `-p, --path`: Path to Git repository (default: current directory)
- `-o, --output`: Output file path (default: git_activity.md)
- `--style`: Output style - 'mermaid' or 'tree' (default: mermaid)
- `--max-depth`: Maximum folder depth to display (default: 4)
- `--verbose`: Include files in the diagram (default: directories only)

## Output Examples

### Mermaid Style
```mermaid
flowchart LR
    root_node[/root\]
    style root_node fill:#ffffff,stroke:#333,stroke-width:2px
    root_node --> node_docs[/docs\]
    style node_docs fill:#38c6ff,stroke:#333,stroke-width:2px
    node_docs --> node_docs_about[/about\]
    style node_docs_about fill:#1ce2ff,stroke:#333,stroke-width:2px
    root_node --> node_mkdocs[/mkdocs\]
    style node_mkdocs fill:#ff00ff,stroke:#333,stroke-width:2px
    node_mkdocs --> node_mkdocs_utils[/utils\]
    style node_mkdocs_utils fill:#00ffff,stroke:#333,stroke-width:2px
    node_docs --> node_docs_user-guide[/user-guide\]
    style node_docs_user-guide fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs --> node_mkdocs_themes[/themes\]
    style node_mkdocs_themes fill:#38c6ff,stroke:#333,stroke-width:2px
    node_mkdocs_themes --> node_mkdocs_themes_mkdocs[/mkdocs\]
    style node_mkdocs_themes_mkdocs fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_themes_mkdocs --> node_mkdocs_themes_mkdocs_locales[/locales\]
    style node_mkdocs_themes_mkdocs_locales fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_themes --> node_mkdocs_themes_readthedocs[/readthedocs\]
    style node_mkdocs_themes_readthedocs fill:#1ce2ff,stroke:#333,stroke-width:2px
    node_mkdocs_themes_readthedocs --> node_mkdocs_themes_readthedocs_locales[/locales\]
    style node_mkdocs_themes_readthedocs_locales fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs --> node_mkdocs_config[/config\]
    style node_mkdocs_config fill:#1ce2ff,stroke:#333,stroke-width:2px
    node_mkdocs --> node_mkdocs_tests[/tests\]
    style node_mkdocs_tests fill:#38c6ff,stroke:#333,stroke-width:2px
    node_mkdocs_tests --> node_mkdocs_tests_config[/config\]
    style node_mkdocs_tests_config fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_themes_mkdocs --> node_mkdocs_themes_mkdocs_js[/js\]
    style node_mkdocs_themes_mkdocs_js fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs --> node_mkdocs_templates[/templates\]
    style node_mkdocs_templates fill:#00ffff,stroke:#333,stroke-width:2px
    node_docs --> node_docs_dev-guide[/dev-guide\]
    style node_docs_dev-guide fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs --> node_mkdocs_structure[/structure\]
    style node_mkdocs_structure fill:#00ffff,stroke:#333,stroke-width:2px
    node_docs --> node_docs_css[/css\]
    style node_docs_css fill:#00ffff,stroke:#333,stroke-width:2px
    node_docs --> node_docs_img[/img\]
    style node_docs_img fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_themes_mkdocs --> node_mkdocs_themes_mkdocs_css[/css\]
    style node_mkdocs_themes_mkdocs_css fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_themes_mkdocs --> node_mkdocs_themes_mkdocs_webfonts[/webfonts\]
    style node_mkdocs_themes_mkdocs_webfonts fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_themes_readthedocs --> node_mkdocs_themes_readthedocs_css[/css\]
    style node_mkdocs_themes_readthedocs_css fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_tests --> node_mkdocs_tests_structure[/structure\]
    style node_mkdocs_tests_structure fill:#00ffff,stroke:#333,stroke-width:2px
    root_node --> node_requirements[/requirements\]
    style node_requirements fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs --> node_mkdocs_commands[/commands\]
    style node_mkdocs_commands fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs --> node_mkdocs_livereload[/livereload\]
    style node_mkdocs_livereload fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_tests --> node_mkdocs_tests_utils[/utils\]
    style node_mkdocs_tests_utils fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_themes_readthedocs --> node_mkdocs_themes_readthedocs_js[/js\]
    style node_mkdocs_themes_readthedocs_js fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs --> node_mkdocs_contrib[/contrib\]
    style node_mkdocs_contrib fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_contrib --> node_mkdocs_contrib_search[/search\]
    style node_mkdocs_contrib_search fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_contrib_search --> node_mkdocs_contrib_search_lunr-language[/lunr-language\]
    style node_mkdocs_contrib_search_lunr-language fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_tests --> node_mkdocs_tests_integration[/integration\]
    style node_mkdocs_tests_integration fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_tests_integration --> node_mkdocs_tests_integration_complicated_config[/complicated_config\]
    style node_mkdocs_tests_integration_complicated_config fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_tests_integration --> node_mkdocs_tests_integration_minimal[/minimal\]
    style node_mkdocs_tests_integration_minimal fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_contrib_search --> node_mkdocs_contrib_search_templates[/templates\]
    style node_mkdocs_contrib_search_templates fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_tests_integration --> node_mkdocs_tests_integration_subpages[/subpages\]
    style node_mkdocs_tests_integration_subpages fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_tests_integration --> node_mkdocs_tests_integration_unicode[/unicode\]
    style node_mkdocs_tests_integration_unicode fill:#00ffff,stroke:#333,stroke-width:2px
    root_node --> node_LICENSE[/LICENSE\]
    style node_LICENSE fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_themes_mkdocs --> node_mkdocs_themes_mkdocs_img[/img\]
    style node_mkdocs_themes_mkdocs_img fill:#00ffff,stroke:#333,stroke-width:2px
    node_mkdocs_themes_readthedocs --> node_mkdocs_themes_readthedocs_img[/img\]
    style node_mkdocs_themes_readthedocs_img fill:#00ffff,stroke:#333,stroke-width:2px
    node_docs --> node_docs_CNAME[/CNAME\]
    style node_docs_CNAME fill:#00ffff,stroke:#333,stroke-width:2px
```

### Tree Style
```
root/
└── src/ (15 commits)
    └── utils/ (8 commits)
└── tests/ (5 commits)
```

With `--verbose` flag:
```
root/
└── src/ (15 commits)
    └── utils/ (8 commits)
        └── helpers.py (3 commits)
        └── config.py (2 commits)
    └── main.py (5 commits)
└── tests/ (5 commits)
    └── test_main.py (2 commits)
```

## Use Cases

- Understand which parts of your codebase receive the most attention
- Identify hot spots in your repository that might need refactoring
- Generate documentation about repository structure and activity
- Analyze team focus areas in large projects

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
