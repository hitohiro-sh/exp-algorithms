from typing import *
from dataclasses import dataclass
from dataclasses import field

T = TypeVar('T', int, float, str)

@dataclass
class Node(Generic[T]):
    leaf: bool
    vals: List[T]
    childs: List[Self] = field(default_factory=list)
    parent: Optional[Self] = None


    # vals:   l_v, v, r_v
    # childs: 0,1,    2,3

    @classmethod
    def new(self, v: T, leaf: bool):
        return Node(leaf, [v])

    @classmethod
    def set_parent(self, p, childs):
        for c in childs:
            c.parent = p

    def validate(self) -> bool:
        def f(vs: Set[T], vals: List[T], msg: str =''):
            for v in vals:
                if v in vs:
                    print(f'INVALID: {msg}: {self}')
                    raise Exception()
                vs.add(v)

        if not self.leaf and len(self.vals) + 1 != len(self.childs):
            print(f'INVALID: {self}')
            return False
        if self.leaf and len(self.childs) > 0:
            print(f'INVALID: {self}')
            return False
        try:
            vs = set()
            if self.parent:
                f(vs, self.parent.vals)
            f(vs, self.vals)
            for c in self.childs:
                f(vs, c.vals)
        except:
            return False
            
        return True

    def pos(self, v: T) -> Tuple[int, bool]:
        for i, v2 in enumerate(self.vals):
            if v == v2:
                return i,True
        return -1,False

    def pos_for_add(self, v: T) -> Tuple[int, bool]:
        pos = len(self.vals)
        for i, v2 in enumerate(self.vals):
            if v == v2:
                return i,False
            if v < v2:
                pos = i
                break
        return pos,True

    def swap_v_successor(self, vals: List[T], i:int) -> Self:
        if self.leaf:
            tmp = self.vals[0]
            self.vals[0] = vals[i]
            vals[i] = tmp
            return self
        else:
            return self.childs[0].swap_v_successor(vals, i)

    def add(self, v: T, pos: Optional[int]=None) -> int:
        if not pos:
            pos,_ = self.pos_for_add(v)
        
        if len(self.vals) < 3:    
            self.vals.insert(pos, v)
            root = None
        else:
            if pos in (0,1):
                #print(f"add case1,case2")
            
                l_node = self
                # a
                a = self.vals[0]
                # b,c
                p_v,r_v = self.vals[1:]
                if pos == 0:
                    #print(f"add case1")
                    self.vals = [v, a]
                else:
                    #print(f"add case2")
                    self.vals = [a, v]
                r_node = Node.new(r_v, self.leaf)
                if not self.leaf:
                    childs = self.childs
                    l_node.childs = childs[:2]
                    Node.set_parent(l_node, l_node.childs)
                    r_node.childs = childs[2:]
                    Node.set_parent(r_node, r_node.childs)

                if self.parent:
                    parent = self.parent
                    l_node.parent = parent
                    r_node.parent = parent
                    _,root = parent.add(p_v)
                    i = parent.childs.index(self)
                    parent.childs.insert(i+1, r_node)
                
            #elif pos in (2,3):
            else:
                #print(f"add case3,case4")
                
                r_node = self
                # c
                c_v = self.vals[-1]
                # a,b
                l_v,p_v = self.vals[:2]
                if pos == 2:
                    #print(f"add case3")
                    self.vals = [v, c_v]
                else:
                    #print(f"add case4")
                    self.vals = [c_v, v]
                l_node = Node.new(l_v, self.leaf)
                if not self.leaf:
                    childs = self.childs
                    l_node.childs = childs[:2]
                    Node.set_parent(l_node, l_node.childs)
                    r_node.childs = childs[2:]
                    Node.set_parent(r_node, r_node.childs)
                    
                if self.parent:
                    parent = self.parent
                    l_node.parent = parent
                    r_node.parent = parent
                    _,root = parent.add(p_v)
                    i = parent.childs.index(self)
                    parent.childs.insert(i, l_node)

            if not self.parent:
                # root
                self.parent = Node.new(p_v, False)
                l_node.parent = self.parent
                r_node.parent = self.parent
                self.parent.childs = [l_node, r_node]
                
                root = self.parent
                    
        return pos, root

    def left_sibling(self) -> Self:
        try:
            pos = self.parent.childs.index(self)
        except:
            print(self.parent.childs)
            raise Exception()


        if pos == 0:
            return None
        else:
            return self.parent.childs[pos-1]
    
    def right_sibling(self) -> Self:
        try:
            pos = self.parent.childs.index(self)
        except:
            print(self.parent.childs)
            raise Exception()

        if pos == len(self.parent.childs)-1:
            return None
        else:
            return self.parent.childs[pos+1]

    def reconst_for_delete(self, v: T, call_from_delete: bool = True):
        if len(self.vals) > 1:
            raise Exception()
        else:
            pos,_ = self.pos_for_add(v)
            
            l_s = self.left_sibling()
            r_s = self.right_sibling()
            
            if r_s and len(r_s.vals) > 1:
                # case rotate
                #print('case1')
                r_v = r_s.vals.pop(0)
                r_c = r_s.childs.pop(0)
                i = self.parent.childs.index(self)
                p_v = self.parent.vals[i]
                
                self.vals.append(p_v)
                self.parent.vals[i] = r_v
                r_c.parent = self
                self.childs.append(r_c)
                pass
            elif l_s and len(l_s.vals) > 1:
                # case rotate
                #print('case2')
                l_v = l_s.vals.pop()
                l_c = l_s.childs.pop()
                i = self.parent.childs.index(self)
                p_v = self.parent.vals[i-1]
            
                self.vals.insert(0, p_v)
                self.parent.vals[i-1] = l_v
                l_c.parent = self
                self.childs.insert(0, l_c)
                pass
            elif (not l_s or len(l_s.vals) == 1) and (not r_s or len(r_s.vals) == 1):
                if len(self.parent.vals) > 1:
                    # case merge
                    if r_s and len(r_s.vals) == 1:
                        #print('case3')
                        i = self.parent.childs.index(self)
                        p_v = self.parent.vals[i]
                        r_v = r_s.vals[0]
                        self.parent.childs.remove(r_s)
                        self.parent.vals.remove(p_v)
                        
                        self.vals = [self.vals[0], p_v, r_v]

                        Node.set_parent(self, r_s.childs)
                        self.childs = self.childs + r_s.childs


                    elif l_s and len(l_s.vals) == 1:
                        #print('case4')
                        i = self.parent.childs.index(self)
                        p_v = self.parent.vals[i-1]
                        l_v = l_s.vals[-1]
                        self.parent.childs.remove(l_s)
                        self.parent.vals.remove(p_v)
                        
                        self.vals = [l_v, p_v, self.vals[0]]

                        Node.set_parent(self, l_s.childs)
                        self.childs = l_s.childs + self.childs
                else:
                    if self.parent.parent:
                        self.parent.reconst_for_delete(v, False)
                        
                    else:
                        # case root
                        #print('root')
                        root = self.parent
                        if l_s:
                            r_s = self
                        else:
                            l_s = self
                            root.vals = [l_s.vals[0], root.vals[0], r_s.vals[0]]
                            root.childs = l_s.childs + r_s.childs
                            for c in root.childs:
                                c.parent = root

    def delete(self, v: T):
        if len(self.vals) > 1:
            self.vals.remove(v)
            return
        else:
            
            pos,_ = self.pos(v)
            l_s = self.left_sibling()
            r_s = self.right_sibling()
            if r_s and len(r_s.vals) > 1:
                # case rotate
                #print('delete case1')
                r_v = r_s.vals.pop(0)
                
                i = self.parent.childs.index(self)
                p_v = self.parent.vals[i]
                self.vals[-1] = p_v
                self.parent.vals[i] = r_v
                
                pass
            elif l_s and len(l_s.vals) > 1:
                # case rotate
                #print('delete case2')
                l_v = l_s.vals.pop()
                
                i = self.parent.childs.index(self)
                p_v = self.parent.vals[i-1]
                self.vals[0] = p_v
                self.parent.vals[i-1] = l_v
                
                pass
            elif (not l_s or len(l_s.vals) == 1) and (not r_s or len(r_s.vals) == 1):
                if len(self.parent.vals) > 1:
                    # case merge
                    
                    if r_s and len(r_s.vals) == 1:
                        #print('delete case3')

                        i = self.parent.childs.index(self)
                        p_v = self.parent.vals[i]
                        r_v = r_s.vals[0]
                        self.parent.childs.remove(r_s)
                        self.parent.vals.remove(p_v)
                        self.vals = [p_v,r_v]

                    elif l_s and len(l_s.vals) == 1:
                        #print('delete case4')

                        i = self.parent.childs.index(self)
                        p_v = self.parent.vals[i-1]
                        l_v = l_s.vals[-1]
                        self.parent.childs.remove(l_s)
                        self.parent.vals.remove(p_v)
                        self.vals = [l_v,p_v]
                else:
                    if self.parent.parent:
                        #print('reconst')
                        self.parent.reconst_for_delete(v)
                        self.delete(v)
                    else:
                        # case root
                        #print('delete root')

                        root = self.parent
                        if r_s:
                            root.vals = [root.vals[0], r_s.vals[0]]
                        elif l_s:
                            root.vals = [l_s.vals[0], root.vals[0]]
                        root.leaf = True
                        root.childs = []

    def __repr__(self):
        def f(v):
            if v:
                return 'leaf:'
            else:
                return 'node:'
        return f"{f(self.leaf)}{self.vals}"

    def print_rec(self, d=0):
        ind = f"{d:>3} " + ' ' * d
        print(ind + f"{self} parent:{self.parent}")
        #print(ind + f"{self}")
        if self.childs:
            for c in self.childs:
                c.print_rec(d+1)


