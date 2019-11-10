import matplotlib.pyplot as plot
from results import main_run
from PIL import Image
from io import BytesIO

from variables import root_url

feature = 'delay'  # feature to be plotted in the dataset
outliers = 1  # plot the outliers or not
notch = 0  # plot the notches or not
# client = 'mobile'  # 'box' or 'mobile', machines that hosts that hosts the mgt protocol clients
client = 'mob'  # 'statio' or 'mob', machines that hosts that hosts the mgt protocol clients


def save_images():
    # Save the Images
    url = root_url+'figures/'
    plot.savefig(url + '.png', dpi=600, transparent=True)
    plot.savefig(url + '.jpg', dpi=600)
    plot.savefig(url + '.pdf')
    plot.savefig(url + '.svg')

    # (1) save the image in memory in PNG format
    png1 = BytesIO()
    # (2) load this image into PIL
    png2 = Image.open(png1)
    # (3) save as TIFF
    png2.save(url + '.tiff')
    png1.close()


# To compute everything
main_run(client, feature, outliers, notch)

#save_images()

# to keep the figures alive
plot.show()
