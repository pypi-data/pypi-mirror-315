"""Test snapshots of the two panes."""


def test_selector_pane(snap_compare):
    """Test snapshot of selector pane."""
    assert snap_compare("run_selector_tab.py", press=["space"])


def test_placeholder_pane(snap_compare):
    """Test snapshot of placeholder pane."""
    assert snap_compare("run_placeholder_tab.py")
