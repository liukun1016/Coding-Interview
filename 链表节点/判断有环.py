

def intersection_of_2_linked_list(headA, headB):
    """
    https://leetcode.com/problems/intersection-of-two-linked-lists
    len of nodes in A before the intersection: x
    len of nodes in B before the intersection: y
    len of nodes in the intersection, if any: z
    x + z = len(A), y + z = len(B), offset = abs(x-y)
    start from the longer one and reach to the node at offset, then use two pointers
    """
    def getSize(head):
        size = 0
        while head:
            size, head = size + 1, head.next
        return size

    l1, l2 = getSize(headA), getSize(headB)
    longer = headA if l1 > l2 else headB
    shorter = headA if l2 > l1 else headB
    offset = abs(l2-l1)
    while offset:
        longer, offset = longer.next, offset - 1
    while longer and shorter:
        if longer == shorter:
            return longer
        longer, shorter = longer.next, shorter.next
    return None
