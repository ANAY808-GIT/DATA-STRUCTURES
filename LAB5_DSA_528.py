import random,time,math,csv
import matplotlib.pyplot as plt

# ---------------- BINARY SEARCH TREE ----------------
class Node:
    def __init__(self,key,name):
        self.key=key
        self.name=name
        self.left=self.right=None

class BST:
    def __init__(self): self.root=None
    def insert(self,key,name):
        new=Node(key,name)
        if not self.root:
            self.root=new
            return
        cur=self.root
        while True:
            if key<cur.key:
                if not cur.left:
                    cur.left=new
                    return
                cur=cur.left
            elif key>cur.key:
                if not cur.right:
                    cur.right=new
                    return
                cur=cur.right
            else:
                cur.name=name
                return
    def search(self,key):
        cur=self.root
        count=0
        while cur:
            count+=1
            if key==cur.key: return cur.name,count
            cur=cur.left if key<cur.key else cur.right
        return None,count
    def delete(self,key):
        parent=None
        cur=self.root
        while cur and cur.key!=key:
            parent=cur
            cur=cur.left if key<cur.key else cur.right
        if not cur: return
        if not cur.left or not cur.right:
            child=cur.left or cur.right
            if not parent: self.root=child
            elif parent.left==cur: parent.left=child
            else: parent.right=child
        else:
            p=cur
            s=cur.right
            while s.left: p,s=s,s.left
            cur.key,cur.name=s.key,s.name
            if p.left==s: p.left=s.right
            else: p.right=s.right
    def height(self):
        if not self.root: return 0
        stack=[(self.root,1)]
        result=0
        while stack:
            node,level=stack.pop()
            result=max(result,level)
            if node.left: stack.append((node.left,level+1))
            if node.right: stack.append((node.right,level+1))
        return result
    def inorder(self):
        result,stack=[],[]
        cur=self.root
        while cur or stack:
            while cur:
                stack.append(cur)
                cur=cur.left
            cur=stack.pop()
            result.append(cur.key)
            cur=cur.right
        return result
    def is_bst(self):
        a=self.inorder()
        return all(a[i]<a[i+1] for i in range(len(a)-1))

# ---------------- AVL TREE ----------------
class AVLNode:
    def __init__(self,key,name):
        self.key=key
        self.name=name
        self.left=self.right=None
        self.height=1

class AVL:
    def __init__(self):
        self.root=None
        self.rotations=0
    def h(self,node): return node.height if node else 0
    def balance(self,node): return self.h(node.left)-self.h(node.right)
    def right_rotate(self,y):
        x=y.left
        t=x.right
        x.right=y
        y.left=t
        y.height=1+max(self.h(y.left),self.h(y.right))
        x.height=1+max(self.h(x.left),self.h(x.right))
        self.rotations+=1
        return x
    def left_rotate(self,x):
        y=x.right
        t=y.left
        y.left=x
        x.right=t
        x.height=1+max(self.h(x.left),self.h(x.right))
        y.height=1+max(self.h(y.left),self.h(y.right))
        self.rotations+=1
        return y
    def rebalance(self,node):
        node.height=1+max(self.h(node.left),self.h(node.right))
        b=self.balance(node)
        if b>1 and self.balance(node.left)>=0: return self.right_rotate(node)
        if b<-1 and self.balance(node.right)<=0: return self.left_rotate(node)
        if b>1 and self.balance(node.left)<0:
            node.left=self.left_rotate(node.left)
            return self.right_rotate(node)
        if b<-1 and self.balance(node.right)>0:
            node.right=self.right_rotate(node.right)
            return self.left_rotate(node)
        return node
    def _insert(self,node,key,name):
        if not node: return AVLNode(key,name)
        if key<node.key: node.left=self._insert(node.left,key,name)
        elif key>node.key: node.right=self._insert(node.right,key,name)
        else:
            node.name=name
            return node
        return self.rebalance(node)
    def insert(self,key,name): self.root=self._insert(self.root,key,name)
    def search(self,key):
        cur=self.root
        count=0
        while cur:
            count+=1
            if key==cur.key: return cur.name,count
            cur=cur.left if key<cur.key else cur.right
        return None,count
    def minimum(self,node):
        while node.left: node=node.left
        return node
    def _delete(self,node,key):
        if not node: return None
        if key<node.key: node.left=self._delete(node.left,key)
        elif key>node.key: node.right=self._delete(node.right,key)
        else:
            if not node.left: return node.right
            if not node.right: return node.left
            s=self.minimum(node.right)
            node.key,node.name=s.key,s.name
            node.right=self._delete(node.right,s.key)
        return self.rebalance(node)
    def delete(self,key): self.root=self._delete(self.root,key)
    def height(self): return self.h(self.root)
    def inorder(self):
        result,stack=[],[]
        cur=self.root
        while cur or stack:
            while cur:
                stack.append(cur)
                cur=cur.left
            cur=stack.pop()
            result.append(cur.key)
            cur=cur.right
        return result
    def is_bst(self):
        a=self.inorder()
        return all(a[i]<a[i+1] for i in range(len(a)-1))
    def is_balanced(self):
        def check(node):
            if not node: return True,0
            l,lh=check(node.left)
            r,rh=check(node.right)
            return l and r and abs(lh-rh)<=1,1+max(lh,rh)
        return check(self.root)[0]

