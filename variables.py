import matplotlib.pyplot as plot

# Global variables

sentReadings = 250  # of the readings
precision_delay = 1000000  # of the timestamps posix epoch
precision_length = 1024  # of the timestamps posix epoch
number_trials = 10  # Number of trials done
root_url = 'C:/Users/X260/OneDrive/Documents/UC/_LCT/GeneralHands-on/LwM2M/COAPvsHTTP-ISABELA/raw/250_readings/'  # Location of the files

# colors array
# https://matplotlib.org/3.1.1/tutorials/colors/colors.html
box_colors = ['navy', 'lightgrey', 'black', 'lightgrey', 'green']
box_colors2 = ['navy', 'lightgrey', 'black', 'lightgrey', 'green']


# box_colors = ['purple', 'yellow', 'black', 'lightgrey', 'green']
# box_colors2 = ['navy', 'chartreuse', 'black', 'lightgrey', 'green']

def save_images(client, label):
    # Save the Images
    url = root_url + 'figures/'
    # plot.savefig(url + client + '_outliers.' + str(outliers) + feature + '.png', dpi=600, transparent=True)
    # plot.savefig(url + client + '_outliers.' + str(outliers) + feature + '.jpg', dpi=600)

    plot.savefig(url + client +'_'+ label + '.svg')

    # # (1) save the image in memory in PNG format
    # png1 = BytesIO()
    # # (2) load this image into PIL
    # png2 = Image.open(png1)
    # # (3) save as TIFF
    # png2.save(url + '.tiff')
    # png1.close()
