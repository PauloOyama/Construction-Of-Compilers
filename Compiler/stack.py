class StackNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    """
    Initializing a stack.
    Use a dummy node, which is
    easier for handling edge cases.
    """

    def __init__(self):
        self.head = StackNode("head")
        self.size = 0

    # String representation of the stack
    def __str__(self):
        cur = self.head.next
        out = ""
        while cur:
            out += str(cur.value) + "->"
            cur = cur.next
        return out[:-2]

    def get_size(self):
        """
        Get the current size of the stack
        """
        return self.size

    def is_empty(self):
        """
        Check if the stack is empty
        """
        return self.size == 0

    def is_not_empty(self):
        """
        Check if the stack is empty
        """
        return self.size != 0

    def peek(self):
        """
        Get the top item of the stack
        """
        # Sanitary check to see if we
        # are peeking an empty stack.
        if self.is_empty():
            raise Exception("Peeking from an empty stack")
        return self.head.next.value

    def push(self, value):
        """
        Push a value into the stack.
        """
        node = StackNode(value)
        node.next = self.head.next
        self.head.next = node
        self.size += 1

    def pop(self):
        """
        Remove a value from the stack and return.
        """
        if self.is_empty():
            raise Exception("Popping from an empty stack")
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.value
