from typing import *
from dataclasses import dataclass
from dataclasses import field

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

    def validate(self) -> bool:

        return False

    #@property
    #def leaf(self) -> bool:
    #    return not self.left and not self.right 

    def swap_v_successor(self, node: Self) -> Self:
        if not self.left:
            print(f"swap:{self}")
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

    def rotate_right2(self) -> Self:
        # p(d(e,c),v)
        # d(e,p(c,v))
        v = self
        p = v.parent
        d = p.left
        e = d.left
        c = d.right

        if p.parent:
            if p.is_left_child():
                p.parent.left = d
                p.parent.left.parent = p.parent
            else:
                p.parent.right = d
                p.parent.right.parent = p.parent
        else:
            d.parent = None
        d.left = e
        d.left.parent = d
        d.right = p
        d.right.parent = d
        p.left = c
        p.left.parent = p
        p.right = v
        p.right.parent = p
        return d
        

    def rotate_left2(self) -> Self:
        # p(v,d(c,e))
        # d(p(v,c),e)

        v = self
        p = v.parent
        d = p.right
        e = d.right
        c = d.left

        if p.parent:
            if p.is_left_child():
                p.parent.left = d
                p.parent.left.parent = p.parent
            else:
                p.parent.right = d
                p.parent.right.parent = p.parent
        else:
            d.parent = None
        d.right = e
        d.right.parent = d
        d.left = p
        d.left.parent = d
        p.right = c
        p.right.parent = p
        p.left = v
        p.left.parent = p
        return d

    def rotate_left(self) -> Self:
        # l[parent.left]<-p[parent]<-v[self]
        # p(c(),a(,v))
        # a(p(c,),v)
        
        v = self
        if v.is_left_child():
            print(f"rotate left case1")
            vp = v.parent
            self.parent.parent.right = v
            self.parent.parent.right.parent = self.parent.parent
            v.right = vp
            v.right.parent = v
            vp.right = None
            vp.left = None

            a = v
            p = a.parent
        else:
            print(f"rotate left case2")
            a = self.parent
            p = self.parent.parent
        
        p.right = None
        p_parent = p.parent
        if p.parent:
            if p.is_left_child():
                p_parent.left = a
                p_parent.left.parent = p_parent
            else:
                p_parent.right = a
                p_parent.right.parent = p_parent
        a.left = p
        a.left.parent = a

        return a

    def rotate_right(self) -> Self:
        # v[self]->p[parent]->r[parent.right]

        v = self
        if v.is_right_child():
            print(f"rotate right case3")
            vp = v.parent
            self.parent.parent.left = v
            self.parent.parent.left.parent = self.parent.parent
            v.left = vp
            v.left.parent = v
            vp.left = None
            vp.right = None

            a = v
            p = a.parent
        else:
            print(f"rotate right case4")
            a = self.parent
            p = self.parent.parent

        p.left = None
        p_parent = p.parent
        if p.parent:
            if p.is_left_child():
                p_parent.left = a
                p_parent.left.parent = p_parent
            else:
                p_parent.right = a
                p_parent.right.parent = p_parent
        a.right = p
        a.right.parent = a

        return a

    def reconstruct(self) -> Optional[Self]:
        if self.parent.rb_type == Node.RED:
            print(f"re {self.parent} {self.parent.parent} {self.parent.parent.right}")
            if self.parent.is_left_child():
                
                if not self.parent.parent.right or self.parent.parent.right.rb_type == Node.BLACK:
                    print('case1')

                    pparent = self.parent.parent
                    ppp = pparent.parent
                    p = self.rotate_right()
                    p.right.rb_type = Node.RED
                    #pparent.left = p
                    #pparent.left.parent = pparent
                    p.rb_type = Node.BLACK
                    #p.right.rb_type = Node.RED
                    if not ppp:
                        p.parent = None
                        p.rb_type = Node.BLACK
                        return p
                    else:
                        return None
                else:
                    print('case2')
                    self.parent.parent.right.rb_type = Node.BLACK
                    self.parent.parent.left.rb_type = Node.BLACK

                    if self.parent.parent.parent:
                        self.parent.parent.rb_type = Node.RED
                    else:
                        self.parent.parent.rb_type = Node.BLACK
                        return self.parent.parent
                    return self.parent.parent.reconstruct()
            else:
                if not self.parent.parent.left or self.parent.parent.left.rb_type == Node.BLACK:
                    print('case3')
                    pparent = self.parent.parent
                    ppp = pparent.parent
                    #print(f"{pparent}")
                    p = self.rotate_left()
                    p.left.rb_type = Node.RED
                    #pparent.left = p
                    #pparent.left.parent = pparent
                    p.rb_type = Node.BLACK
                    #p.right.rb_type = Node.RED
                    if not ppp:
                        p.parent = None
                        p.rb_type = Node.BLACK
                        return p
                    else:
                        return None
                else:
                    print('case4')
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
        print(f"add to:{self}")
        if self.rb_type == Node.BLACK:
            if v < self.val:
                self.left = Node.new(v, Node.RED)
                self.left.parent = self
            else:
                self.right = Node.new(v, Node.RED)
                self.right.parent = self
            return None
        else:
            if v < self.val:
                self.left = Node.new(v, Node.RED)
                self.left.parent = self
                return self.left.reconstruct()
            else:
                self.right = Node.new(v, Node.RED)
                self.right.parent = self
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
        print(f"left sibling:{self}")
        if self.rb_type == Node.RED:
            node = self.parent
        else:
            node = self
        
        if node.parent.rb_type == Node.BLACK:
            if node.is_left_child():
                return None
            else:
                if node.parent.left.rb_type == Node.BLACK:
                    print("left sibling case2")
                    return node.parent.left
                else:
                    print("left sibling case3")
                    return node.parent.left.right
        else:
            if node.is_left_child():
                if node.parent.is_left_child():
                    return None
                else:
                    if not node.parent.parent.left:
                        return None
                    if node.parent.parent.left.rb_type == Node.BLACK:
                        print("left sibling case5")
                        return node.parent.parent.left
                    else:
                        print("left sibling case6")
                        return node.parent.parent.left.right
            else:
                print("left sibling case7")
                return node.parent.left
            
    def right_sibling_group(self) -> Self:
        print(f"right sibling:{self}")
        if self.rb_type == Node.RED:
            node = self.parent
        else:
            node = self
        
        if node.parent.rb_type == Node.BLACK:
            if node.is_right_child():
                return None
            else:
                if node.parent.right.rb_type == Node.BLACK:
                    print("right sibling case2")
                    return node.parent.right
                else:
                    print("right sibling case3")
                    return node.parent.right.left
        else:
            if node.is_right_child():
                if node.parent.is_right_child():
                    return None
                else:
                    if node.parent.parent.right.rb_type == Node.BLACK:
                        print("right sibling case5")
                        return node.parent.parent.right
                    else:
                        print("right sibling case6")
                        return node.parent.parent.right.left
            else:
                print("right sibling case7")
                return node.parent.right

    def pop_left(self) -> Tuple[T,Self]:

        if self.rb_type == Node.BLACK:
            if self.left:
                if self.left.rb_type == Node.RED:
                    p = self
                    e = p.left
                    c = e.right
                    v = e.val
                    p.left = c
                    if p.left:
                        p.left.parent = p

                    return v,e.left

            if self.right:
                left = self
                v = self.val
                d = self.right
                self.right = None
                if d and d.rb_type == Node.RED:
                    self.val = d.val
                    self.left = d.left
                    if self.left:
                        self.left.parent = self
                    self.right = d.right
                    if self.right:
                        self.right.parent = self
                    d = self
                    if d.left:
                        d.left.rb_type = Node.RED
                    if d.right:
                        d.right.rb_type = Node.RED

                    return v,left.left
        raise Exception()

    def pop_right(self) -> Tuple[T,Self]:
        if self.rb_type == Node.BLACK:
            if self.right:
                if self.right.rb_type == Node.RED:
                    p = self
                    e = p.right
                    c = e.left
                    v = e.val
                    p.right = c
                    if p.right:
                        p.right.parent = p

                    return v,e.right
            if self.left:
                right = self
                v = self.val
                d = self.left
                self.left = None
                if d.rb_type == Node.RED:
                    self.val = d.val
                    self.left = d.left
                    if self.left:
                        self.left.parent = self
                    self.right = d.right
                    if self.right:
                        self.right.parent = self
                    d = self
                    #if self.is_left_child():
                    #    self.parent.right = d
                    #    self.parent.right.parent = self.parent
                    #else:
                    #    self.parent.left = d
                    #    self.parent.left.parent = self.parent
                    #d.rb_type = Node.BLACK
                    if d.left:
                        d.left.rb_type = Node.RED
                    if d.right:
                        d.right.rb_type = Node.RED

                    return v,right.right
        raise Exception()

    def reconstruct_for_delete(self,tree=None) -> Tuple[Self,bool]:
        print("reconst")
        if not self.is_single_node():
            raise Exception()
        else:
            l_s = self.left_sibling_group()
            r_s = self.right_sibling_group()
            print(f'delete {l_s} {self} {r_s}')
            root = None
            
            if r_s and not r_s.is_single_node():
                # case rotate
                print(f'delete case1 {l_s} {r_s}')

                if tree:
                    print('delete case1')
                    tree.print_tree()

                r_v,r_c = r_s.pop_left()
                
                #p_v = r_s.parent.val
                if r_s.parent.rb_type == Node.BLACK:
                    parent = r_s.parent
                elif r_s.parent == self.parent:
                    parent = r_s.parent
                else:
                    parent = r_s.parent.parent
                p_v = parent.val
                print(f'delete case1 self:{self} r_s:{r_s} r_v:{r_v} r_c:{r_c} p:{parent}')
                
                self.rb_type = Node.RED
                if self.is_left_child():
                    self.parent.left = Node.new(p_v, Node.BLACK)
                    self.parent.left.parent = self.parent
                    o_v = self.parent.left
                else:
                    self.parent.right = Node.new(p_v, Node.BLACK)
                    self.parent.right.parent = self.parent
                    o_v = self.parent.right
                o_v.left = self
                o_v.left.parent = o_v
                o_v.right = r_c
                if o_v.right:
                    o_v.right.parent = o_v
                
                parent.val = r_v
                pass
            elif l_s and not l_s.is_single_node():
                # case rotate
                print('delete case2')

                l_v,l_c = l_s.pop_right()
                if l_s.parent.rb_type == Node.BLACK:
                    parent = l_s.parent
                elif l_s.parent == self.parent:
                    parent = l_s.parent
                else:
                    parent = l_s.parent.parent
                p_v = parent.val
                print(f'delete case2 self:{self} l_s:{l_s} l_v:{l_v} l_c:{l_c} p:{l_s.parent}')
                self.rb_type = Node.RED
                if self.is_left_child():
                    self.parent.left = Node.new(p_v, Node.BLACK)
                    self.parent.left.parent = self.parent
                    o_v = self.parent.left
                else:
                    self.parent.right = Node.new(p_v, Node.BLACK)
                    self.parent.right.parent = self.parent
                    o_v = self.parent.right
                #o_v.left = self
                #o_v.left.parent = o_v
                #o_v.right = l_c
                #if o_v.right:
                #    o_v.right.parent = o_v
                o_v.right = self
                o_v.right.parent = o_v
                o_v.left = l_c
                if o_v.left:
                    o_v.left.parent = o_v
                parent.val = l_v
                
                pass
            elif (not l_s or l_s.is_single_node()) and (not r_s or r_s.is_single_node()):
                print(f"delete case3/case4 {self.parent}")
                if not self.parent.is_single_node():
                    print(f"delete case3/case4 step2 l_s:{l_s} self:{self} r_s:{r_s}")
                    # case merge
                    if r_s and r_s.is_single_node():
                        print('delete case3')

                        if self.parent == r_s.parent:
                            print("delete case3.1")

                            self.rb_type = Node.RED
                            r_s.rb_type = Node.RED
                            r_s.parent.rb_type = Node.BLACK
                        elif self.parent.rb_type == Node.BLACK:
                            print("delete case3.2")
                            p = self.rotate_left2()
                            p.rb_type = Node.BLACK
                            p.left.rb_type = Node.BLACK
                            p.left.left.rb_type = Node.RED
                            p.left.right.rb_type = Node.RED

                            if not p.parent:
                                root = p
                                #return p,False
                        elif r_s.parent.rb_type == Node.BLACK:
                            print("delete case3.3")
                            p = r_s.rotate_right2()
                            p.rb_type = Node.BLACK
                            p.right.rb_type = Node.BLACK
                            p.right.left.rb_type = Node.RED
                            p.right.right.rb_type = Node.RED

                            if not p.parent:
                                root = p
                                #return p,False
                        elif self.parent.rb_type == Node.RED and r_s.parent.rb_type == Node.RED:
                            print("delete case3.4")
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
                        print('delete case4')

                        if self.parent == l_s.parent:
                            print("delete case4.1")

                            self.rb_type = Node.RED
                            l_s.rb_type = Node.RED
                            l_s.parent.rb_type = Node.BLACK
                        elif self.parent.rb_type == Node.BLACK:
                            print("delete case4.2")
                            p = self.rotate_right2()
                            
                            p.rb_type = Node.BLACK
                            p.right.rb_type = Node.BLACK
                            p.right.left.rb_type = Node.RED
                            p.right.right.rb_type = Node.RED

                            if not p.parent:
                                root = p
                                #return p,False
                        elif l_s.parent.rb_type == Node.BLACK:
                            print("delete case4.3")
                            p = l_s.rotate_left2()
                            p.rb_type = Node.BLACK
                            p.left.rb_type = Node.BLACK
                            p.left.left.rb_type = Node.RED
                            p.left.right.rb_type = Node.RED
                            
                            if not p.parent:
                                root = p
                                #return p,False
                        elif self.parent.rb_type == Node.RED and l_s.parent.rb_type == Node.RED:
                            print("delete case4.4")
                            v = self
                            p = v.parent.parent
                            d = p.right
                            e = p.left
                            c = l_s

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
                            d.left = e
                            d.left.parent = d
                            e.right = p
                            e.right.parent = e
                            p.left = c
                            p.left.parent = p
                            p.right = v
                            p.right.parent = p

                        pass
                else:
                    print(f'case root {self} {self.parent}')
                    if self.parent.parent:
                        ret,_ = self.parent.reconstruct_for_delete(tree)
                        if tree:
                            print("reconst case root tree:")
                            tree.print_tree()
                        return ret,True
                    else:
                        # case root
                        print(f'root {l_s} {self} {r_s}')
                        
                        root = self.parent
                        if self.is_left_child():
                            root.left.rb_type = Node.RED
                            root.right = r_s
                            root.right.parent = root
                            root.right.rb_type = Node.RED
                        else:
                            root.left = l_s
                            root.left.parent = root
                            root.left.rb_type = Node.RED
                            root.right.rb_type = Node.RED
                        #root.right.parent = root
                        
                        #root.left = l_s
                        #root.left.parent = root
            if tree:
                print("reconst tree:")
                tree.print_tree()
            return root,False

    def is_single_node(self) -> bool:
        if self.rb_type == Node.BLACK:
            if ((not self.left or self.left.rb_type == Node.BLACK) 
                and (not self.right or self.right.rb_type == Node.BLACK)):
                return True
    
        return False

    def _delete(self, v: T):
        if self.is_left_child():
            self.parent.left = None
        else:
            self.parent.right = None
        #return None

    def delete(self, v: T, cnt=0, tree=None):
        print(f"delete at:{self} parent:{self.parent}")
        #if self.rb_type == Node.RED:
        if not self.is_single_node():
            if self.is_left_child():
                if self.right:
                    self.parent.left = self.right
                    self.parent.left.parent = self.parent
                    self.parent.left.rb_type = Node.BLACK
                elif self.left:
                    self.parent.left = self.left
                    self.parent.left.parent = self.parent
                    self.parent.left.rb_type = Node.BLACK
                else:
                    self.parent.left = None
                
            else:
                if self.right:
                    self.parent.right = self.right
                    self.parent.right.parent = self.parent
                    self.parent.right.rb_type = Node.BLACK
                elif self.left:
                    self.parent.right = self.left
                    self.parent.right.parent = self.parent
                    self.parent.right.rb_type = Node.BLACK
                else:
                    self.parent.right = None

            return None
        else:
            if cnt > 5:
                return None
            ret,flag = self.reconstruct_for_delete(tree)
            
            
            self.delete(v, cnt+1)
            if tree:
                print('tree')
                tree.root.print_rec()
                pass
            return ret

    def __repr__(self):
        def f(v):
            if v == Node.BLACK:
                return 'b:'
            else:
                return 'r:'
        return f"{f(self.rb_type)}{self.val}"

    def print_rec(self, d=0):
        #if d > 4:
        #    return
        #ind = f"{d:>3} " + ' ' * d
        #print(ind + f"{self} parent:{self.parent}")
        if not self.left and not self.right:
            ind = f"{d:>3} " + ' ' * d
            print(ind + f"{self} parent:{self.parent}")
            return
        if self.left:
            self.left.print_rec(d+1)
        else:
            ind = f"{d+1:>3} " + ' ' * (d+1)
            print(ind + '-')
        ind = f"{d:>3} " + ' ' * d
        print(ind + f"{self} parent:{self.parent}")
        if self.right:
            self.right.print_rec(d+1)
        else:
            ind = f"{d+1:>3} " + ' ' * (d+1)
            print(ind + '-')