class Tree234(Generic[T]):

    def __init__(self) -> None:
        self.root = None
        pass

    def search(self, v: T):
        if self.root == None:
            return False
        else:
            cur = self.root
            while True:
                pos,flag = cur.pos(v)
                if flag:
                    return True
                else:
                    if cur.leaf:
                        return False
                    pos,flag = cur.pos_for_add(v)
                    cur = cur.childs[pos]
            return False


    def add(self, v: T):
        if self.root == None:
            self.root = Node.new(v, True)
        else:
            if self.search(v):
                return

            cur = self.root
            while True:
                pos,flag = cur.pos_for_add(v)
                if not flag:
                    return
                if cur.leaf:
                    _,ret = cur.add(v, pos)
                    if ret:
                        self.root = ret
                    return
                else:
                    cur = cur.childs[pos]

    def delete(self, v: T):
        if self.root:
            cur = self.root
            if cur.leaf:
                pos,flag = cur.pos(v)
                if flag:
                    if self.root == cur:
                        # case root
                        if len(cur.vals) > 1:
                            cur.vals.remove(v)
                        else:
                            self.root = None
                        return

            while True:
                pos,flag = cur.pos(v)
                if flag:
                    if not cur.leaf:
                        cur = cur.childs[pos+1].swap_v_successor(cur.vals, pos)
                        
                    # leaf
                    cur.delete(v)
                    break
                else:
                    if cur.leaf:
                        break
                    pos,flag = cur.pos_for_add(v)
                    cur = cur.childs[pos]


    def print_tree(self):
        if self.root:
            print('tree:')
            self.root.print_rec()
        else:
            print('(empty)')

    def validate(self):
        self.validate_node(self.root)

    def validate_node(self, node: Node):
        if node:
            if not node.validate():
                print("INVALID")
                self.print_tree()
                raise Exception()
            for n in node.childs:
                self.validate_node(n)
                

        

def main():
    import random
    random.seed(1)
    t = Tree234()
    try:
        def add_proc(i):
            print(f"add: {i * 10}")

            t.add(i * 10)
            return
            t.validate()
            if not t.search(i * 10):
                print('SEARCH FAILED')
                raise Exception()
            
        
        def delete_proc(i):
            print(f"delete: {i * 10}")

            t.delete(i * 10)
            return
            t.validate()

        for _ in range(10000):
            i = random.randint(1, 1000)
            add_proc(i)
            #t.print_tree()
        for _ in range(1000):
            i = random.randint(1, 1000)
            delete_proc(i)
        for _ in range(1000):
            i = random.randint(1, 1000)
            add_proc(i)

        for _ in range(1000):
            i = random.randint(1, 100)
            delete_proc(i)

        for _ in range(1000):
            i = random.randint(1, 1000)
            add_proc(i)

        for _ in range(1000):
            i = random.randint(1, 1000)
            delete_proc(i)

    except:
        pass
        #t.print_tree()

if __name__ == '__main__':
    main()