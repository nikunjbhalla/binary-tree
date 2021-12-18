class bookNode:
    """ 
    Class for book object which holds book ID, counter for the books available,
    number of times book is checked out and reference to adjacent book object 
    """

    def __init__ (self, bkID, avail_count):
        """
        :param bkID: Book ID
        :param avail_count: Count of available books for this book
        """
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
    """
    Method adds a new book in the library

    :param node: bookNode tree object
    :param bkID: Book ID
    :param avail_count: Count of available books for this book
    :return:
    """
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
    """
    This function looks up the tree for the give book ID and
    returns the object for that book

    :param node: bookNode tree object
    :param key: Book ID being looked for
    :return: bookNode : Book object for the ID looked up
    """
    if node is None:
        return False # TODO : handle error for None Node

    if node.bookID == key: # checking if current node is the searched one
        return node

    left_node = lookup(node.left, key) # checking if left node is the searched one
    if left_node:
        return left_node

    right_node = lookup(node.right, key)  # checking if right node is the searched one
    return right_node


class LibraryRecord:
    """ """

    node = None

    def __init__(self):
        pass

    def _readBookList(self, bkID, avail_count):
        """
        Function adds book ID and the count of available books to the library

        :param bkID: Book ID
        :param avail_count: Count of available books for this book
        :return:
        """
        if self.node is None:
            self.node = bookNode(bkID, int(avail_count))
        else:
            insert(self.node, bkID, int(avail_count))

    def _chkInChkOut(self, bkID, inOut):
        """
        Updates the value of available books and checked out book counter
        based on prompt options 'checkIn' or 'checkOut'

        inOut value:
            checkOut -> Decreases count of available books
            checkIn -> Increases count of available books

        :param bkID: Book ID
        :param inOut: Prompt if the book is checked in or checked out
        :return:
        """
        node = lookup(self.node, bkID)

        if inOut == 'checkOut':
            node.avCntr-=1 # TODO : handle condition for zero available
            node.chkOutCntr+=1
        elif inOut == 'checkIn':
            node.avCntr+=1

    def _getTopBooks(self, bkNode):
        """

        :param bkNode: bookNode tree object
        :return:
        """
        if(bkNode is None):
            return []

        node = bkNode
        left = bkNode.left
        right = bkNode.right
        
        maxRes = []
        if(node is not None):
            maxRes = self._getTopBooks(left)
            maxRes = maxRes + self._getTopBooks(right)
            maxRes.append(node)
            maxRes.sort(key=lambda x: x.chkOutCntr, reverse=True)
        return maxRes[0:3]

    def _notIssued(self, bkNode):
        """

        :param bkNode: bookNode tree object
        :return:
        """
        pass

    def _findBook(self, eNode, bkID):
        """

        :param eNode: bookNode tree object
        :param bkID: Book ID
        :return:
        """
        node = lookup(eNode, bkID)
        if node:
            if node.avCntr > 0:
                prompt_text = 'Book id {} is available for checkout'.format(bkID)
            else:
                prompt_text = 'All copies of book id {} have been checked out'.format(bkID)
        else:
            prompt_text = 'Book id {} does not exist.'.format(bkID)

        output = open("outputPS6.txt","a")
        output.write(prompt_text+" \n")
        output.close()

    def printBooks(self, bkNode):
        """

        :param bkNode: bookNode tree object
        :return:
        """
        pass


if __name__ == '__main__':
    libraryRecords = LibraryRecord()

    with open('inputPS6.txt') as f:
        lines = f.readlines()

        for line in lines:
            bookInfo = line.strip('\n').split(',')
            libraryRecords._readBookList(bookInfo[0],bookInfo[1])
        # print(libraryRecords.node.inorder(libraryRecords.node))
        # print(libraryRecords.node.preorder(libraryRecords.node)) # For Test

    with open('promptsPS6.txt') as f:
        lines = f.readlines()
        for line in lines:
            prompt = line.strip('\n').replace(' ','').split(':')

            if prompt[0] == 'checkIn' or prompt[0] == 'checkOut':
                libraryRecords._chkInChkOut(prompt[1], prompt[0])
            elif prompt[0] == 'ListTopBooks':
                print(libraryRecords.node.preorder(libraryRecords.node)) # For Test
                topBooks = libraryRecords._getTopBooks(libraryRecords.node)
                [print(str(book.bookID) + ' ' + str(book.chkOutCntr)) for book in topBooks]
            elif prompt[0] == 'findBook':
                libraryRecords._findBook(libraryRecords.node, prompt[1])