class TreeRB(Generic[T]):

    def __init__(self) -> None:
        self.root = None
        pass

    def search(self, v: T):
        if self.root == None:
            return False
        else:
            cur = self.root
            while cur:
                if cur.val == v:
                    return True
                else:
                    if v < cur.val:
                        cur = cur.left
                    else:
                        cur = cur.right
                
            return False


    def add(self, v: T):
        if self.root == None:
            self.root = Node.new(v, Node.BLACK)
        else:
            if self.search(v):
                return

            cur = self.root
            while True:
                if v < cur.val:
                    if cur.left:
                        cur = cur.left
                    else:
                        ret = cur.add(v)
                        if ret:
                            self.root = ret
                        break
                else:
                    if cur.right:
                        cur = cur.right
                    else:
                        ret = cur.add(v)
                        if ret:
                            self.root = ret
                        break

    def delete(self, v: T):
        if self.root:
            cur = self.root
            while cur:
                if cur.val == v:
                    if cur.right:
                        print('swap case1')
                        cur = cur.right.swap_v_successor(cur)
                    #elif cur.left and not cur.right:
                    #    print('swap case2')
                    #    cur = cur.left.swap_v_successor(cur)
                    elif not cur.left and not cur.right:
                        if cur == self.root:
                            self.root = None
                            break                  
                    # leaf
                    ret = cur.delete(v, 0, self)
                    if ret:
                        self.root = ret
                    break
                #elif not cur.left and not cur.right:
                #    break
                if v < cur.val:
                    cur = cur.left
                else:
                    cur = cur.right
            if not cur:
                print("not found")

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

        vals = []
        n = 20
        size = 1000
        for _ in range(n):
            i = random.randint(1, size)
            add_proc(i)
            vals.append(i)
            t.print_tree()

        for cnt, i in enumerate(vals):
            #if cnt >= 4:
            #    break
            delete_proc(i)
            t.print_tree()
        
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
        #pass
        t.print_tree()

if __name__ == '__main__':
    main()