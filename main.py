import matplotlib.pyplot as plot
from results import main_run

feature = 'delay'  # feature to be plotted in the dataset
outliers = 1  # plot the outliers or not
notch = 0  # plot the notches or not
client = 'mobile'  # 'box' or 'mobile', machines that hosts that hosts the mgt protocol clients

# To compute everything
main_run(client, feature, outliers, notch)

# Save the Images
# plot.savefig(C:/Users/X260/OneDrive/Documents/UC/_LCT/GeneralHands-on/LwM2M/COAPvsHTTP-ISABELA/figures/1000_readings/'+feature'.png', dpi=600, transparent=True)
# plot.savefig(C:/Users/X260/OneDrive/Documents/UC/_LCT/GeneralHands-on/LwM2M/COAPvsHTTP-ISABELA/figures/1000_readings/'+feature'.tiff', dpi=600)
# plot.savefig(C:/Users/X260/OneDrive/Documents/UC/_LCT/GeneralHands-on/LwM2M/COAPvsHTTP-ISABELA/figures/1000_readings/'+feature'.jpg', dpi=600)
# plot.savefig(C:/Users/X260/OneDrive/Documents/UC/_LCT/GeneralHands-on/LwM2M/COAPvsHTTP-ISABELA/figures/1000_readings/'+feature'.pdf')
# plot.savefig(C:/Users/X260/OneDrive/Documents/UC/_LCT/GeneralHands-on/LwM2M/COAPvsHTTP-ISABELA/figures/1000_readings/'+feature'.svg')

# to keep the figures alive
plot.show()


