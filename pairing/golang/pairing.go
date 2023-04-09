package main

import (
	"fmt"
	"strings"
)

type ordered interface {
	int
}

type Node[T ordered] struct {
	Val    T
	Childs []*Node[T]
	Parent *Node[T]
}

type PairingHeap[T ordered] struct {
	Root *Node[T]
}

type _P func(format string, args ...any) (n int, e error)

func p(format string, args ...any) {
	// empty
}

func NewNode[T ordered](v T) *Node[T] {
	return &Node[T]{
		Val:    v,
		Childs: []*Node[T]{},
		Parent: nil,
	}
}

func (self *Node[T]) AddChild(node *Node[T]) {
	self.Childs = append(self.Childs, node)
	node.Parent = self
}

func (self *Node[T]) Print(d int, _p _P) {

	_p("%3v %v%v\n", d, strings.Repeat(" ", d), self.Val)
	for _, c := range self.Childs {
		c.Print(d+1, _p)
	}
}

// func (self *PairingHeap[T]) meld(root *Node[T]) {
// 	if self.Root.Val < root.Val {
// 		self.Root.AddChild(root)
// 	} else {
// 		root.AddChild(self.Root)
// 		self.Root = root
// 	}
// }

func meld[T ordered](n1 *Node[T], n2 *Node[T]) *Node[T] {
	if n1.Val < n2.Val {
		n1.AddChild(n2)
		return n1
	} else {
		n2.AddChild(n1)
		return n2
	}
}

func (self *PairingHeap[T]) Add(v T) {
	if self.Root == nil {
		self.Root = NewNode(v)
	} else {
		self.Root = meld(self.Root, NewNode(v))
	}
}

func (self *PairingHeap[T]) Pop() T {
	val := self.Root.Val

	if len(self.Root.Childs) == 0 {
		self.Root = nil
	} else {
		tmp := []*Node[T]{}
		nodes := self.Root.Childs
		for len(nodes) != 1 {
			i := 1
			for ; i < len(nodes); i += 2 {
				tmp = append(tmp, meld(nodes[i-1], nodes[i]))
			}
			if i == len(nodes) {
				tmp = append(tmp, nodes[i-1])
			}
			nodes = tmp
			tmp = []*Node[T]{}
		}

		self.Root = nodes[0]

	}

	return val
}

func (self *PairingHeap[T]) Print() {
	if self.Root != nil {
		self.Root.Print(0, fmt.Printf)
	} else {
		fmt.Printf("(empty)\n")
	}
}

func main() {
	fmt.Println("Run.")

	t := &PairingHeap[int]{}
	t.Add(10)
	t.Print()
	t.Add(20)
	t.Print()

	fmt.Println("---")
	t = &PairingHeap[int]{}
	for i := 0; i < 10; i++ {
		t.Add(10 * (i + 1))
	}
	t.Pop()
	t.Print()
	t.Pop()
	t.Print()
}
