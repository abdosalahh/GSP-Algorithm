import itertools
import re
class GSP:
    def __init__(self, sequances, minSupport):
        self.sequances = sequances
        self.minSupport = minSupport / 100 * len(self.sequances)

    def count_min_support(self, elementList):
        # initialize counter dictionary
        dic_counter2 = {}
        for k in elementList:
            dic_counter2[k] = 0

        # count support of each element
        for item in elementList:
            for data in self.sequances:
                position = 0
                flag_length = 0
                if type(item) is tuple:
                    for i in range(len(item)):
                        if len(item[i]) > 1:
                            while position < len(data):
                                regEx = ""
                                for char in item[i]:
                                    regEx += f".*?{char}"
                                if re.search(regEx, data[position]):
                                    position += 1
                                    flag_length += 1
                                    break
                                position += 1
                        else:
                            while position < len(data):
                                if data[position].find(item[i]) != -1:
                                    position += 1
                                    flag_length += 1
                                    break
                                position += 1
                        if flag_length == len(item):
                            dic_counter2[item] += 1
                            break
                        elif flag_length == 0:
                            break
                else:
                    while position < len(data):
                        regEx = ""
                        for char in item:
                            regEx += f".*?{char}"
                        if re.search(regEx, data[position]):
                            dic_counter2[item] += 1
                            break
                        else:
                            position += 1

        # filter item that < min_support
        two_item_set = {}
        for val, counter in dic_counter2.items():
            if counter >= self.minSupport:
                two_item_set[val] = counter

        two_item_list = [*two_item_set.keys()]
        # return final list
        return two_item_list, two_item_set

    def JoinOneItem(self):
        # flaten data and convert it to set to drop dublicates
        flatten_list = list(itertools.chain.from_iterable(self.sequances))
        # convert to string as FF or FG elc
        flatten_list = "".join(flatten_list)
        flatten_list2 = [*flatten_list]
        flatten_list3 = set(flatten_list2)
        l1 = list(flatten_list3)
        l1.sort()
        return l1

    def joinTowItems(self, elementList):
        # build matrix 1
        matrix1 = [p for p in itertools.product(elementList, repeat=2)]
        matrix1 = [tuple(i) for i in matrix1]
        # build matrix 2
        comb = itertools.combinations(elementList, 2)
        matrix2 = list(comb)
        matrix2 = [f"{i[0]}{i[1]}" for i in matrix2]
        return matrix1 + matrix2

    def JoinThreeOrMore(self, elementList):
        three_item_list = []
        for item in elementList:
            for item2 in elementList:
                if type(item2) is tuple and type(item) is tuple:
                    # first case
                    if len(item[0]) == 1 and len(item2[-1]) == 1:
                        if item[1:] == item2[:len(item2) - 1]:
                            if (tuple([*item, item2[-1]]) not in three_item_list):
                                three_item_list.append(tuple([*item, item2[-1]]))
                    # second case
                    elif len(item[0]) != 1 and len(item2[-1]) == 1:
                        temp = list(item)
                        temp[0] = temp[0][1:]
                        temp = tuple(temp)
                        if temp[0:] == item2[:len(item2) - 1]:
                            if (tuple([*item, item2[-1]]) not in three_item_list):
                                three_item_list.append(tuple([*item, item2[-1]]))
                    # third case
                    elif len(item[0]) == 1 and len(item2[-1]) != 1:
                        temp = list(item2)
                        temp[-1] = temp[-1][:len(temp) - 1]
                        temp = tuple(temp)
                        if item[1:] == temp[0:]:
                            if (tuple([*item, item2[-1]]) not in three_item_list):
                                three_item_list.append(tuple([*item, item2[-1]]))
                    # forth case
                    else:
                        temp_item = list(item)
                        temp_item[0] = temp_item[0][1:]
                        temp_item = tuple(item)
                        temp_item2 = list(item2)
                        temp_item2[-1] = temp_item2[-1][:len(temp_item2) - 1]
                        temp_item2 = tuple(item2)
                        if temp_item[0:] == temp_item2[0:]:
                            if (tuple([*item, item2[-1]]) not in three_item_list):
                                three_item_list.append(tuple([*item, item2[-1]]))

                elif type(item2) is not tuple and type(item) is tuple:  # (A , B) + (AB)
                    # first case
                    if len(item[0]) == 1:
                        if item[1:][0] == item2[:len(item2) - 1] or item[1:][0] == item2[1:len(item2)]:
                            if (tuple([item[0], item2]) not in three_item_list):
                                three_item_list.append(tuple([item[0], item2]))
                    # second case
                    elif len(item[0]) != 1:
                        temp = list(item)
                        temp[0] = temp[0][1:]
                        temp = tuple(temp)
                        if temp[0:][0] == item2[:len(item2) - 1] or item[1:][0] == item2[1:len(item2)]:
                            if (tuple([item[0], item2]) not in three_item_list):
                                three_item_list.append(tuple([item[0], item2]))

                elif type(item2) is tuple and type(item) is not tuple:
                    # first case
                    if len(item2[-1]) == 1:
                        if item[1:] == item2[:len(item2) - 1][0] or item[1:] == item2[1:len(item2)][0]:
                            if (tuple([item, item2[-1]]) not in three_item_list):
                                three_item_list.append(tuple([item, item2[-1]]))
                    # third case
                    elif len(item2[-1]) != 1:
                        temp = list(item2)
                        temp[-1] = temp[-1][:len(temp) - 1]
                        temp = tuple(temp)
                        if item[1:] == temp[0:][0] or item[1:] == temp[0:][0]:
                            if (tuple([item, item2[-1]]) not in three_item_list):
                                three_item_list.append(tuple([item, item2[-1]]))
                elif type(item2) is not tuple and type(item) is not tuple:
                    if item[1:] == item2[0:len(item2) - 1]:
                        if (item + item2[-1] not in three_item_list):
                            three_item_list.append(item + item2[-1])

        # three_item_set = set(three_item_list)
        # three_item_list = list(three_item_set)
        # three_item_list.sort()
        return three_item_list

    def search(self):
        result = []
        # step 1
        l1 = self.JoinOneItem()
        oneItemList, oneItemDictionry = self.count_min_support(l1)
        result.append(oneItemList)
        # step 2
        l2 = self.joinTowItems(oneItemList)
        twoItemList, twoItemDictionry = self.count_min_support(l2)
        result.append(twoItemList)
        # step 3
        l3 = self.JoinThreeOrMore(twoItemList)
        threeOrMoreItemList, threeOrMoreItemDictionry = self.count_min_support(l3)
        result.append(threeOrMoreItemList)
        while len(threeOrMoreItemList) != 0:
            l = self.JoinThreeOrMore(threeOrMoreItemList)
            threeOrMoreItemList, threeOrMoreItemDictionry = self.count_min_support(l)
            if (len(threeOrMoreItemList) != 0):
                result.append(threeOrMoreItemList)

        return result


dataset = [['A', 'B', 'FG', 'C', 'D'],
           ['B', 'G', 'D'],
           ['B', 'F', 'G', 'AB'],
           ['F', 'AB', 'C', 'D'],
           ['A', 'BC', 'G', 'F', 'DE']]

# dataset = [['bd', 'c', 'b'],
#            ['bf', 'ce', 'b'],
#            ['ag', 'b'],
#            ['be', 'ce'],
#            ['a', 'bd', 'b', 'c', 'b']]

# dataset = [['4', '7', '16', '13', '24', '3'],
#            ['14', '3', '23', '234'],
#            ['56', '12', '56', '3', '2'],
#            ['2', '34', '25', '1', '24']]

# dataset = [['CD', 'ABC', 'ABF', 'ACDF'],
#            ['ABF', 'E'],
#            ['ABF'],
#            ['DGH', 'BF', 'AGH']]

gsp = GSP(dataset, 40)
final = gsp.search()
print(final)
