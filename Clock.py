import time


# the clock is used mainly for converting between representations of time - either a string, or an integer number.
# the clock also asserts valid input from the user to ensure that the time string passed to other methods will be able
# to be parsed and a correct corresponding integer value will result
class Clock:

    # given time input as a string, this method converts the string into an int representation of that time. The int
    # number will be the number of minutes since midnight
    #
    # time and space complexity = Big O(1)
    @staticmethod
    def convertTimeToInt(timeStr):

        # used for reading from the package info csv - any package marked with a deadline of EOD means 5:00 pm - so
        # a value of 17 hours - or 1020 minutes from midnight is returned
        if timeStr == "EOD":
            return 1020

        # because the string is indexed at the first 2 positions to parse an hour value, if there is only one digit in
        # the hour, a '0' is added to the beginning so the value will be parsed correctly
        elif timeStr[1] == ":":
            timeStr = "0" + timeStr

        # since time is represented in this program on the 12 hr clock and not military time, to accurately calculate
        # the minutes since midnight of a time with an hour between 1-11 PM, an offset of 12 hours must be added to
        # avoid being mistakenly interpreted as 12 hrs earlier
        timeSuffixAdjustment = 0 if timeStr[6:8].upper() == "AM" or int(timeStr[0:2]) == 12 else 720

        # once any necessary adjustments have been made, the minutes since midnight is calculated and returned
        return (int(timeStr[0:2]) * 60) + int(timeStr[3:5]) + timeSuffixAdjustment

    # this method does just the opposite of the one above - and converts an integer representation of time in minutes
    # to a human-readable string
    #
    # time and space complexity = Big O(1)
    @staticmethod
    def convertIntToTime(mins):

        # first the value is divided by 60 for the number of hours, and that value is cast to a string and stored
        hr = str(int(mins / 60))

        # next the remainder after even division by 60 is found, representing the minute of the hour
        minute = str(mins % 60)

        # if there are more than 11 hours, since a 12-hour clock is being used, the suffix is changed to 'PM' and the
        # hours are decreased by 12 if there are more than 12 hours
        suffix = "AM" if int(hr) < 12 else "PM"
        if int(hr) > 12:
            hr = str(int(hr) - 12)

        # if there are less than 10 minutes, a '0' is added onto the beginning of the minutes string
        if int(minute) < 10:
            minute = "0" + minute

        return hr + ':' + minute + ' ' + suffix

    # this method specifies a required format for time strings and is used by the main program entry to assert properly
    # formatted time is received before passing it to other clock methods to be parsed
    #
    # time and space complexity = Big O(1)
    @staticmethod
    def getValidInput(userInput):
        try:
            time.strptime(userInput, '%I:%M %p')
            return True
        except ValueError:
            return False
