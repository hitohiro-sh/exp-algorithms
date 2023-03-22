from typing import *
from dataclasses import dataclass
from dataclasses import field

T = TypeVar('T', int, float, str)



@dataclass
class Node(Generic[T]):
    val: T
    childs: List[Self] = field(default_factory=list)
    parent: Optional[Self] = None
    #degree: int = 0
    mark: bool = False


    @property
    def degree(self):
        return len(self.childs)

    def addChild(self, node : Self):
        self.childs.append(node)
        node.parent = self
        #self.degree += 1


    def removeChild(self, node: Self):
        self.childs.remove(node)
        node.parent = None
        #self.degree -= 1


    def removeAllChild(self) -> List[Self]:
        childs = self.childs
        self.childs = []
        for c in childs:
            c.parent = None
        return childs
        

    def print(self, d=0, _p=print):


        ind = f"{d:>3} " + ' ' * d
        _p(f"{ind}{self.val}")
        
        for c in self.childs:
            c.print(d+1, _p)


@dataclass
class FibHeap(Generic[T]):
    min_h: Node[T] = None
    root_list: List[Node[T]] = field(default_factory=list)

    
    def add(self, v: T):
        node = Node(v)
        self.root_list.append(node)
        
        if not self.min_h or self.min_h.val > node.val:
            self.min_h = node


    def pop(self) -> T:
        v = self.min_h
        if v:
            self.root_list.extend(v.removeAllChild())
            self.root_list.remove(v)
            if not self.root_list:
                self.min_h = None
            else:
                self.min_h = self.root_list[-1]
                self.consolidate()
        
        return v


    def consolidate(self) -> T:
        def link(x: Node[T], y: Node[T]):
            #if y in self.root_list:
            #    self.root_list.remove(y)
            x.addChild(y)
            y.mark = False

        nodes = [None] * (len(self.root_list) + 1)

        for x in self.root_list:
            d = x.degree
            while nodes[d]:
                y = nodes[d]
                if x.val > y.val:
                    tmp = x
                    x = y
                    y = tmp
                link(x, y)
                nodes[d] = None
                d += 1
            nodes[x.degree] = x

        self.min_h = None
        self.root_list = []
        for i in range(len(nodes)):
            if nodes[i]:
                self.root_list.append(nodes[i])
                if not self.min_h or nodes[i].val < self.min_h.val:
                    self.min_h = nodes[i]
    
    def decrease_key(self, x: Node[T], k: T):
        self._decrease_key(x, k)

    def delete(self, x: Node[T]):
        self._decrease_key(x, None)
        if x:
            self.root_list.extend(x.removeAllChild())
            self.root_list.remove(x)
            if not self.root_list:
                self.min_h = None
            else:
                self.min_h = self.root_list[-1]
                self.consolidate()

    def _decrease_key(self, x: Node[T], k: Optional[T]):
        def cut(x: Node[T], y: Node[T]):
            y.removeChild(x)
            self.root_list.append(x)
            x.mark = False

        def cascading_cut(y: Node[T]):
            z = y.parent
            if z:
                if not y.mark:
                    y.mark = True
                else:
                    cut(y, z)
                    cascading_cut(z)
        if k != None:
            if k > x.val:
                raise Exception()
            x.val = k
        
            y = x.parent
            if y and x.val < y.val:
                self.cut(x, y)
                self.cascading_cut(y)
            if x.val < self.min_h.val:
                min_h.val = x
        else:
            y = x.parent
            if y:
                self.cut(x, y)
                self.cascading_cut(y)
            
            
    def print(self):
        print("---")
        for i,root in enumerate(self.root_list):
            print(f"root {i}:")
            root.print()
        pass
        #if self.root:
        #    self.root.print()
        #else:
        #    print('(empty)')


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