from typing import *
from dataclasses import dataclass
from dataclasses import field

def _log(msg):
    #print(f"LOG: {msg}")
    pass

T = TypeVar('T', int, float, str)



@dataclass
class Node(Generic[T]):
    RED=False
    BLACK=True

    rb_type: bool
    val: T
    left: Self = None
    right: Self = None
    parent: Optional[Self] = None

    
    @classmethod
    def new(self, v: T, rb_type: bool):
        return Node(rb_type, v)

    @classmethod
    def is_black_null(self, node: Optional[Self]) -> bool:
        return not node or node.rb_type == Node.BLACK

    @classmethod
    def is_black(self, node: Self) -> bool:
        return node.rb_type == Node.BLACK
    
    @classmethod
    def is_red(self, node: Self) -> bool:
        return node.rb_type == Node.RED

    def set_left(self, node: Optional[Self]):
        self.left = node
        if node:
            self.left.parent = self

    def set_right(self, node: Optional[Self]):
        self.right = node
        if node:
            self.right.parent = self

    def validate(self) -> bool:

        return False

    def swap_v_successor(self, node: Self) -> Self:
        if not self.left:
            _log(f"swap:{self}")
            tmp = self.val
            self.val = node.val
            node.val = tmp
            
            return self
        else:
            return self.left.swap_v_successor(node)

    def is_left_child(self) -> bool:
        return self.parent.left == self

    def is_right_child(self) -> bool:
        return self.parent.right == self

    def replace(self, node: Optional[Self]) -> Self:
        if self.is_left_child():
            self.parent.set_left(node)
        else:
            self.parent.set_right(node)
        return node
    
    def rotate_right2(self) -> Self:
        # p(d(e,c),v)
        # d(e,p(c,v))
        v = self
        p = v.parent
        d = p.left
        e = d.left
        c = d.right

        _log(f"rotate_right2 v:{v} p:{p} d:{d} e:{e} c:{c}")

        if p.parent:
            p.replace(d)
        else:
            d.parent = None
        d.set_left(e)
        d.set_right(p)
        p.set_left(c)
        p.set_right(v)

        #d.print_rec()

        return d
        
    def set_type(self, t: bool):
        self.rb_type = t

    def rotate_left2(self) -> Self:
        # p(v,d(c,e))
        # d(p(v,c),e)
        v = self
        p = v.parent
        d = p.right
        e = d.right
        c = d.left

        if p.parent:
            p.replace(d)
        else:
            d.parent = None
        d.set_right(e)
        d.set_left(p)
        p.set_right(c)
        p.set_left(v)

        return d

    def rotate_left(self) -> Self:
        # l[parent.left]<-p[parent]<-v[self]
        v = self
        if v.is_right_child():
            # p(c,a(d,v))
            # a(p(c,d),v)
            
            a = v.parent
            p = a.parent
            c = p.left
            d = a.left
            
            if p.parent:
                p.replace(a)
            else:
                a.parent = None

            
            a.set_left(p)
            p.set_right(d)

            p.set_type(Node.RED)

            return a
        else:
            # p(c,a(v(d,e),f))
            # v(p(c,d),a(e,f))
            v = self
            d = v.left
            e = v.right
            a = v.parent
            f = a.right
            p = a.parent

            if p.parent:
                p.replace(v)
            else:
                v.parent = None
            v.set_right(a)
            v.set_left(p)
            p.set_right(d)
            a.set_left(e)
            
            p.set_type(Node.RED)

            return v

    def rotate_right(self) -> Self:
        # v[self]->p[parent]->r[parent.right]

        v = self
        if v.is_left_child():
            _log('rotate right case1')
            # p(a(v,d),c)
            # a(v,p(d,c))

            v = self
            a = v.parent
            p = a.parent
            c = p.right
            d = a.right
            
            if p.parent:
                p.replace(a)
            else:
                a.parent = None

            
            a.set_right(p)
            p.set_left(d)

            p.set_type(Node.RED)

            return a
        else:
            _log('rotate right case2')
            # p(a(f,v(e,d)),c)
            # v(a(f,e),p(d,c))
            v = self
            d = v.right
            e = v.left
            a = v.parent
            f = a.left
            p = a.parent

            if p.parent:
                p.replace(v)
            else:
                v.parent = None
            v.set_left(a)
            v.set_right(p)
            p.set_left(d)
            a.set_right(e)
            
            p.set_type(Node.RED)

            v.print_rec(_p=_log)

            return v


    def reconstruct(self) -> Optional[Self]:
        if Node.is_red(self.parent):
            _log(f"reconst {self.parent} {self.parent.parent} {self.parent.parent.right}")
            if self.parent.is_left_child():
                
                if Node.is_black_null(self.parent.parent.right):
                    _log('case1')

                    p = self.rotate_right()
                    
                    
                    p.set_type(Node.BLACK)
                    
                    if not p.parent:
                        #p.set_type(Node.BLACK)
                        return p
                    else:
                        return None
                else:
                    _log('case2')
                    self.parent.parent.right.set_type(Node.BLACK)
                    self.parent.parent.left.set_type(Node.BLACK)

                    if self.parent.parent.parent:
                        self.parent.parent.set_type(Node.RED)
                    else:
                        self.parent.parent.set_type(Node.BLACK)
                        return self.parent.parent
                    return self.parent.parent.reconstruct()
            else:
                if Node.is_black_null(self.parent.parent.left):
                #if not self.parent.parent.left or self.parent.parent.left.rb_type == Node.BLACK:
                    _log('case3')

                    p = self.rotate_left()
                    
                    p.set_type(Node.BLACK)
                    
                    if not p.parent:
                        #p.set_type(Node.BLACK)
                        return p
                    else:
                        return None
                else:
                    _log('case4')
                    self.parent.parent.right.rb_type = Node.BLACK
                    self.parent.parent.left.rb_type = Node.BLACK

                    if self.parent.parent.parent:
                        self.parent.parent.rb_type = Node.RED
                    else:
                        self.parent.parent.rb_type = Node.BLACK
                        return self.parent.parent
                    return self.parent.parent.reconstruct()
        else:
            return None
            

    def add(self, v: T) -> Optional[Self]:
        _log(f"add to:{self}")
        if Node.is_black(self):
            if v < self.val:
                self.set_left(Node.new(v, Node.RED))
            else:
                self.set_right(Node.new(v, Node.RED))
            return None
        else:
            if v < self.val:
                self.set_left(Node.new(v, Node.RED))
                return self.left.reconstruct()
            else:
                self.set_right(Node.new(v, Node.RED))
                return self.right.reconstruct()
            
    #def left_sibling(self) -> Self:
    #    try:
    #        pos = self.parent.childs.index(self)
    #    except:
    #        print(self.parent.childs)
    #        raise Exception()
    #
    #
    #    if pos == 0:
    #        return None
    #    else:
    #        return self.parent.childs[pos-1]
    
    #def right_sibling(self) -> Self:
    #    try:
    #        pos = self.parent.childs.index(self)
    #    except:
    #        print(self.parent.childs)
    #        raise Exception()
    #
    #    if pos == len(self.parent.childs)-1:
    #        return None
    #    else:
    #        return self.parent.childs[pos+1]

    def left_sibling_group(self) -> Self:
        _log(f"left sibling:{self}")
        if self.rb_type == Node.RED:
            node = self.parent
        else:
            node = self
        if not node.parent:
            return None
        if Node.is_black(node.parent):
            if node.is_left_child():
                return None
            else:
                if Node.is_black_null(node.parent.left):
                    return node.parent.left
                else:
                    return node.parent.left.right
        else:
            
            if node.is_left_child():
                
                if node.parent.is_right_child():
                    if Node.is_black_null(node.parent.parent.left):
                        return node.parent.parent.left
                    else:
                        return node.parent.parent.left.right
            else:
                return node.parent.left
            
    def right_sibling_group(self) -> Self:
        _log(f"right sibling:{self}")
        if self.rb_type == Node.RED:
            node = self.parent
        else:
            node = self
        if not node.parent:
            return None
        if Node.is_black(node.parent):
            if node.is_right_child():
                return None
            else:
                if Node.is_black_null(node.parent.right):
                    return node.parent.right
                else:
                    return node.parent.right.left
        else:
            # Node.is_red(node.parent)
            if node.is_right_child():
                
                if node.parent.is_left_child():
                    if Node.is_black_null(node.parent.parent.right):
                        return node.parent.parent.right
                    else:
                        return node.parent.parent.right.left
            else:
                return node.parent.right
            
    def pop_left(self) -> Tuple[T,Self]:

        if self.rb_type == Node.BLACK:
            if self.left:
                if self.left.rb_type == Node.RED:
                    p = self
                    e = p.left
                    c = e.right
                    v = e.val
                    p.set_left(c)
                    p.left = c
                    _log(f"pop_left case1 p:{p} e:{e} c:{c} v:{v}")
                    
                    return v,e.left

            if self.right:
                ll = self.left
                v = self.val
                d = self.right
                _log(f"pop_left case2 v:{v} d:{d}")
                self.right = None
                if d and d.rb_type == Node.RED:
                    self.val = d.val
                    self.set_left(d.left)
                    self.set_right(d.right)
                    d = self
                    d.set_type(Node.BLACK)
                    
                    return v,ll
        raise Exception()

    def pop_right(self) -> Tuple[T,Self]:
        if Node.is_black(self):
            if self.right:
                if Node.is_red(self.right):
                    p = self
                    e = p.right
                    c = e.left
                    v = e.val
                    _log(f"pop_right case1 p:{p} e:{e} c:{c} v:{v}")
                    p.set_right(c)
                    
                    return v,e.right
            if self.left:
                rr = self.right
                v = self.val
                d = self.left
                _log(f"pop_right case2 self:{self} v:{v} d:{d}")
                self.left = None
                if Node.is_red(d):
                    self.val = d.val
                    self.set_left(d.left)
                    self.set_right(d.right)
                    d = self
                    d.set_type(Node.BLACK)
                    
                    return v,rr
        raise Exception()

    def reconstruct_for_delete(self) -> Self:
        _log("reconst")
        if not self.is_single_node():
            raise Exception()
        else:
            l_s = self.left_sibling_group()
            r_s = self.right_sibling_group()
            _log(f'delete l_s:{l_s} self:{self} r_s:{r_s}')
            root = None
            
            if r_s and not r_s.is_single_node():
                # case rotate
                _log(f'delete case1 {l_s} {r_s}')

                #if tree:
                #    _log('delete case1 pop left begin')
                #    tree.root.print_rec(_p=_log)

                

                r_v,r_c = r_s.pop_left()

                #if tree:
                #    _log('delete case1 pop left end')
                #    tree.root.print_rec(_p=_log)
                
                
                if Node.is_black(r_s.parent):
                    parent = r_s.parent
                elif r_s.parent == self.parent:
                    parent = r_s.parent
                else:
                    parent = r_s.parent.parent
                p_v = parent.val
                _log(f'delete case1 self:{self} r_s:{r_s} r_v:{r_v} r_c:{r_c} p:{parent}')
                
                self.set_type(Node.RED)
                if self.is_left_child():
                    self.parent.set_left(Node.new(p_v, Node.BLACK))
                    o_v = self.parent.left
                else:
                    self.parent.set_right(Node.new(p_v, Node.BLACK))
                    o_v = self.parent.right
                o_v.set_left(self)
                o_v.set_right(r_c)
                
                parent.val = r_v
                pass
            elif l_s and not l_s.is_single_node():
                # case rotate
                _log('delete case2')

                #if tree:
                #    _log('delete case2')
                #    tree.print_tree(_p=_log)

                l_v,l_c = l_s.pop_right()
                if Node.is_black(l_s.parent):
                    parent = l_s.parent
                elif l_s.parent == self.parent:
                    parent = l_s.parent
                else:
                    parent = l_s.parent.parent
                p_v = parent.val
                _log(f'delete case2 self:{self} l_s:{l_s} l_v:{l_v} l_c:{l_c} p:{l_s.parent}')
                self.set_type(Node.RED)
                if self.is_left_child():
                    self.parent.set_left(Node.new(p_v, Node.BLACK))
                    o_v = self.parent.left
                else:
                    self.parent.set_right(Node.new(p_v, Node.BLACK))
                    o_v = self.parent.right
                
                o_v.set_right(self)
                o_v.set_left(l_c)
                
                parent.val = l_v
                pass
            elif (not l_s or l_s.is_single_node()) and (not r_s or r_s.is_single_node()):
                _log(f"delete case3/case4 {self.parent}")
                if not self.parent:
                    return self,False
                if not self.parent.is_single_node():
                    _log(f"delete case3/case4 step2 l_s:{l_s} self:{self} r_s:{r_s}")
                    # case merge
                    if r_s and r_s.is_single_node():
                        _log('delete case3')

                        if self.parent == r_s.parent:
                            _log("delete case3.1")

                            self.rb_type = Node.RED
                            r_s.rb_type = Node.RED
                            r_s.parent.rb_type = Node.BLACK
                        elif self.parent.rb_type == Node.BLACK:
                            _log("delete case3.2")
                            p = self.rotate_left2()
                            p.rb_type = Node.BLACK
                            p.left.rb_type = Node.BLACK
                            p.left.left.rb_type = Node.RED
                            p.left.right.rb_type = Node.RED

                            if not p.parent:
                                root = p
                                
                        elif r_s.parent.rb_type == Node.BLACK:
                            _log("delete case3.3")
                            p = r_s.rotate_right2()
                            p.rb_type = Node.BLACK
                            p.right.rb_type = Node.BLACK
                            p.right.left.rb_type = Node.RED
                            p.right.right.rb_type = Node.RED

                            if not p.parent:
                                root = p
                                
                        elif self.parent.rb_type == Node.RED and r_s.parent.rb_type == Node.RED:
                            _log("delete case3.4")
                            v = self
                            p = v.parent.parent
                            d = p.left
                            e = p.right
                            c = r_s
                            if p.parent:
                                if p.is_left_child():
                                    p.parent.left = d
                                    p.parent.left.parent = p.parent
                                else:
                                    p.parent.right = d
                                    p.parent.right.parent = p.parent
                            else:
                                d.parent = None
                                root = d
                            
                            d.rb_type = Node.BLACK
                            d.right = e
                            d.right.parent = d
                            e.left = p
                            e.left.parent = e
                            p.right = c
                            p.right.parent = p
                            p.left = v
                            p.left.parent = p
                            c.rb_type = Node.RED
                            v.rb_type = Node.RED

                        pass
                    elif l_s and l_s.is_single_node():
                        _log('delete case4')

                        if self.parent == l_s.parent:
                            _log("delete case4.1")

                            self.rb_type = Node.RED
                            l_s.rb_type = Node.RED
                            l_s.parent.rb_type = Node.BLACK
                        elif self.parent.rb_type == Node.BLACK:
                            _log("delete case4.2")
                            p = self.rotate_right2()
                            
                            p.rb_type = Node.BLACK
                            p.right.rb_type = Node.BLACK
                            p.right.left.rb_type = Node.RED
                            p.right.right.rb_type = Node.RED

                            if not p.parent:
                                root = p
                                
                        elif l_s.parent.rb_type == Node.BLACK:
                            _log("delete case4.3")
                            p = l_s.rotate_left2()
                            p.rb_type = Node.BLACK
                            p.left.rb_type = Node.BLACK
                            p.left.left.rb_type = Node.RED
                            p.left.right.rb_type = Node.RED
                            
                            if not p.parent:
                                root = p
                                
                        elif self.parent.rb_type == Node.RED and l_s.parent.rb_type == Node.RED:
                            _log("delete case4.4")
                            v = self
                            p = v.parent.parent
                            d = p.right
                            e = p.left
                            c = l_s

                            if p.parent:
                                p.replace(d)
                            else:
                                d.parent = None
                                root = d
                            
                            d.set_type(Node.BLACK)
                            d.set_left(e)
                            e.set_right(p)
                            p.set_left(c)
                            p.set_right(v)

                        pass
                else:
                    _log(f'case root {self} {self.parent}')
                    if self.parent.parent:
                        ret = self.parent.reconstruct_for_delete()
                        #if tree:
                        #    _log("reconst case root tree:")
                        #    tree.root.print_rec(_p=_log)
                        return ret
                    else:
                        # case root
                        _log(f'root {l_s} {self} {r_s}')
                        
                        root = self.parent
                        if self.is_left_child():
                            root.left.set_type(Node.RED)
                            root.set_right(r_s)
                            if root.right:
                                root.right.set_type(Node.RED)
                        else:
                            root.set_left(l_s)
                            if root.left:
                                root.left.set_type(Node.RED)
                            root.right.set_type(Node.RED)
                      
            #if tree:
            #    _log("reconst tree:")
            #    tree.print_tree(_p=_log)
            return root

    def is_single_node(self) -> bool:
        if Node.is_black(self):
            if Node.is_black_null(self.left) and Node.is_black_null(self.right):
                return True
        return False

    def delete(self, v: T, cnt=0, tree=None):
        
        _log(f"delete at:{self} parent:{self.parent}")
        
        if not self.is_single_node():
            #b(r,r)
            #b(,r)
            #b(r,)
            if self.parent:
                if Node.is_red(self):
                    self.replace(None)
                else:
                    #b(r,)
                    _log(f"delete call self:{self} parent:{self.parent}")
                    if self.right and self.left:
                        raise Exception()
                    
                    if self.right:
                        self.replace(self.right)
                        self.right.set_type(Node.BLACK)
                    else:
                        self.replace(self.left)
                        self.left.set_type(Node.BLACK)

            else:
                if self.left:
                    self.left.parent = None
                    self.left.set_type(Node.BLACK)
                    
                    return self.left
            return None 
        else:
            ret = self.reconstruct_for_delete()
            
            self.delete(v, cnt+1)
            if tree:
                _log('tree')
                tree.root.print_rec(_p=_log)
                pass
            return ret

    def __repr__(self):
        def f(node):
            if not node:
                return "null"
            if node.rb_type == Node.BLACK:
                return f'b:{node.val}'
            else:
                return f'r:{node.val}'
        return f"{f(self)}"
        #return f"[{f(self)} left:{f(self.left)} right:{f(self.right)}]"

    def print_pre(self, d=0):
        
        ind = f"{d:>3} " + ' ' * d
        print(ind + f"{self} parent:{self.parent}")
        if not self.left and not self.right:
            return
        if self.left:
            self.left.print_pre(d+1)
        else:
            ind = f"{d+1:>3} " + ' ' * (d+1)
            print(ind + '-')
        
        if self.right:
            self.right.print_pre(d+1)
        else:
            ind = f"{d+1:>3} " + ' ' * (d+1)
            print(ind + '-')   

    def print_rec(self, d=0, _p=print):
        
        if not self.left and not self.right:
            ind = f"{d:>3} " + ' ' * d
            _p(ind + f"{self} parent:{self.parent}")
            return
        if self.left:
            self.left.print_rec(d+1,_p=_p)
        else:
            ind = f"{d+1:>3} " + ' ' * (d+1)
            _p(ind + '-')
        ind = f"{d:>3} " + ' ' * d
        _p(ind + f"{self} parent:{self.parent}")
        if self.right:
            self.right.print_rec(d+1,_p=_p)
        else:
            ind = f"{d+1:>3} " + ' ' * (d+1)
            _p(ind + '-')


