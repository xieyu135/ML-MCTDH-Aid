
import re

import numpy as np

class TreeNode:
    n_children_max = 6
    def __init__(self, val=None, n_children=None,
            child0=None,
            child1=None,
            child2=None,
            child3=None,
            child4=None,
            child5=None,
            level=None,
            leaf_name=None,
            parent=None,
            ind=None):
        self.val = val  # 数据
        self.n_children = n_children
        self.child0 = child0
        self.child1 = child1
        self.child2 = child2
        self.child3 = child3
        self.child4 = child4
        self.child5 = child5
        self.level = level
        self.leaf_name = leaf_name
        self.parent = parent
        self.ind = ind
    def __str__(self):
        if self.n_children:
            return self.__class__.__name__ + f"(ind: {self.ind}, val:{self.val}, children: {[getattr(self, 'child'+str(i)).ind for i in range(self.n_children)]})"
        else:
            return self.__class__.__name__ + f'(ind: {self.ind}, val:{self.val}, mode: {self.leaf_name})'
def parseTree(tree_lines):
    nodes = {}
    node_txts = {}
    for i,line in enumerate(tree_lines):
        line = line.strip()
        level, txt = re.split(r'> *', line)
        level = int(level)
        node = TreeNode(level=level, ind=i)
        # print(node)
        nodes[i] = node
        node_txts[i] = txt
    # for node in nodes.values():
        # print(node)
    n_node = len(nodes)
    for i in range(n_node):
        # print(i)
        node = nodes[i]
        txt = node_txts[i]
        if '[' in txt:
            node.leaf_name = txt
        else:
            i2 = 0
            for i1 in range(i+1, n_node):
                node_i1 = nodes[i1]
                if node_i1.level==node.level+1:
                    name = f'child{i2}'
                    setattr(node, name, node_i1)
                    node_i1.parent = node
                    # print(i, i1)
                    child = getattr(node, name)
                    # print(child.ind)
                    i2+= 1
                    node.n_children = i2
                elif node_i1.level<=node.level:
                    break
    # node = nodes[2]
    # for i in range(node.n_children):
        # name = f'child{i}'
        # child = getattr(node, name)
        # print('ind:', child.ind, 'val:', child.val)
    for i in range(n_node):
        node = nodes[i]
        txt = node_txts[i]
        if node.n_children is not None:
            # print('node:', i, 'n_children', node.n_children, 'child n_basis:', txt)
            n_basis_list = [int(x) for x in txt.split()]
            for i1 in range(node.n_children):
                # print('i1:', i1)
                name = f'child{i1}'
                child = getattr(node, name)
                # print('child.ind:', child.ind)
                child.val = n_basis_list[i1]
    # node = nodes[0]
    # for i in range(node.n_children):
        # name = f'child{i}'
        # child = getattr(node, name)
        # print('ind:', child.ind, 'val:', child.val)
    return nodes
def toTreeLines(nodes):
    n_node = len(nodes)
    tree_lines = [] 
    for i in range(n_node):
        node = nodes[i]
        line = '  '*node.level + f'{node.level}>'
        if node.n_children:
            for i_child in range(node.n_children):
                name = f'child{i_child}'
                child = getattr(node, name)
                line+= f' {child.val}'
        else:
            line+= f' {node.leaf_name}'
        tree_lines.append(line)
    return tree_lines
def calcProduct(vals):
    p = 1
    for val in vals:
        p*= val
    return p
def resetBasis(n0, vals):
    while n0>calcProduct(vals):
        i_min = np.argmin(vals)
        vals[i_min] = vals[i_min] + 1
    return vals
def checkNbasis(nodes):
    # flag = True
    n_node = len(nodes)
    for i in range(n_node):
        node = nodes[i]
        if node.val is None or node.n_children is None:
            continue
        children = []
        vals = []
        for i1 in range(node.n_children):
            name = f'child{i1}'
            child = getattr(node, name)
            children.append(child)
            vals.append(child.val)
        if node.val>calcProduct(vals):
            # flag = False
            vals = resetBasis(node.val, vals)
            for child, val in zip(children, vals):
                child.val = val
    return nodes
def rebuildRightTreeLines(tree_lines):
    nodes = parseTree(tree_lines)
    nodes = checkNbasis(nodes)
    tree_lines = toTreeLines(nodes)
    return tree_lines
def test():
    s = '''0> 2 2
  1> [el]
  1> 4 5
    2> 4 4
      3> 5 5
        4> [1a]
        4> 5 4
          5> [2a]
          5> [3a]
      3> 3 4
        4> 3 4
          5> [4a]
          5> [5a]
        4> 4 5
          5> [6a]
          5> [7a]
    2> 4 5
      3> 3 3
        4> 3 4
          5> [8a]
          5> [9a]
        4> 4 4
          5> [10a]
          5> [11a]
      3> 4 5
        4> 4 5
          5> [16a]
          5> [19a]
        4> 2 2
          5> [20a]
          5> [90a]'''
    lines = s.split('\n')
    nodes = parseTree(lines)
    for node in nodes.values():
        print(node)
    nodes = checkNbasis(nodes)
    tree_lines = toTreeLines(nodes)
    for line in tree_lines:
        print(line)
if __name__=='__main__':
    # node = TreeNode(ind=0)
    # print(node)
    test()

