"""
Add Two Numbers
===============
https://leetcode.com/problems/add-two-numbers/

    You are given two non-empty linked lists
    representing two non-negative integers.
    The digits are stored in reverse order
    and each of their nodes contain a single digit.
    Add the two numbers and return it as a linked list.

    You may assume the two numbers do not contain any leading zero,
    except the number 0 itself.

    Example::
        Input:
          (2 -> 4 -> 3) +

          (5 -> 6 -> 4)

        Output:
          (7 -> 0 -> 8)

        Explanation:
          342 + 465 = 807.

"""


class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        name = self.__class__.__name__
        hexid = hex(id(self))

        val = self.val

        arr = [val]
        node = self.next
        while node is not None:
            arr.append(node.val)
            node = node.next
        return f'{name}({arr}) at {hexid}'
# %%


class Solution:

    @staticmethod
    def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:

        if Solution.len(l1) > Solution.len(l2):
            r, other = l1, l2
        else:
            r, other = l2, l1

        r_start, carry = r, 0
        while r:
            val = r.val + other.val + carry

            if val > 9:
                carry = 1
                val = val % 10
            else:
                carry = 0

            r.val = val

            if not r.next and carry:
                r.next = ListNode(0)

            if not other.next:
                other.next = ListNode(0)

            other = other.next
            r = r.next

        return r_start

    @staticmethod
    def len(L):
        length = 0
        while L:
            L = L.next
            length += 1
        return length
# %%


def main():

    from practice.util.driver import Driver

    driver = Driver(Solution, 'addTwoNumbers')

    l1 = createList(values=[2, 4, 3])
    l2 = createList(values=[5, 6, 4])

    driver.run(
        l1=l1,
        l2=l2, )


def createList(values):
    val = values.pop(0)
    l1 = ListNode(val)
    node = l1
    while values:
        val = values.pop(0)
        node.next = ListNode(val)
        node = node.next
    return l1


if __name__ == '__main__':
    main()
