import sys

numbers = []
index = 0
for i in sys.argv[1:]:
    if i=='A' or i=='R':
        index = sys.argv.index(i)
        break
    else:
        numbers.append(int(i))

print("Initial list:", numbers)

class MinHeap:

    #Class attributes
    def __init__(self, initial):
        self.HeapArray = []
        self.initialArr = initial
    
    #Getting index of the node's parent
    def getparentidx(self, pos):
        if pos==0:
            return 0
        return (pos-1)//2
    
    #Getting index of the node's left child
    def getleftchildidx(self, pos):
        return (2 * pos) + 1
    
    #Getting index of the node's right child
    def getrightchildidx(self, pos):
        return (2*pos) + 2
    
    #Returning true if the node is a leaf, else false
    def isleaf(self, pos):
        if self.getleftchildidx(pos)>=len(self.HeapArray) and self.getrightchildidx(pos)>=len(self.HeapArray):
            return True
        return False
    
    #Swapping two nodes
    def swap(self, idx1, idx2):
        self.HeapArray[idx1], self.HeapArray[idx2] = self.HeapArray[idx2], self.HeapArray[idx1]
    
    #Adding a node to a heap and putting it in the correct place
    def add(self, element):
        self.HeapArray.append(element)
        nodeidx = len(self.HeapArray)-1
        #While the node is less than it's parent, keep on swapping (Heapifying up)
        while self.HeapArray[nodeidx] < self.HeapArray[self.getparentidx(nodeidx)]:
            self.swap(nodeidx, self.getparentidx(nodeidx))
            nodeidx = self.getparentidx(nodeidx)
    
    #Deleting the root and shifting everything to the correct place
    def delete(self):
        deleted = self.HeapArray[0]
        self.swap(0, len(self.HeapArray)-1)
        self.HeapArray.pop(len(self.HeapArray)-1)
        nodeidx = 0
        #Initial switch with the root node and it's two children
        rootlist = [self.HeapArray[nodeidx], self.HeapArray[self.getleftchildidx(nodeidx)], self.HeapArray[self.getrightchildidx(nodeidx)]]
        minimum = rootlist.index(min(rootlist))
        self.swap(0, minimum)
        if minimum==1:
            nodeidx = 1
        else:
            nodeidx = 2
        #While the node is greater than it's child, keep on swapping (heapifying down)
        while self.HeapArray[nodeidx] > (self.HeapArray[self.getleftchildidx(nodeidx)]):
            swapper = self.getleftchildidx(nodeidx)
            if(self.HeapArray[self.getrightchildidx(nodeidx)] < self.HeapArray[self.getleftchildidx(nodeidx)]):
                swapper = self.getrightchildidx(nodeidx)
            self.swap(nodeidx, swapper)
            nodeidx = swapper

            if self.isleaf(nodeidx):
                break
            else:
                continue
            
        return deleted

    #Heapifying all elements of initial list and then printing heap
    def heapify(self):
        for i in self.initialArr:
            self.add(i)
        print("Heapified List:", self.HeapArray)


minHeap = MinHeap(numbers)
minHeap.heapify()

for i in range(index, len(sys.argv)):
    if sys.argv[i]=='A':
        minHeap.add(int(sys.argv[i+1]))
        print("Added " + sys.argv[i+1] + " to the heap: ", minHeap.HeapArray)
    if sys.argv[i]=='R':
        deleted = minHeap.delete()
        print("Popped " + str(deleted) + " from heap: ", minHeap.HeapArray)