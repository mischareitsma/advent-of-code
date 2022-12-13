import ast

LT: int = -1
EQ: int = 0
GT: int = 1

class Packet:
    
    def __init__(self, packet_input: list|str):
        if type(packet_input) == str:
            packet_input = ast.literal_eval(packet_input)

        self.data = packet_input
    
    def __lt__(self, other):
        return self.__compare_packets(other) == LT

    def __gt__(self, other):
        return self.__compare_packets(other) == GT

    def __eq__(self, other):
        return self.__compare_packets(other) == EQ

    def __compare_packets(self, other):
        return self.__compare_lists(self.data, other.data)

    @staticmethod
    def __compare_lists(data, other_data):

        for i, sd in enumerate(data):

            # self has more data then other, so self is greater than
            if i >= len(other_data):
                return GT
            
            od = other_data[i]
            
            if type(sd) == int and type(od) == int:
                # Both are ints. < and > will end the comparison, == will not
                # self is lower than, so packets is lower than
                if sd < od:
                    return LT
                # self is greater than, so packets is greater than
                if sd > od:
                    return GT
            else:
                # One of two could be an int, convert to list
                if type(sd) == int:
                    sd = [sd]
                if type(od) == int:
                    od = [od]

                r = Packet.__compare_lists(sd, od)
                if r != EQ:
                    return r
        
        if len(data) < len(other_data):
            return LT
        
        return EQ
