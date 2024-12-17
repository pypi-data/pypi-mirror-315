# README.md
# MkDocs Drawio Converter Plugin

A MkDocs plugin that automatically converts Drawio (.drawio) files to SVG format during the build process.

## Installation

```bash
pip install mkdocs-drawio-converter
```

## Requirements

- Draw.io desktop app installed (for the CLI tool)
- MkDocs

## Configuration

Add the following to your `mkdocs.yml`:

```yaml
plugins:
  - drawio-converter:
      drawio_executable: /path/to/drawio  # Path to drawio executable
      source_dir: docs                    # Directory containing .drawio files
      output_dir: svg                     # Directory for output SVG files
```

## Usage

1. Place your .drawio files in your docs directory
2. Build your MkDocs site
3. Reference the converted SVG files in your markdown:

```markdown
![My Diagram](svg/diagram.svg)
```