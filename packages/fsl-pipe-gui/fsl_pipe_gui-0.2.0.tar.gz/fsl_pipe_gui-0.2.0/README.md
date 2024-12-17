[![PyPI - Downloads](https://img.shields.io/pypi/dm/fsl-pipe-gui)](https://pypi.org/project/fsl-pipe-gui/)
[![Documentation](https://img.shields.io/badge/Documentation-fsl--pipe-blue)](https://open.win.ox.ac.uk/pages/ndcn0236/fsl-pipe)
[![Pipeline status](https://git.fmrib.ox.ac.uk/ndcn0236/fsl-pipe-gui/badges/main/pipeline.svg)](https://git.fmrib.ox.ac.uk/ndcn0236/fsl-pipe-gui/-/pipelines/latest)

Terminal-based GUI for fsl-pipe.
It allows interactively choosing which subset of potential output files you want an fsl-pipe pipeline to produce.

# Installation
```shell
pip install fsl-pipe-gui
```

Any bug reports and feature requests are very welcome (see [issue tracker](https://git.fmrib.ox.ac.uk/ndcn0236/fsl-pipe-gui/-/issues)).

# Usage
For any pipelines using the standard command line interface, the GUI will be available using the `-g/--gui` flag.
Some pipelines might have customised this flag. Please check their documentation.

When starting the GUI from your own custom python code, you will need:
- a `file_tree` describing the paths of the input and output files (see [file-tree](https://open.win.ox.ac.uk/pages/ndcn0236/file-tree)).
- a `pipeline` containing the recipes to produce the output from the input files (see [fsl-pipe](https://open.win.ox.ac.uk/pages/ndcn0236/fsl-pipe)).
The GUI can then be started using
```python
pipeline.gui(file_tree)
```

This GUI consists of 3 parts, which will be presented to the user in sequence:
1. An interactive table, where the default values for placeholders (e.g., subject or session id) can be overwritten.
2. A visualisation of the `file_tree` on the left. For the template selected on the left, the matching filenames are shown on the right. If you want the pipeline to produce a specific file, simply click on the row to mark the checkbox. Files without a checkbox cannot be produced by this pipeline. If the checkbox has been replaced by an "M" then the file cannot be produced due to a missing input file. Filenames in blue already exist (but can be produced by the pipeline anyway if it has a checkbox).
3. A summary of which files are requested and which jobs will actually be run. If the user confirms this summary then the pipeline will actually run.
