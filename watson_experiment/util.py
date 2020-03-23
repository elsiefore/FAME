
def ibm_location_to_cv(location):
    """
    Convert IBM location entries into a cv location format

    :param location_entries: a list/tuple of length 4, representing
        top, left, width, height
    :return: two tuples, (left,top), (right, bottom)
    (left,top), (left + width, top+height)
    """
    # in case of float, convert to int
    top, left, width, height = [int(x) for x in location]
    return (left, top), (left+width, top+height)

def cv_location_to_ibm(location):
    """
    Convert CV location to IBM format
    :param location: a list/tuple of two tuples,
        first tuple is (left, top) cornor coordinates
        second tuple is (right, bottom) corner coordinates
    :return: a list of four entries, as top, left, width, height
    """
    left = int(location[0][0])
    top = int(location[0][1])
    right = int(location[1][0])
    bottom = int(location[1][1])

    width = right - left
    height = bottom - top

    return [top, left, width, height]