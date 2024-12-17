"""Test the file-tree app."""
from file_tree import FileTree, app

async def test_starts():
    tree = FileTree.from_string("""
a = b, c
idx = 1, 2
idx_link = 3, 4
name = A
&LINK idx, idx_link

input
    data
        a.txt
        z.txt
output
    data
        c.txt (b)
""")
    async with app.FileTreeViewer(tree).run_test() as pilot:
        assert True

def test_snapshot(snap_compare):
    assert snap_compare("run_app.py", press=["space"])

def test_snapshot_move(snap_compare):
    assert snap_compare("run_app.py", press=["space", "down", "down", "space"])