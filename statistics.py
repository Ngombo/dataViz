import numpy

# Stats

# Array with the number of readings counted by trial
sentReadings = [25, 25, 25, 25]  # , 339, 341, 3221, 3319, 683, 872, 335, 368]


def stats(df, label, label2):
    sentframes = 0
    receivedframes = 0
    frameloss = 0

    if label2 == 'lw':
        sentframes = 26
        receivedframes = len(df)
        frameloss = numpy.round((1 - (receivedframes / float(sentframes))) * 100, 2)
    if label2 == 'ul':
        sentframes = 25
        receivedframes = len(df)
        frameloss = numpy.round((1 - (receivedframes / float(sentframes))) * 100, 2)
    mean = numpy.round(df.mean(), 2)
    median = numpy.round(df.median(), 2)
    mode = numpy.round(df.mode()[0], 2)


    print '\nStats for trial number ' + label
    if label2 == 'lw' or label2 == 'ul':
        print 'Sent Frames: ' + str(sentframes)
        print 'Received Frames: ' + str(receivedframes)
        print 'Frame Loss: ' + str(frameloss)
    print 'mean: ' + str(mean)
    print 'median: ' + str(median)
    print 'mode: ' + str(mode)

    if label2 == 'sm':
        sum = df.sum()
        print 'sum: ' + str(sum) + '\n'
