# mkdocs_drawio_converter/plugin.py
import os
import subprocess
from pathlib import Path
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

class DrawioConverterPlugin(BasePlugin):
    config_scheme = (
        ('drawio_executable', config_options.Type(str, default='/usr/local/bin/drawio')),
        ('source_dir', config_options.Type(str, default='docs')),
        ('output_dir', config_options.Type(str, default='svg')),
    )

    def on_files(self, files, config):
        """Process Drawio files before MkDocs builds the site."""
        source_dir = Path(self.config['source_dir'])
        output_dir = Path(self.config['output_dir'])
        drawio_executable = self.config['drawio_executable']

        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        # Find all .drawio files
        for drawio_file in source_dir.glob('**/*.drawio'):
            relative_path = drawio_file.relative_to(source_dir)
            output_path = output_dir / relative_path.with_suffix('.svg')

            # Create output subdirectories if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Convert drawio to SVG using drawio CLI
            try:
                subprocess.run([
                    drawio_executable,
                    '--export',
                    str(drawio_file),
                    '--format', 'svg',
                    '--output', str(output_path)
                ], check=True)
                print(f"Converted {drawio_file} to {output_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting {drawio_file}: {e}")
            except FileNotFoundError:
                print(f"drawio executable not found at {drawio_executable}")
                print("Please install draw.io or update the drawio_executable path in mkdocs.yml")

        return files


