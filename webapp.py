import streamlit as st
from datetime import date
from sklearn.metrics import mean_squared_error, mean_absolute_error
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
from plotly.subplots import make_subplots

def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data
    
def caricaCrypto():
	from pandas_ods_reader import read_ods
	path = "Crypto.ods"
	sheet_idx = 1
	df = read_ods(path, sheet_idx)
	sheet_name = "Foglio1"
	df = read_ods(path, sheet_name)
	df = read_ods(path, 1, headers=False)
	df = read_ods(path, 1, columns=["titolo"])
	return df    
    
def caricatitoli():
	from pandas_ods_reader import read_ods
	path = "Titoli.ods"
	sheet_idx = 1
	df = read_ods(path, sheet_idx)
	sheet_name = "Foglio1"
	df = read_ods(path, sheet_name)
	df = read_ods(path, 1, headers=False)
	df = read_ods(path, 1, columns=["titolo", "nome"])
	return df

def caricaETF():
	from pandas_ods_reader import read_ods
	path = "EFT.ods"
	sheet_idx = 1
	df = read_ods(path, sheet_idx)
	sheet_name = "Foglio1"
	df = read_ods(path, sheet_name)
	df = read_ods(path, 1, headers=False)
	df = read_ods(path, 1, columns=["Titolo", "nome"])
	return df

def caricaForex():
	from pandas_ods_reader import read_ods
	path = "Forex.ods"
	sheet_idx = 1
	df = read_ods(path, sheet_idx)
	sheet_name = "Foglio1"
	df = read_ods(path, sheet_name)
	df = read_ods(path, 1, headers=False)
	df = read_ods(path, 1, columns=["titolo", "sede"])
	return df

START = "2000-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('INTELLIGENZA ARTFICIALE ITALIA')
st.text(' Predizione Stock Price con fbprophet \n1) Seleziona il titolo del quale vuoi stimare un ipotetico StockPrice Trend\n2) Seleziona utilizzando le slide il periodo da pedirre\n3) Inserisci il numero e il prezzo delle azioni \n4) Premi Procedi con la previsione e attendi Predizione\n\n\n')

st.sidebar.subheader('\n\n1) Selezionare Opzione')
option = ('CRYPTO','FOREX', 'TITOLI', 'ETF')
selected_option = st.sidebar.selectbox('Seleziona il Titolo da predirre', option)

if(selected_option == 'FOREX'):
	st.sidebar.subheader('\n\n2) Seleziona o digita ciò che vuoi predirre')
	stocks = caricaForex()
	selected_stock = st.sidebar.selectbox('Seleziona il Titolo da predirre', stocks["titolo"])

if(selected_option == 'TITOLI'):
	st.sidebar.subheader('\n\n2) Seleziona ciò che vuoi predirre')
	stocks = caricatitoli()
	selected_stock = st.sidebar.selectbox('Seleziona il Titolo da predirre', stocks["titolo"])

if(selected_option == 'ETF'):
	st.sidebar.subheader('\n\n2) Seleziona ciò che vuoi predirre')
	stocks = caricaETF()
	selected_stock = st.sidebar.selectbox('Seleziona il Titolo da predirre', stocks["Titolo"])

if(selected_option == 'CRYPTO'):
	st.sidebar.subheader('\n\n2) Seleziona ciò che vuoi predirre')
	stocks = caricaCrypto()
	selected_stock = st.sidebar.selectbox('Seleziona il Titolo da predirre', stocks["titolo"])


data_load_state = st.info('Caricamento Dati')
data = load_data(selected_stock)
data_load_state.success('Dati caricati con successo !')


if(st.sidebar.checkbox('Visualizza andamento titolo')):
	st.subheader('Grafico Andamento Titolo ' + selected_stock)
	# Plot raw data
	def plot_raw_data():
		fig = go.Figure()
		fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="Stock Open"))
		fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Stock Close"))
		fig.layout.update(title_text='Andamento titolo nel tempo', xaxis_rangeslider_visible=True)
		st.plotly_chart(fig)
		
	plot_raw_data()
	
	def plot_raw_data1():
		fig = go.Figure(data=[go.Candlestick(x=data['Date'],
	        open=data['Open'], high=data['High'],
	        low=data['Low'], close=data['Close'])
	             ])
		fig.update_layout(title_text='Grafico a candela andamento titolo nel tempo', xaxis_rangeslider_visible=True)
		st.plotly_chart(fig)
		
		plot_raw_data1()

