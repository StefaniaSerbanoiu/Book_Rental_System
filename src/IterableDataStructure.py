class IterableEntity:
    def __init__(self, given_list):
        self.__list_of_objects = given_list
        self._position = 0

    def __getitem__(self, index):
        return self.__list_of_objects[index]

    def __setitem__(self, index, value):
        self.__list_of_objects[index] = value

    def __delitem__(self, index):
        del self.__list_of_objects[index]

    def __len__(self):
        return len(self.__list_of_objects)

    def __iter__(self):
        self._position = 0
        return self

    def remove(self, item):
        self.__list_of_objects.remove(item)

    def __next__(self):
        # Stop iteration when other elements are not available
        if self._position == len(self.__list_of_objects):
            raise StopIteration()
        # Move to the next element
        self._position += 1
        return self.__list_of_objects[self._position - 1]

    def append(self, element):
        self.__list_of_objects.append(element)


def comparison_function_for_ascending_order(first_element_to_compare, second_element_to_compare):
    if first_element_to_compare > second_element_to_compare:
        return True
    return False


def comparison_function_for_descending_order(first_element_to_compare, second_element_to_compare):
    if first_element_to_compare < second_element_to_compare:
        return True
    return False


def shell_sort(list_of_elements, comparison_function):
    length = len(list_of_elements)
    interval = length // 2
    while interval > 0:
        for first_index in range(interval, length):
            auxiliary_element = list_of_elements[first_index]
            second_index = first_index
            while second_index >= interval and comparison_function(list_of_elements[second_index - interval], auxiliary_element) is True:
                list_of_elements[second_index] = list_of_elements[second_index - interval]
                second_index -= interval

            list_of_elements[second_index] = auxiliary_element
        interval //= 2
    return list_of_elements


def filter_entity(list_of_elements,  acceptance_function, parameter_for_acceptance_function):
    length = len(list_of_elements)
    index = 0

    while index < length:
        element = list_of_elements[index]

        if acceptance_function(element, parameter_for_acceptance_function) is False:
            list_of_elements.remove(element)
            length -= 1
            index -= 1

        index += 1

    return list_of_elements
