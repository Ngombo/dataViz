import matplotlib.pyplot as plot
from results import run_delay_boxplots, runbars
from variables import root_url

# showresults(feature, outliers or not, notch or not)
##runbars('length', 1, 0)
# runboxplots('length', 0, 0)

# To plot the boxplot
feature = 'delay'  # feature to be plotted in the dataset
outliers = 0  # plot the outliers or not
notch = 0  # plot the notches or not
client = 'mobile'  # 'box' or 'mobile', machines that hosts that hosts the mgt protocol clients
run_delay_boxplots(client, feature, outliers, notch)
# runboxplots('delay', 0, 0)

# to keep the figures alive
plot.show()
# plot.savefig(root_url+'delays.png', dpi=300)
