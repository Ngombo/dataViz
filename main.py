import matplotlib.pyplot as plot
from results import showresults

# showresults(feature, outliers or not, notch or not)
showresults('length', 1, 0)
showresults('length', 0, 1)

showresults('delay', 1, 0)
showresults('delay', 0, 1)

# to keep the figures alive
##plot.show()
# plot.savefig('delays.png', dpi=300)