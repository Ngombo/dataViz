import matplotlib.pyplot as plot
from results import main_run
# from PIL import Image
# from io import BytesIO


feature = 'delay'  # feature to be plotted in the dataset
outliers = 1  # plot the outliers or not
notch = 0  # plot the notches or not
#client = 'mobile'  # 'box' or 'mobile', machines that hosts that hosts the mgt protocol clients
client = 'statio'  # 'statio' or 'mob', machines that hosts that hosts the mgt protocol clients

# To compute everything
main_run(client, feature, outliers, notch)

#save_images()

# def save_images():
#     # Save the Images
#     url = 'C:/Users/X260/OneDrive/Documents/UC/_LCT/GeneralHands-on/LwM2M/COAPvsHTTP-ISABELA/figures/1000_readings/'+feature
#     plot.savefig(url+'.png', dpi=600, transparent=True)
#     plot.savefig(url+'.jpg', dpi=600)
#     plot.savefig(url+'.pdf')
#     plot.savefig(url+'.svg')
#
#     # (1) save the image in memory in PNG format
#     png1 = BytesIO()
#     # (2) load this image into PIL
#     png2 = Image.open(png1)
#     # (3) save as TIFF
#     png2.save(url+'.tiff')
#     png1.close()

# to keep the figures alive
plot.show()


