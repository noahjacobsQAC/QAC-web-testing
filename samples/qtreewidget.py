# root = self.treeview.model().invisibleRootItem()
# for item in self.iterItems(root):
#     print(item.text())

# recursive solution
def iterItems(self, root):
    def recurse(parent):
        for row in range(parent.rowCount()):
            for column in range(parent.columnCount()):
                child = parent.child(row, column)
                yield child
                if child.hasChildren():
                    yield from recurse(child)
    if root is not None:
        yield from recurse(root)

# recursive solution
def iterItems(self, root):
    def recurse(parent):
        if root is not None:
            for row in range(parent.rowCount()):
                for column in range(parent.columnCount()):
                    child = parent.child(row, column)
                    yield child
                    if child.hasChildren():
                        for item in recurse(child):
                            yield item
    return recurse(root)

# iterative solution
def iterItems(self, root):
    if root is not None:
        stack = [root]
        while stack:
            parent = stack.pop(0)
            for row in range(parent.rowCount()):
                for column in range(parent.columnCount()):
                    child = parent.child(row, column)
                    yield child
                    if child.hasChildren():
                        stack.append(child)

# ### FILL ###
def fill_item(item, value):

    def new_item(parent, text, val=None):
        child = QTreeWidgetItem([text])
        fill_item(child, val)
        parent.addChild(child)
        child.setExpanded(True)

    if value is None: return

    elif isinstance(value, dict):
        for key, val in sorted(value.items()):
            new_item(item, str(key), val)

    elif isinstance(value, (list, tuple)):
        for val in value:
            text = (str(val) if not isinstance(val, (dict, list, tuple))
                    else '[%s]' % type(val).__name__)
            new_item(item, text, val)
    else:
        new_item(item, str(value))