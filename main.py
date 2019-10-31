import matplotlib.pyplot as plot
from results import main_run

feature = 'delay'  # feature to be plotted in the dataset
outliers = 1  # plot the outliers or not
notch = 0  # plot the notches or not
client = 'mobile'  # 'box' or 'mobile', machines that hosts that hosts the mgt protocol clients

# To compute everything
main_run(client, feature, outliers, notch)

# to keep the figures alive
plot.show()
# plot.savefig(root_url+'delays.png', dpi=300)
