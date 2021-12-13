class bookNode:
    def __init__ (self, bkID, avail_count):
        self.bookID = bkID
        self.avCntr = avail_count
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


def insert(node, bkID, avail_count):   
    q = []  
    q.append(node)  
 
    while len(q):
        node = q[0]  
        q.pop(0)  

        if not node.left: 
            node.left = bookNode(bkID, avail_count)  
            break
        else: 
            q.append(node.left)  

        if not node.right: 
            node.right = bookNode(bkID, avail_count)
            break
        else: 
            q.append(node.right)


def lookup(node, key): 
    if node is None:
        return False # TODO : handle error for None Node

    if node.bookID is key: # checking if current node is the searched one
        return node

    left_node = lookup(node.left, key) # checking if left node is the searched one
    if left_node:
        return left_node

    right_node = lookup(node.right, key)  # checking if right node is the searched one
    return right_node


def findMax(node):
    pass


class LibraryRecord:

    node = None

    def __init__(self):
        pass

    def _readBookList(self, bkID, avail_count): 
        if self.node is None:
            self.node = bookNode(bkID, int(avail_count))
        else:
            insert(self.node, bkID, int(avail_count))            

    def _chkInChkOut(self, bkID, inOut):
        node = lookup(self.node, bkID)
        if inOut == 'checkOut':
            node.avCntr -= 1  # TODO : handle condition for zero available
            node.chkOutCntr += 1
        elif inOut == 'checkIn':
            node.avCntr += 1

    def _getTopBooks(self, bkNode):
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
                print(libraryRecords.node.preorder(libraryRecords.node)) # For Test
                libraryRecords._getTopBooks(libraryRecords.node)
