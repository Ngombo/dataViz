import matplotlib.pyplot as plot
from plots import runplots

# runplots(feature, outliers or not, notch or not)
runplots('delay', 1, 1)

# to keep the figures alive
plot.show()
# plot.savefig('delays.png', dpi=300)