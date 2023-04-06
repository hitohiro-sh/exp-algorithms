from typing import *
from dataclasses import dataclass
from dataclasses import field

T = TypeVar('T', int, float, str, Tuple[Self, ...])


@dataclass
class Node(Generic[T]):
    val: T
    childs: List[Self] = field(default_factory=list)


    def addChild(self, node : Self):
        self.childs.append(node)


    def print(self, d=0, _p=print):
        ind = f"{d:>3} " + ' ' * d
        _p(f"{ind}{self.val}")
        for c in self.childs:
            c.print(d+1, _p)


@dataclass
class PairingHeap(Generic[T]):
    root: Node = None

    

    @classmethod
    def meld(self, node1: Node[T], node2: Node[T]) -> Node[T]:
        if node1.val < node2.val:
            node1.addChild(node2)
            return node1
        else:
            node2.addChild(node1)
            return node2
        
    #def _meld(self, root: Node[T]):

        #if self.root.val < root.val:
        #    self.root.addChild(root)
        #else:
        #    root.addChild(self.root)
        #    self.root = root

    def add(self, v: T):
        if not self.root:
            self.root = Node(v)
        else:
            self.root = PairingHeap.meld(self.root, Node(v))
            

    def pop(self) -> T:
        root = self.root
        val = root.val

        if not self.root.childs:
            self.root = None
        else:
            trees = root.childs
            tmp = []

            while len(trees) > 1:
                for i in range(0, len(trees), 2):
                    if i+1 < len(trees):
                        tmp.append(PairingHeap.meld(trees[i], trees[i+1]))
                    else:
                        tmp.append(trees[i])
                trees = tmp
                tmp = []
            self.root = trees[0]
            #self.root = root.childs[0]
            #for c in root.childs[1:]:
            #    self._meld(c)

        return val
    
    def print(self):
        if self.root:
            self.root.print()
        else:
            print('(empty)')


def main():
    t = PairingHeap()

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
    t = PairingHeap()
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

    print('---')
    import random
    random.seed(1)

    t = PairingHeap()
    for _ in range(50):
        i = random.randint(1, 50)
        t.add(i * 10)
        if random.randint(0, 10) < 3:
            print('---')
            t.print()
            t.pop()
            print('--- pop ---')
            t.print()

    pass

if __name__ == '__main__':
    main()
