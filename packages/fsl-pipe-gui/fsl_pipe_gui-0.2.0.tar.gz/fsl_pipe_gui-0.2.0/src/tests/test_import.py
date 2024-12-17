"""Basic import test."""


def test_import():
    """Just test that importing works."""
    import fsl_pipe_gui

    assert hasattr(fsl_pipe_gui, "run_gui")
