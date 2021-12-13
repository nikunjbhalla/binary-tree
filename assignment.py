class bookNode:
    def __init__ (self, bkID, availCount):
        self.bookID = bkID
        self.avCntr = availCount
        self.chkOutCntr = 0
        self.left = None
        self.right = None

    ## Test
    def preorder(self, root):
      res = []
      if root:
         res.append("{} {} {}".format(root.bookID, root.avCntr, root.chkOutCntr))
         res = res + self.preorder(root.left)
         res = res + self.preorder(root.right)
      return res

    ## Test
    def inorder(self, root):
        res = []
        if root:
            res = self.inorder(root.left) 
            res.append(root.bookID)
            res = res + self.inorder(root.right)
        return res


def insert(node, bkID, availCount):   
    q = []  
    q.append(node)  
 
    while (len(q)):  
        node = q[0]  
        q.pop(0)  

        if not node.left: 
            node.left = bookNode(bkID, availCount)  
            break
        else: 
            q.append(node.left)  

        if not node.right: 
            node.right = bookNode(bkID, availCount)
            break
        else: 
            q.append(node.right)
    
def lookup(node, key): 
    if (node == None):
        return False # TODO : handle error for None Node

    if (node.bookID == key): # checking if current node is the searched one
        return node

    leftNode = lookup(node.left, key) # checking if left node is the searched one
    if leftNode:
        return leftNode

    rightNode = lookup(node.right, key)  # checking if right node is the searched one  
    return rightNode

def findMax(node):
    # Base case
    
    if (node == None):
        return False # TODO :  handle condition

    print(node.bookID, node.chkOutCntr, node.left)
    # Return maximum of 3 values:
    # 1) Root's data 
    # 2) Max in Left Subtree
    # 3) Max in right subtree
    if node.left:
        lres = findMax(node.left)
        if (lres.chkOutCntr > node.chkOutCntr):
            res = lres
    if node.right:
        rres = findMax(node.right)
        if (rres.chkOutCntr > node.chkOutCntr):
            res = rres   
    
    return res


class LibraryRecord:

    node = None

    def __init__(self):
        pass

    def _readBookList(self, bkID, availCount): 
        if self.node is None:
            self.node = bookNode(bkID, int(availCount))
        else:
            insert(self.node, bkID, int(availCount))            

    def _chkInChkOut(self, bkID, inOut):
        print('*** {} book : {} ***'.format(inOut, bkID))
        node = lookup(self.node, bkID)
        print('Currently {} has {} books available and is checked out {} times \n'
        .format(node.bookID, node.avCntr, node.chkOutCntr))
        
        if inOut == 'checkOut':
            node.avCntr-=1 # TODO : handle condition for zero available
            node.chkOutCntr+=1
        elif inOut == 'checkIn':
            node.avCntr+=1

    def _getTopBooks(self, bkNode):
        node = findMax(bkNode)
        print(node.bkID, node.avCntr, node.chkOutCntr)
        pass

    def _notIssued(self, bkNode):
        pass

    def _findBook(self, eNode, bkID):
        pass

    def printBooks(self, bkNode):
        pass


if __name__ == '__main__':
    libraryRecords = LibraryRecord()

    with open('inputPS6.txt') as f:
        lines = f.readlines()

        for line in lines:
            bookInfo = line.strip('\n').split(',')
            libraryRecords._readBookList(bookInfo[0],bookInfo[1])

        print(libraryRecords.node.preorder(libraryRecords.node)) # For Test

    with open('promptsPS6.txt') as f:
        lines = f.readlines()
        for line in lines:
            prompt = line.strip('\n').replace(' ','').split(':')

            if prompt[0] == 'checkIn' or prompt[0] == 'checkOut':
                libraryRecords._chkInChkOut(prompt[1], prompt[0])
            elif prompt[0] == 'ListTopBooks':
                libraryRecords._getTopBooks(libraryRecords.node)

    print(libraryRecords.node.inorder(libraryRecords.node)) # For Test
