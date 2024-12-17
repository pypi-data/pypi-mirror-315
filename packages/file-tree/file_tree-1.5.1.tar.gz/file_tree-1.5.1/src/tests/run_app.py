"""Run the file-tree app for testing."""
import file_tree

tree = file_tree.FileTree.from_string("""
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

app = file_tree.app.FileTreeViewer(tree)