# ---------------- RED-BLACK TREE ----------------
# Each node is RED or BLACK. NIL leaves are shared BLACK sentinel nodes.
class RBNode:
    def __init__(self,key=None,name=None,color="BLACK"):
        self.key=key
        self.name=name
        self.color=color
        self.left=self.right=self.parent=None

class RedBlackTree:
    def __init__(self):
        self.NIL=RBNode()
        self.NIL.left=self.NIL.right=self.NIL.parent=self.NIL
        self.root=self.NIL
        self.rotations=0
    # Left rotation preserves BST ordering while changing tree structure.
    def left_rotate(self,x):
        y=x.right
        x.right=y.left
        if y.left!=self.NIL: y.left.parent=x
        y.parent=x.parent
        if x.parent==self.NIL: self.root=y
        elif x==x.parent.left: x.parent.left=y
        else: x.parent.right=y
        y.left=x
        x.parent=y
        self.rotations+=1
    # Right rotation is the mirror operation of left rotation.
    def right_rotate(self,y):
        x=y.left
        y.left=x.right
        if x.right!=self.NIL: x.right.parent=y
        x.parent=y.parent
        if y.parent==self.NIL: self.root=x
        elif y==y.parent.right: y.parent.right=x
        else: y.parent.left=x
        x.right=y
        y.parent=x
        self.rotations+=1
    # Standard BST insertion followed by recolouring/rotations.
    def insert(self,key,name):
        z=RBNode(key,name,"RED")
        z.left=z.right=self.NIL
        parent=self.NIL
        cur=self.root
        while cur!=self.NIL:
            parent=cur
            if key<cur.key: cur=cur.left
            elif key>cur.key: cur=cur.right
            else:
                cur.name=name
                return
        z.parent=parent
        if parent==self.NIL: self.root=z
        elif key<parent.key: parent.left=z
        else: parent.right=z
        self.insert_fixup(z)
    # Restore Red-Black properties after insertion.
    def insert_fixup(self,z):
        while z.parent.color=="RED":
            if z.parent==z.parent.parent.left:
                uncle=z.parent.parent.right
                if uncle.color=="RED":
                    z.parent.color="BLACK"
                    uncle.color="BLACK"
                    z.parent.parent.color="RED"
                    z=z.parent.parent
                else:
                    if z==z.parent.right:
                        z=z.parent
                        self.left_rotate(z)
                    z.parent.color="BLACK"
                    z.parent.parent.color="RED"
                    self.right_rotate(z.parent.parent)
            else:
                uncle=z.parent.parent.left
                if uncle.color=="RED":
                    z.parent.color="BLACK"
                    uncle.color="BLACK"
                    z.parent.parent.color="RED"
                    z=z.parent.parent
                else:
                    if z==z.parent.left:
                        z=z.parent
                        self.right_rotate(z)
                    z.parent.color="BLACK"
                    z.parent.parent.color="RED"
                    self.left_rotate(z.parent.parent)
        self.root.color="BLACK"
        self.root.parent=self.NIL
    # Search returns the patient name and number of comparisons.
    def search(self,key):
        cur=self.root
        count=0
        while cur!=self.NIL:
            count+=1
            if key==cur.key: return cur.name,count
            cur=cur.left if key<cur.key else cur.right
        return None,count
    def minimum(self,node):
        while node.left!=self.NIL: node=node.left
        return node
    # Replace one subtree with another during deletion.
    def transplant(self,u,v):
        if u.parent==self.NIL: self.root=v
        elif u==u.parent.left: u.parent.left=v
        else: u.parent.right=v
        v.parent=u.parent
    # Standard BST deletion followed by colour repair when needed.
    def delete(self,key):
        z=self.root
        while z!=self.NIL and z.key!=key:
            z=z.left if key<z.key else z.right
        if z==self.NIL: return
        y=z
        original_color=y.color
        if z.left==self.NIL:
            x=z.right
            self.transplant(z,z.right)
        elif z.right==self.NIL:
            x=z.left
            self.transplant(z,z.left)
        else:
            y=self.minimum(z.right)
            original_color=y.color
            x=y.right
            if y.parent==z: x.parent=y
            else:
                self.transplant(y,y.right)
                y.right=z.right
                y.right.parent=y
            self.transplant(z,y)
            y.left=z.left
            y.left.parent=y
            y.color=z.color
        if original_color=="BLACK": self.delete_fixup(x)
    # Restore Red-Black properties after deletion.
    def delete_fixup(self,x):
        while x!=self.root and x.color=="BLACK":
            if x==x.parent.left:
                w=x.parent.right
                if w.color=="RED":
                    w.color="BLACK"
                    x.parent.color="RED"
                    self.left_rotate(x.parent)
                    w=x.parent.right
                if w.left.color=="BLACK" and w.right.color=="BLACK":
                    w.color="RED"
                    x=x.parent
                else:
                    if w.right.color=="BLACK":
                        w.left.color="BLACK"
                        w.color="RED"
                        self.right_rotate(w)
                        w=x.parent.right
                    w.color=x.parent.color
                    x.parent.color="BLACK"
                    w.right.color="BLACK"
                    self.left_rotate(x.parent)
                    x=self.root
            else:
                w=x.parent.left
                if w.color=="RED":
                    w.color="BLACK"
                    x.parent.color="RED"
                    self.right_rotate(x.parent)
                    w=x.parent.left
                if w.right.color=="BLACK" and w.left.color=="BLACK":
                    w.color="RED"
                    x=x.parent
                else:
                    if w.left.color=="BLACK":
                        w.right.color="BLACK"
                        w.color="RED"
                        self.left_rotate(w)
                        w=x.parent.left
                    w.color=x.parent.color
                    x.parent.color="BLACK"
                    w.left.color="BLACK"
                    self.right_rotate(x.parent)
                    x=self.root
        x.color="BLACK"
    # Calculate tree height iteratively; NIL leaves are not counted.
    def height(self):
        if self.root==self.NIL: return 0
        stack=[(self.root,1)]
        result=0
        while stack:
            node,level=stack.pop()
            result=max(result,level)
            if node.left!=self.NIL: stack.append((node.left,level+1))
            if node.right!=self.NIL: stack.append((node.right,level+1))
        return result
    def inorder(self):
        result=[]
        stack=[]
        cur=self.root
        while cur!=self.NIL or stack:
            while cur!=self.NIL:
                stack.append(cur)
                cur=cur.left
            cur=stack.pop()
            result.append(cur.key)
            cur=cur.right
        return result
    def is_bst(self):
        a=self.inorder()
        return all(a[i]<a[i+1] for i in range(len(a)-1))
    # Validate root colour, red-parent rule and equal black height.
    def is_valid(self):
        if self.root==self.NIL: return True
        if self.root.color!="BLACK": return False
        def check(node):
            if node==self.NIL: return True,1
            if node.color not in ("RED","BLACK"): return False,0
            if node.color=="RED" and (node.left.color=="RED" or node.right.color=="RED"):
                return False,0
            left_ok,left_black=check(node.left)
            right_ok,right_black=check(node.right)
            valid=left_ok and right_ok and left_black==right_black
            return valid,left_black+(1 if node.color=="BLACK" else 0)
        return check(self.root)[0] and self.is_bst()

