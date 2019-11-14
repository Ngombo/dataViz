import matplotlib.pyplot as plot
from results import main_run
from PIL import Image
from io import BytesIO

from variables import root_url, save_images

feature = 'delay'  # feature to be plotted in the dataset
outliers = 0  # plot the outliers or not
notch = 0  # plot the notches or not
# client = 'mobile'  # 'box' or 'mobile', machines that hosts that hosts the mgt protocol clients
client = 'statio'  # 'statio' or 'mob', machines that hosts that hosts the mgt protocol clients





# To compute everything
main_run(client, feature, outliers, notch)

save_images(client, 'outliers.' + str(outliers) + feature)

# to keep the figures alive
plot.show()
