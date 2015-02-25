class Transition(object):
    """
    This class defines a set of transitions which are applied to a
    configuration to get the next configuration.
    """
    # Define set of transitions
    LEFT_ARC = 'LEFTARC'
    RIGHT_ARC = 'RIGHTARC'
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'

    def __init__(self):
        raise ValueError('Do not construct this object!')

    @staticmethod
    def left_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        # raise NotImplementedError('Please implement left_arc!')
        # return -1

        if not conf.buffer or not conf.stack:
            return -1

        # add the arc (b, L, s) to set of arcs A and pop stack
        # that is, draw arc bt next node on the buffer and on stack with label L
        idx_wi = conf.stack[-1] # s
        idx_wj = conf.buffer.pop(0) # b
        
        if idx_wi is 0 or (idx_wj, relation, idx_wi) in conf.arcs:
            return -1

        print 'left arc'
        print (idx_wj, relation, idx_wi)

        conf.stack = conf.stack[:-1] # pop stack / remove last element
        conf.arcs.append((idx_wj, relation, idx_wi)) # add the arc (b, L, s) to A

    @staticmethod
    def right_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        if not conf.buffer or not conf.stack:
            return -1

        # You get this one for free! Use it as an example.

        # add the arc (s, L, b) to A, and push b onto stack where
        # s:idx_wi is the next node on the stack and b:idx_wj is 
        # the next node on the buffer
        idx_wi = conf.stack[-1]
        idx_wj = conf.buffer.pop(0)

        if idx_wi is 0 or (idx_wj, relation, idx_wi) in conf.arcs:
            return -1

        print 'right arc'
        print (idx_wi, relation, idx_wj)
        conf.stack.append(idx_wj) # push b onto stack
        conf.arcs.append((idx_wi, relation, idx_wj))

    @staticmethod
    def reduce(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        # raise NotImplementedError('Please implement reduce!')
        if not conf.buffer or not conf.stack:
            return -1

        print 'reduce'
        # remove b from buffer and add to stack
        idx_wj = conf.buffer.pop(0)
        conf.stack.append(idx_wj)


    @staticmethod
    def shift(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        # raise NotImplementedError('Please implement shift!')
        if not conf.stack:
            return -1

        # check preconditions, s cannot be root
        if conf.stack[-1] is 0:
            return -1
        print 'shift'
        # pop sigma
        conf.stack = conf.stack[:-1]

