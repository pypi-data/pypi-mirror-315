import shutil

from file_tree import FileTree
from fsl_pipe import In, Out, Pipeline

from fsl_pipe_gui.all_panes import PipelineSelector
from fsl_pipe_gui.selector_tab import OutputSelector

tree = FileTree.from_string(
    """
    name=a,b
    in
        a.txt
        b.txt
        {name}.txt (inter)
    final (in)
        {name}.txt (final)
    """
)

pipe = Pipeline()


@pipe
def write_value(a: Out):
    with open(a, "w") as f:
        f.write("a")


@pipe
def write_value(b: Out):
    with open(b, "w") as f:
        f.write("b")


@pipe
def copy_file(inter: In, final: Out):
    shutil.copyfile(inter, final)


base = PipelineSelector(pipe, tree)
app = OutputSelector(base)