st.sidebar.subheader('\n\n3) Selezionare periodo di predizione')
n_years = st.sidebar.slider('Numero di Anni :', 0, 4)
period_y = n_years * 365

n_moth = st.sidebar.slider('Numero di Mesi :',0, 11)
period_m = n_moth * 30

n_week = st.sidebar.slider('Numero di Settimane :', 0, 3)
period_w = n_week * 7

n_day = st.sidebar.slider('Nemro di Giorni :', 0, 6)
period_d = n_day

period = period_y + period_m + period_w + period_d

st.sidebar.subheader('\n\n4) Selezionare numero dei titoli posseduti o da acquistare e il Prezzo($) di acquisto')
azioni = st.sidebar.number_input('Numero Azioni Possedute', 0.00)
prezzo = st.sidebar.number_input('Prezzo pagato per una azione ( In dollari $ ) al momento dell acquisto', 0.00)
st.sidebar.text('Valore totale :  ' + str(azioni*prezzo))


if(st.sidebar.button('Procedi con la Previsione del Titolo')):

	
	#st.write(data.tail())
	
	
		
		
	model_load_state = st.info('Sto Creando la Rete Neurale su ' + selected_stock + ' ...')

	# Predict forecast with Prophet.
	df_train = data[['Date','Close']]
	df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

	model_load_state.info('Sto Allenando la Rete Neurale su ' + selected_stock + ' ...')

	m = Prophet()
	m.fit(df_train)
	future = m.make_future_dataframe(periods=period)
	forecast = m.predict(future)

	model_load_state.info('Sto Creando il grafico della predizione su ' + selected_stock + ' ...')

	# Show and plot forecast
	st.subheader('Grafico previsione andamento Titolo ' + selected_stock)
	    
	last_element = forecast["yhat"].iloc[-1]  

	  
	st.write(f'Grafico predizione andamento titolo tra {n_years} anni {n_moth} mesi {n_week} settimane e {n_day} giorni .')
	fig1 = plot_plotly(m, forecast)
	st.plotly_chart(fig1)

	st.write("Componenti per la Pervisione del titolo " + selected_stock )
	fig2 = m.plot_components(forecast)
	st.write(fig2)
		
	
	model_load_state.info('Sto Ragionando sulle conclusioni dell Investimento...')

	st.subheader('Conclusioni investimento Titolo ' + selected_stock)
	txt1 = st.text(f'Secondo il modello di previsione il prezzo di un singolo titolo di {selected_stock} \n tra {n_years} anni {n_moth} mesi {n_week} settimane e {n_day} giorni sarà di circa {round(last_element,3)} $ \n\n')

	txt2 = st.text(f'Quindi possedendo {azioni} azioni del titolo {selected_stock} acquistate a {prezzo} ciascuna\nIl valore totale, si ipotizza che potrebbe passare da \n{round((azioni*prezzo),3)} $  a  {round((azioni*last_element),3)} $  \n\n')

	guadagno = (azioni*last_element)-(azioni*prezzo)

	if(guadagno >= 0 ):
		txt3 = st.text(f'Andando a generare un profitto stimato di circa {round(guadagno,3)} $ \n\n')
	else:
		txt3 = st.text(f'Andando a generare una perdita di circa  {round(guadagno,3)} $ \n\n')

	if(period>0):
		misurazione_err = forecast["yhat"].iloc[:-period] 
		mae = mean_absolute_error(df_train["y"],misurazione_err)
		mse = mean_squared_error(df_train["y"],misurazione_err)
		txt3 = st.text(f'Metriche valutazione modello predittivo : \n 1)Errore Medio Assoluto : {round(mae,3)} \n2) Errore Medio Quadratico : {round(mse,3)}')

	model_load_state.success('Previsione su ' + selected_stock + ' Completata ...')
	
	error = st.error('Attenzione !  Questo strumento NON tiene conto di Guerre, Pandemie, Speculazioni, Possibili esplosioni di bolle, Scandali o Colpi di Stato.')
	error2 = st.warning('Quindi è vivamente SCONSIGLIATO investire i propri capitali tenendo conto esclusivamente di questo strumento...')
	error3 = st.info('Invece è CONSIGLIATO fare prima degli accurati studi sul titolo o opzione su cui si vuole investire e solo successivamente fare ulteriori Controlli o Verifiche utilizzando lo strumento...')