class TreeRB(Generic[T]):

    def __init__(self) -> None:
        self.root = None
        pass

    def search(self, v: T):        
        cur = self.root

        vi = set()
        while cur:
            vi.add(cur.val)
            if cur.val == v:
                return True
            else:
                if v < cur.val:
                    cur = cur.left
                else:
                    cur = cur.right
                if cur and cur.val in vi:
                    raise Exception()
        return False


    def add(self, v: T):
        if self.root == None:
            self.root = Node.new(v, Node.BLACK)
        else:
            if self.search(v):
                return

            cur = self.root

            def add_proc(cur, v):
                ret = cur.add(v)
                if ret:
                    self.root = ret
            
            while cur:
                if v < cur.val:
                    if not cur.left:
                        add_proc(cur, v)
                        break 
                    cur = cur.left
                else:
                    if not cur.right:
                        add_proc(cur, v)
                        break
                    cur = cur.right

    def delete(self, v: T):
        if self.root:
            cur = self.root
            while cur:
                if cur.val == v:
                    if cur.right:
                        _log('swap case1')
                        cur = cur.right.swap_v_successor(cur)
                    
                    elif not cur.left and not cur.right:
                        if cur == self.root:
                            self.root = None
                            break                  
                    # leaf
                    ret = cur.delete(v, 0, self)
                    if ret:
                        self.root = ret
                    break
                
                if v < cur.val:
                    cur = cur.left
                else:
                    cur = cur.right
            if not cur:
                print("NOT FOUND")

    def print_tree(self, _p=print):
        if self.root:
            _p('tree:')
            self.root.print_rec(_p=_p)
        else:
            _p('(empty)')

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
    t = TreeRB()
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

        
        
        def test(msg, data_gen, vals):
            print(msg)
            for v in vals:
                t = data_gen()
                print(f"=== {msg} begin ===")
                t.print_tree()
                print("===")
                print(f"delete: {v}")
                t.delete(v)
                print(f"=== {msg} result ===")
                t.print_tree()
                print("===")

        def test_data1():
            t = TreeRB()
            t.add(10)
            t.add(20)
            t.add(30)
            return t
        
        def test_data2():
            t = TreeRB()
            t.add(30)
            t.add(20)
            t.add(10)
            return t
        
        test("test1", test_data1, [10,20,30])
        test("test2", test_data2, [10,20,30])

        def test_data3():
            t = TreeRB()
            t.add(10)
            t.add(20)
            t.add(30)
            t.add(40)
            return t
        
        def test_data4():
            t = TreeRB()
            t.add(40)
            t.add(30)
            t.add(20)
            t.add(10)
            return t
        
        def test_data5():
            t = TreeRB()
            t.add(20)
            t.add(10)
            t.add(30)
            t.add(40)
            return t
        
        def test_data6():
            t = TreeRB()
            t.add(10)
            t.add(30)
            t.add(20)
            t.add(40)
            return t
        
        def test_data7():
            t = TreeRB()
            t.add(10)
            t.add(20)
            t.add(40)
            t.add(30)
            return t

        test("test3", test_data3, [10,20,30,40])
        test("test4", test_data4, [10,20,30,40]) 
        test("test5", test_data5, [10,20,30,40]) 
        test("test6", test_data6, [10,20,30,40])
        test("test7", test_data7, [10,20,30,40])

        def test_data8():
            t = TreeRB()
            t.add(10)
            t.add(20)
            t.add(40)
            t.add(30)
            t.delete(40)
            return t
        
        test("test8", test_data8, [10,20,30])

        def test_data9():
            t = TreeRB()
            t.add(20)
            t.add(10)
            t.add(30)
            t.add(40)
            t.add(50)
            t.add(60)
            t.add(70)
            t.add(80)
            t.add(90)
            t.delete(70)
            t.add(100)
            return t

        test("test9", test_data9, [10,20,30,40,50,60,70,80,90,100])

        def test_data10():
            t = TreeRB()
            t.add(20)
            t.add(10)
            t.add(30)
            t.add(40)
            t.add(50)
            t.add(60)
            t.add(70)
            t.add(80)
            t.add(90)
            t.delete(70)
            t.add(100)
            t.delete(10)
            return t

        test("test10", test_data10, [100,10,30,40,50,60,70,80,90,20])

        #return
        t = TreeRB()
        vals = []
        n = 50
        size = 1000
        for cnt in range(n):
            i = random.randint(1, size)
            print(f"cnt:{cnt}")
            add_proc(i)
            if i not in vals:
                vals.append(i)
            t.print_tree()

            for i2 in vals:
                if not t.search(i2 * 10):
                    print(f'SEARCH FAILED {i2 * 10}')
                    raise Exception()

        for cnt, i in enumerate(vals):
            #if cnt >= 7:
            #    break
            print(f"cnt:{cnt}")
            delete_proc(i)
            print(f"=== delete:{i * 10} ===")
            t.print_tree()
            print("===")

            #print(vals)
            for i2 in vals[cnt+1:]:
                if not t.search(i2 * 10):
                    print(f'SEARCH FAILED {i2 * 10}')
                    raise Exception()

        
        return
    

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

    #except:
    finally:
        pass
        #t.print_tree()

if __name__ == '__main__':
    main()