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


class LibraryRecord:
    """ """

    node = None

    def __init__(self):
        pass

    def _readBookList(self, bkID, availCount):
        """
        Function adds book ID and the count of available books to the library

        :param bkID: Book ID
        :param avail_count: Count of available books for this book
        :return: None
        """
        if self.node is None:
            self.node = bookNode(bkID, int(availCount))
        else:
            self.insert(self.node, bkID, int(availCount))

    def _chkInChkOut(self, bkID, inOut):
        """
        Updates the value of available books and checked out book counter
        based on prompt options 'checkIn' or 'checkOut'

        inOut value:
            checkOut -> Decreases count of available books
            checkIn -> Increases count of available books

        :param bkID: Book ID
        :param inOut: Prompt if the book is checked in or checked out
        :return: None
        """
        node = self.lookup(self.node, bkID)

        if node.bookID:
            if inOut == 'checkOut':
                if node.avCntr > 0:
                    node.avCntr-=1
                    node.chkOutCntr+=1
                else:
                    output = open("outputPS6.txt","a")
                    output.write("All available copies of the below books have been checked out:"+" \n")
                    output.write(bkID+'\n')
                    output.close()

            elif inOut == 'checkIn':
                node.avCntr+=1
        else:
            output = open("outputPS6.txt","a")
            output.write("Book id {} does not exist.".format(bkID))
            output.close()

    def _getTopBooks(self, bkNode):
        """

        :param bkNode: bookNode tree object
        :return: does not return anything, writes output to outputPS6.txt
        """
        topBooks = self.getTopBooks(bkNode)
        counter = 1
        for book in topBooks:
            output = open("outputPS6.txt","a")
            output.write('Top Books '+str(counter)+': '+str(book.bookID) + ', ' + str(book.chkOutCntr)+'\n')
            output.close()
            counter+=1

    def _notIssued(self, bkNode):
        """

        :param bkNode: bookNode tree object
        :return deletedBooks: books IDs that were deleted
        """
        root = bkNode
        notIssued = self.notIssued(bkNode)
        deletedBooks = []

        for nodeID in notIssued:
            node = self.lookup(root,nodeID)
            deletedBooks.append(self.deleteNode(node,root))
        output = open("outputPS6.txt","a")
        output.write('List of books not issued:\n')
        for book in deletedBooks:
            output.write(str(book)+'\n')
        output.close()

        return deletedBooks

    def _findBook(self, eNode, bkID):
        """

        :param eNode: bookNode tree object
        :param bkID: Book ID
        :return:
        """
        node = self.lookup(eNode, bkID)
        if node and node.bookID:
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
        res = self.traverse(bkNode)

        res.sort(key=lambda x: x.bookID)

        output = open("outputPS6.txt","a")
        output.write('There are a total of {} book titles in the library.\n'.format(len(res)))
        for book in res:
            output.write('{}, {}'.format(book.bookID, book.avCntr)+'\n')
        output.close()

        

    def insert(self, node, bkID, avail_count):
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

    def lookup(self, node, key):
        """
        This function looks up the tree for the give book ID and
        returns the object for that book

        :param node: bookNode tree object
        :param key: Book ID being looked for
        :return: bookNode : Book object for the ID looked up
        """
        if node is None:
            return False

        if node.bookID == key: # checking if current node is the searched one
            return node

        left_node = self.lookup(node.left, key) # checking if left node is the searched one
        if left_node:
            return left_node

        right_node = self.lookup(node.right, key)  # checking if right node is the searched one
        return right_node

    def getTopBooks(self, bkNode):
        """

        :param bkNode: bookNode tree object
        :return: maxRes[0:3] first 3 items in the list maxRes which is sorted in descending order of checkout count
        """
        if(bkNode is None):
            return []

        node = bkNode
        left = bkNode.left
        right = bkNode.right

        maxRes = []
        if(node is not None):
            maxRes = self.getTopBooks(left)
            maxRes = maxRes + self.getTopBooks(right)
            maxRes.append(node)
            maxRes.sort(key=lambda x: x.chkOutCntr, reverse=True)
        return maxRes[0:3]

    def notIssued(self, node):
        """
        :param bkNode: bookNode tree object
        :return notIssued: list of book nodes to be deleted
        """
        notIssued = []
        if(node.left is not None):
            notIssued = notIssued + self.notIssued(node.left)
        if(node.chkOutCntr == 0):
            notIssued.append(node.bookID)
        if(node.right is not None):
            notIssued = notIssued + self.notIssued(node.right)
        return notIssued

    def deleteNode(self, bkNode, root):
        """

        :param bkNode: bookNode tree object
        :param root: root of the tree
        :return deletedID: ID of the delted book
        """
        curr = [root]
        parent = []
        last_parent = None
        deepest_rightmost = None
        while(len(curr)):
            deepest_rightmost = curr.pop(0)
            if(len(parent)):
                last_parent = parent.pop(0)
            if(deepest_rightmost.left):
                curr.append(deepest_rightmost.left)
                parent.append(deepest_rightmost)
            if(deepest_rightmost.right):
                parent.append(deepest_rightmost)
                curr.append(deepest_rightmost.right)

        deletedID = bkNode.bookID
        bkNode.bookID = deepest_rightmost.bookID
        bkNode.avCntr = deepest_rightmost.avCntr
        bkNode.chkOutCntr = deepest_rightmost.chkOutCntr
        if(last_parent.left == deepest_rightmost):
            last_parent.left = None
        elif(last_parent.right == deepest_rightmost):
            last_parent.right = None
        deepest_rightmost = None
        return deletedID

    def traverse(self, bkNode):
        res = []
        if bkNode:
            res.append(bkNode)
            res = res + self.traverse(bkNode.left)
            res = res + self.traverse(bkNode.right)
        return res


if __name__ == '__main__':
    libraryRecords = LibraryRecord()

    with open('inputPS6.txt') as f:
        lines = f.readlines()

        for line in lines:
            bookInfo = line.strip('\n').split(',')
            libraryRecords._readBookList(bookInfo[0],bookInfo[1])
    # print(libraryRecords.node.inorder(libraryRecords.node))
    # print(libraryRecords.node.preorder(libraryRecords.node))

    with open('promptsPS6.txt') as f:
        lines = f.readlines()
        for line in lines:
            prompt = line.strip('\n').replace(' ','').split(':')

            if prompt[0] == 'checkIn' or prompt[0] == 'checkOut':
                libraryRecords._chkInChkOut(prompt[1], prompt[0])
            elif prompt[0] == 'ListTopBooks':
                libraryRecords._getTopBooks(libraryRecords.node)
            elif prompt[0] == 'findBook':
                libraryRecords._findBook(libraryRecords.node, prompt[1])
            elif prompt[0] == 'BooksNotIssued':
                libraryRecords._notIssued(libraryRecords.node)
            elif prompt[0] == 'printInventory':
                libraryRecords.printBooks(libraryRecords.node)
    # print(libraryRecords.node.preorder(libraryRecords.node))
    # print(libraryRecords.node.inorder(libraryRecords.node))
