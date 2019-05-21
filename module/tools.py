import pandas as pd
import matplotlib.pyplot as plt
import pandas.plotting._converter as pandacnv

class EnergyPrediction:
    
    def __init__(self,url, names_col=['Other renewables','Wind', 'All utility-scale solar',
                                      'Geothermal', 'Wood and wood-derived fuels', 'Other biomass']):
        self.data = pd.read_csv(url,index_col=0);
        self.data.dropna(inplace=True);
        self.data.drop([self.data.columns[0], self.data.columns[1]], axis=1, inplace=True);
        self.data = self.data.T;
        self.data = self.data.T.drop_duplicates().T;
        self.data.columns = names_col;
        self.data.index.names = ['Date']
        self.data.index = pd.to_datetime(self.data.index)
        pandacnv.register()



    def showEnergyGen(self,title = 'US Energy Generation From Renewables from 2001 to 2016',
                      labelx='Date',labely="Energy [unit in $10^{3} MWh$]"):        
        plt.plot(self.data)
        plt.xlabel(labelx)
        plt.ylabel(labely)
        plt.title(title)
        plt.legend(self.data.columns)
        plt.show();
        