# ---------------- SAMPLE DEMONSTRATION ----------------
print("SAMPLE INPUT: 10,20,30,40,50,25")
trees=[BST(),AVL(),RedBlackTree()]
for key in [10,20,30,40,50,25]:
    for tree in trees: tree.insert(key,"Patient_"+str(key))
for tree in trees:
    print(type(tree).__name__,"Root:",tree.root.key,"Height:",tree.height())
    print(type(tree).__name__,"Inorder:",tree.inorder())
print("AVL rotations:",trees[1].rotations)
print("Red-Black rotations:",trees[2].rotations)

# ---------------- DELETION TESTS ----------------
print("\nDELETION TESTS")
for Tree in [BST,AVL,RedBlackTree]:
    tree=Tree()
    for key in [20,10,30,5,15,25,35,27]: tree.insert(key,str(key))
    for key,label in [(5,"leaf"),(25,"one-child"),(30,"two-child")]:
        tree.delete(key)
        print(Tree.__name__,"After",label,"deletion:",tree.inorder())
    assert tree.is_bst()
    if isinstance(tree,AVL): assert tree.is_balanced()
    if isinstance(tree,RedBlackTree): assert tree.is_valid()

# -- WORKLOAD GENERATION --
def workload(n,kind,rng):
    data=list(range(1,n+1))
    if kind=="Random": rng.shuffle(data)
    elif kind=="Nearly sorted":
        for i in range(max(1,int(n*0.05))):
            x,y=rng.randrange(n),rng.randrange(n)
            data[x],data[y]=data[y],data[x]
    return data

