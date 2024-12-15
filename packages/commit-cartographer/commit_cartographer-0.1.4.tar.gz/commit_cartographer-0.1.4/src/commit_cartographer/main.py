import click
import sys
from commit_cartographer import git_activity
from commit_cartographer.visualizers import VISUALIZERS

@click.command()
@click.option(
    '-p', '--path',
    default='.',
    help='Path to the Git repository (default: current directory)',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True)
)
@click.option(
    '-o', '--output',
    default='git_activity.md',
    help='Output markdown file path (default: git_activity.md)',
    type=click.Path(dir_okay=False, writable=True)
)
@click.option(
    '--max-depth',
    default=4,
    help='Maximum folder depth to display (default: 4)',
    type=int
)
@click.option(
    '--style',
    type=click.Choice(['mermaid', 'tree']),
    default='mermaid',
    help='Output style (default: mermaid)'
)
def main(path, output, max_depth, style):
    """Generate a diagram showing Git repository folder activity."""
    try:
        counts = git_activity.get_folder_commit_counts(path)
        
        with open(output, 'w') as f:
            f.write("# Git Repository Activity Diagram\n\n")
            
            diagram = VISUALIZERS[style](counts)
            
            if style == 'mermaid':
                f.write("```mermaid\n")
                f.write(diagram)
                f.write("\n```\n")
            else:  # tree style
                f.write("```\n")
                f.write(diagram)
                f.write("\n```\n")
            
        click.echo(f"Diagram has been written to {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
