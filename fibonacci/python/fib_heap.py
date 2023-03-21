from typing import *
from dataclasses import dataclass
from dataclasses import field

T = TypeVar('T', int, float, str)

@dataclass
class Node(Generic[T]):
    val: T
    childs: List[Self] = field(default_factory=list)
    parent: Optional[Self] = None
    degree: int = 0
    mark: bool = False

    def addChild(self, node : Self):
        self.childs.append(node)
        node.parent = self

    def print(self, d=0, _p=print):
        ind = f"{d:>3} " + ' ' * d
        _p(f"{ind}{self.val}")
        for c in self.childs:
            c.print(d+1, _p)

@dataclass
class FibHeap:
    min_h: Node = None
    root_list: List[Node] = field(default_factory=list)

    def add(self, v: T):
        #if not self.root:
        #    self.root = Node(v)
        #else:
        #    self._meld(Node(v))
        pass

    def pop(self) -> T:
        #root = self.root
        #val = root.val

        #if not self.root.childs:
        #    self.root = None
        #self.root = root.childs[0]
        #for c in root.childs[1:]:
        #    self._meld(c)

        #return val
        pass
    
    def print(self):
        if self.root:
            self.root.print()
        else:
            print('(empty)')


def main():
    t = FibHeap()

    t.add(10)
    t.print()

    t.add(20)
    t.print()

    t.add(30)
    t.print()

    t.add(40)
    t.print()

    t.pop()
    t.print()

    print('---')
    t = FibHeap()
    t.add(30)
    t.add(40)
    t.print()
    t.add(10)
    t.add(20)
    t.print()
    t.pop()
    t.print()
    t.pop()
    t.print()

    pass

if __name__ == '__main__':
    main()