# -- PERFORMANCE EXPERIMENTS --
rng=random.Random(42)
sizes=[1000,5000,10000]
datasets=["Sequential","Random","Nearly sorted"]
rows=[]
graph_data=[]
for n in sizes:
    for kind in datasets:
        data=workload(n,kind,rng)
        searches=rng.sample(range(1,n+1),1000)
        deletions=rng.sample(range(1,n+1),n//5)
        results=[]
        # Run the same workload against all three tree types.
        for Tree in [BST,AVL,RedBlackTree]:
            tree=Tree()
            start=time.perf_counter()
            for key in data: tree.insert(key,"Patient_"+str(key))
            insert_time=time.perf_counter()-start
            tree_height=tree.height()
            avg_comparisons=sum(tree.search(k)[1] for k in searches)/len(searches)
            rotations=getattr(tree,"rotations",0)
            for key in deletions: tree.delete(key)
            delete_height=tree.height()
            assert tree.is_bst()
            if isinstance(tree,AVL): assert tree.is_balanced()
            if isinstance(tree,RedBlackTree): assert tree.is_valid()
            results.append((Tree.__name__,tree_height,insert_time,avg_comparisons,rotations,delete_height))
            rows.append([n,kind,Tree.__name__,tree_height,math.floor(math.log2(n)),round(insert_time,6),rotations,round(avg_comparisons,2),delete_height])
        if kind=="Sequential": graph_data.append((n,results[0][1],results[1][1],results[2][1]))
        print("\nN:",n,"| Dataset:",kind)
        for name,height,elapsed,comparisons,rotations,delete_height in results:
            print(name,"Height:",height,"| Time:",round(elapsed,6),"| Comparisons:",round(comparisons,2),"| Rotations:",rotations,"| After deletion:",delete_height)

# -- CSV OUTPUT --
headers=["N","Dataset","Tree","Final Height","Minimum Height","Insertion Time","Rotations","Average Comparisons","Height After Deletion"]
with open("comparison_results_3_trees.csv","w",newline="") as file:
    writer=csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)
print("\nCSV file generated: comparison_results_3_trees.csv")

#-- GRAPH VISUALIZATION ---
x=[v[0] for v in graph_data]
plt.plot(x,[v[1] for v in graph_data],marker="o",label="Plain BST")
plt.plot(x,[v[2] for v in graph_data],marker="o",label="AVL Tree")
plt.plot(x,[v[3] for v in graph_data],marker="o",label="Red-Black Tree")
plt.xlabel("Number of Patient IDs")
plt.ylabel("Tree Height")
plt.title("BST vs AVL vs Red-Black Tree - Sequential Dataset")
plt.legend()
plt.grid()
plt.savefig("three_tree_height_comparison.png")
plt.show()
