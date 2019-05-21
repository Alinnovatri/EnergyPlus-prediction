import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm 
#Arreglar error al mostrar los datos
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
    
    def showTrendGen(self, energy):
        ciclo, tend = sm.tsa.filters.hpfilter(energy)
        new_data = energy.loc[ energy.index, :]
        new_data['Trend'] = tend
        new_data[[new_data.columns[0], 'Trend']].plot(figsize=(10, 8), fontsize=12);
        legend = plt.legend()
        legend.prop.set_size(14);
        plt.show();
        
    def promMov(self, energy, days=5):
        # Calculando promedios móviles cada 5 días
        wft_ma = energy[energy.columns[0]].rolling(days).mean()
        new_df_2 = energy.loc[ energy.index, :]
        new_df_2['Moving average'] = wft_ma
        plot = new_df_2[[new_df_2.columns[0], 'Moving average']].plot(figsize=(10, 8), fontsize=12)
    
    def descST(self,energy):
        # Ejemplo de descomposición de serie de tiempo
        descomposicion = sm.tsa.seasonal_decompose(energy[energy.columns[0]], model='additive', freq=31)  
        #fig = descomposicion.plot()
        descomposicion.plot()
        
    def adjuARIMA(self,energy):
        # Modelo ARIMA sobre el valor de cierre de la acción.
        modelo = sm.tsa.ARIMA(energy[energy.columns[0]].iloc[1:], order=(1, 0, 0), freq = 'MS')  
        resultados = modelo.fit(disp=-1)  
        self.new_df_3 = energy.loc[ energy.index, :]
        self.new_df_3['Pronostico'] = resultados.fittedvalues  
        plot = self.new_df_3[[self.new_df_3.columns[0], 'Pronostico']].plot(figsize=(10, 8))
    
    def pred(self):
        start = datetime.datetime.strptime("2016-01-01", "%Y-%m-%d")
        date_list = pd.date_range('2016-01-01', freq='1D', periods=366)
        future = pd.DataFrame(index=date_list, columns= df.columns)
        data = pd.concat([df, future])
        self.new_df_3['Pronostico'] = resultados.predict(start = 1825, end = 2192, dynamic= True)
        data[['Price', 'Forecast']].plot(figsize=(12, 8))