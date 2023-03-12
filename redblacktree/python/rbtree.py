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
        if self.leaf:
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
        if self.rb_type == Node.RED:
            node = self.parent
        else:
            node = self
        
        if node.parent.rb_type == Node.BLACK:
            if node.is_left_child():
                return None
            else:
                if node.parent.left == Node.BLACK:
                    return node.parent.left
                else:
                    return node.parent.left.right
        else:
            if node.is_left_child():
                if node.parent.is_left_child():
                    return None
                else:
                    if node.parent.parent.left.rb_type == Node.BLACK:
                        return node.parent.parent.left
                    else:
                        return node.parent.parent.left.right
            else:
                return node.parent.left
            
    def right_sibling_group(self) -> Self:
        if self.rb_type == Node.RED:
            node = self.parent
        else:
            node = self
        
        if node.parent.rb_type == Node.BLACK:
            if node.is_right_child():
                return None
            else:
                if node.parent.right == Node.BLACK:
                    return node.parent.right
                else:
                    return node.parent.right.left
        else:
            if node.is_right_child():
                if node.parent.is_right_child():
                    return None
                else:
                    if node.parent.parent.right.rb_type == Node.BLACK:
                        return node.parent.parent.right
                    else:
                        return node.parent.parent.right.left
            else:
                return node.parent.right

    def pop_left(self) -> Tuple[T,Self]:
        if self.rb_type == Node.BLACK:
            if self.left:
                left = self.left
                v = self.left.val
                self.left = left.right
                return v,left.left
            elif self.right:
                v = self.val
                self.val = self.right.val
                self.left = self.right.left
                self.right = self.right.right
                return v,self.left
            else:
                v = self.val
                if self.is_left_child():
                    self.parent.left = self.right
                else:
                    self.parent.right = self.right
                return v,self.left
        else:
            return self.parent.pop_left()

    def pop_right(self) -> Tuple[T,Self]:
        if self.rb_type == Node.BLACK:
            if self.right:
                right = self.right
                v = self.right.val
                self.right = right.left
                return v,right.right
            elif self.left:
                v = self.val
                self.val = self.left.val
                self.left = self.left.right
                return v,self.right
            else:
                v = self.val
                if self.is_left_child():
                    self.parent.left = None
                else:
                    self.parent.right = None
                return v,self.right
        else:
            return self.parent.pop_right()

    def reconstruct_for_delete(self, v: T) -> Self:
        
        if not self.is_single_node():
            raise Exception()
        else:
            l_s = self.left_sibling_group()
            r_s = self.right_sibling_group()
            
            root = None
            
            if r_s and not r_s.is_single_node():
                # case rotate
                #print('case1')

                r_v,r_c = r_s.pop_left()
                p_v = r_s.parent.val

                v = self.val
                self.val = p_v
                self.right = Node.new(v, Node.RED)
                self.right.parent = self
                r_s.parent.val = r_v
                self.left = r_c
                self.left.parent = self
                
                pass
            elif l_s and not l_s.is_single_node():
                # case rotate
                #print('case2')

                l_v,l_c = l_s.pop_right()
                p_v = l_s.parent.val

                v = self.val
                self.val = p_v
                self.left = Node.new(v, Node.RED)
                self.left.parent = self
                l_s.parent.val = l_v
                self.right = l_c
                self.right.parent = self
                
                pass
            elif (not l_s or l_s.is_single_node()) and (not r_s or r_s.is_single_node()):
                
                if not self.parent.is_single_node():

                    # case merge
                    if r_s and r_s.is_single_node():
                        #print('case3')

                        self.rb_type = Node.RED
                        r_s.rb_type = Node.RED
                        r_s.parent.rb_type = Node.BLACK

                        pass
                    elif l_s and l_s.is_single_node():
                        #print('case4')

                        self.rb_type = Node.RED
                        l_s.rb_type = Node.RED
                        l_s.parent.rb_type = Node.BLACK

                        pass
                else:
                    if self.parent.parent:
                        return self.parent.reconstract_for_delete(v)
                        
                    else:
                        # case root
                        #print('root')
                        
                        root = self.parent
                        
                        root.right = r_s
                        root.right.parent = root
                        
                        root.left = l_s
                        root.left.parent = root
                        return root
            return None

    def is_single_node(self) -> bool:
        if self.rb_type == Node.BLACK:
            if not self.left and not self.right:
                return True
            elif (self.left and self.left.rb_type == Node.BLACK
                  and self.right and self.right.rb_type == Node.BLACK):
                return True
    
        return False


    def delete(self, v: T):
        if self.rb_type == Node.RED:
            if self.is_left_child():
                self.parent.left = None
            else:
                self.parent.right = None
            return None
        else:
            ret = self.reconst_for_delete()
            self.delete(v)
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
        ind = f"{d:>3} " + ' ' * d
        print(ind + f"{self} parent:{self.parent}")
        if not self.left and not self.right:
            return
        if self.left:
            self.left.print_rec(d+1)
        else:
            ind = f"{d+1:>3} " + ' ' * (d+1)
            print(ind + '-')
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
            while True:
                if cur.val == v:
                    if cur.left or cur.right:
                        cur = cur.right.swap_v_successor(cur)
                    elif not cur.left and not cur.right:
                        if cur == self.root:
                            self.root = None
                            break                  
                    # leaf
                    ret = cur.delete(v)
                    if ret:
                        self.root = ret
                    break
                elif not cur.left and not cur.right:
                    break
                if v < cur.val:
                    cur = cur.left
                else:
                    cur = cur.right


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

        for _ in range(20):
            i = random.randint(1, 1000)
            add_proc(i)
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
        pass
        #t.print_tree()

if __name__ == '__main__':
    main()