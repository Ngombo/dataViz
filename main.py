import matplotlib.pyplot as plot
from results import runboxplots, runbars

# showresults(feature, outliers or not, notch or not)
runbars('length', 1, 0)
#runboxplots('length', 0, 0)

# runboxplots(feature, outliers or not, notch or not)
runboxplots('delay', 1, 0)
#runboxplots('delay', 0, 0)

# to keep the figures alive
plot.show()
# plot.savefig('delays.png', dpi=300)