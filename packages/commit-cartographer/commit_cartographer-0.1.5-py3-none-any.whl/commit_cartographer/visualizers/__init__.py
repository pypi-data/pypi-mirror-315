from . import mermaid
from . import tree

VISUALIZERS = {
    'mermaid': mermaid.generate_diagram,
    'tree': tree.generate_diagram
}
