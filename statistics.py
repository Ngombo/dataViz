import numpy

# Stats

# Array with the number of readings counted by trial
sentReadings = [25, 25, 25, 25]  # , 339, 341, 3221, 3319, 683, 872, 335, 368]


def stats(df, label):
    # sentframes = sentReadings[i]
    # receivedframes = datasets[i].count()
    # frameloss = numpy.round((1 - (receivedframes / float(sentframes))) * 100, 2)
    mean = numpy.round(df.mean(), 2)
    median = numpy.round(df.median(), 2)
    mode = numpy.round(df.mode()[0], 2)
    sum = df.sum()
    # mode = datasets[i].mode()
    # print datasets[i].mode(self, dropna=True)

    print '\nStats for ' + label
    # print 'Sent Frames: ' + str(sentframes)
    # print 'Received Frames: ' + str(receivedframes)
    # print 'Frame Loss: ' + str(frameloss)
    print 'mean: ' + str(mean)
    print 'median: ' + str(median)
    print 'mode: ' + str(mode)
    print 'sum: ' + str(sum) + '\n'
