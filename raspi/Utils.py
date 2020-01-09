# credits go to stackoverflow (https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another)
def translate(value, fromMin, fromMax, toMin, toMax):
    if value > fromMax:
        value = fromMax
    elif value < fromMin:
        value = fromMin

    # Figure out how 'wide' each range is
    fromSpan = fromMax - fromMin
    toSpan = toMax - toMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - fromMin) / float(fromSpan)

    # Convert the 0-1 range into a value in the right range.
    return toMin + (valueScaled * toSpan)