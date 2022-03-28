import streamlit as st
from datetime import date
from sklearn.metrics import mean_squared_error, mean_absolute_error
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
from plotly.subplots import make_subplots
import datetime
import pandas as pd

def load_data(ticker, periodo,intervallo):
    data = yf.download(ticker, period=periodo, interval=intervallo)
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

st.set_page_config(page_title="Italian Intelligence Analytic Suite by I.A. Italia", page_icon="📈", layout='wide', initial_sidebar_state='auto')

st.markdown("<center><h1> Italian Intelligence Investments Suite <small><br> Powered by INTELLIGENZAARTIFICIALEITALIA.NET </small></h1>", unsafe_allow_html=True)
st.write('<p style="text-align: center;font-size:15px;" > <bold>Tutti i tool di Analisi, Forecast e Visualizzazione di Dati finanziari in unico Posto <bold>  </bold><p>', unsafe_allow_html=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown(' <br>1) Seleziona il titolo del quale vuoi stimare un ipotetico StockPrice Trend<br>2) Seleziona utilizzando le slide il periodo da pedirre<br>3) Inserisci il numero e il prezzo delle azioni <br>4) Premi Procedi con la previsione e attendi Predizione<br><br><br>', unsafe_allow_html=True)

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
#inizio = st.sidebar.date_input("Da che data di inizio desideri allenare la rete", datetime.date(2015, 1, 1))
#fine = st.sidebar.date_input("Da che data di fine desideri allenare la rete", date.today())

tipoinvestitori = ( "Long Term","Short Term" )
investitore = st.sidebar.selectbox("Che tipo di investitore sei ? ", tipoinvestitori)


periodo=""
intervallo=""

if investitore == "Long Term":
	periodi = ( "ytd","6mo","1y","2y","5y","10y","max" )
	periodo = st.sidebar.selectbox("Seleziona il periodo da analizzare", periodi)
	intervallo = '1d'

if investitore == "Short Term":
	periodi = ( "ytd","1d","5d","1mo","3mo","6mo" )
	intervalli = ('1d','1h', '30m',  '15m', '5m')
	periodo = st.sidebar.selectbox("Seleziona il periodo da analizzare", periodi)
	intervallo = st.sidebar.selectbox("Seleziona l'intervallo", intervalli)

if( st.sidebar.checkbox("Carica i dati") ):


	data = load_data(selected_stock,periodo,intervallo)
	data_load_state.success('Dati caricati con successo !')

	tt = 'Date'

	if intervallo != '1d' and intervallo != '1h':
		tt = 'Datetime'

	if intervallo == '1h' :
		tt = 'index'

	data[tt] = data[tt].dt.tz_localize(None)

	if(selected_option == 'TITOLI'):
		info = st.sidebar.checkbox("Visualizza Info TITOLO")
		if(info):
			msft = yf.Ticker(selected_stock)
			st.write("Short name : " + msft.info["shortName"])
			st.write("Exchange TimezoneName : " + msft.info["exchangeTimezoneName"])
			st.write("Mercato : " + msft.info["market"])
			st.write("QuoteType : " + msft.info["quoteType"])
			st.write("")
			st.write("Divindendi  : ")
			st.write(msft.dividends)
			st.write("Splits  : ")
			st.write(msft.splits)
			st.write("")
			st.write("Finanziarie  : " )
			st.write(msft.financials)

			st.write("Finanziarie trimestrali  : ")
			st.write(msft.quarterly_financials)
			st.write("")				
			st.write("Maggiori Holder  : " )
			st.write(msft.major_holders)
			st.write("Maggiori Holder Istituzionali  : ")
			st.write(msft.institutional_holders)
			st.write("")			

			st.write("Bilancio : ")
			st.write(msft.balance_sheet)
			st.write("Bilancio Trimestrale : ")
			st.write(msft.quarterly_balance_sheet)
			st.write("")
			st.write("CashFlow : " )
			st.write(msft.cashflow)
			st.write("CashFlow Trimestrale : " )
			st.write(msft.quarterly_cashflow)
			st.write("")
			st.write("Utile : ")
			st.write(msft.earnings)
			st.write("Utile Trimestrale : ")	
			st.write(msft.quarterly_earnings)
			st.write("")				

			st.write("Calendario : " )	
			st.write(msft.calendar)
			st.write("Notizie : " )
			st.write(msft.news)	

			st.write("")
			st.write("")
			st.write("Raccomandazioni Pubbliche ufficiali")
			st.write(msft.recommendations)
			#st.write(msft.info)

	if(selected_option != 'TITOLI'):
		info = st.sidebar.checkbox("Visualizza Info")
		if(info):
			msft = yf.Ticker(selected_stock)
			st.write("Short name : " + msft.info["shortName"])
			st.write("Exchange TimezoneName : " + msft.info["exchangeTimezoneName"])
			st.write("Mercato : " + msft.info["market"])
			st.write("QuoteType : " + msft.info["quoteType"])
			st.write("")
			st.write("Raccomandazioni Pubbliche ufficiali")
			st.write(msft.recommendations)
			#st.write(msft.info)

	if(st.sidebar.checkbox('Visualizza andamento titolo')):
		st.subheader('Grafico Andamento Titolo ' + selected_stock)
		# Plot raw data
		def plot_raw_data():
			fig = go.Figure()
			fig.add_trace(go.Scatter(x=data[tt], y=data['Open'], name="Stock Open"))
			fig.add_trace(go.Scatter(x=data[tt], y=data['Close'], name="Stock Close"))
			fig.layout.update(title_text='Andamento titolo nel tempo', xaxis_rangeslider_visible=True)
			st.plotly_chart(fig)
			
		plot_raw_data()
		
		def plot_raw_data1():
			fig = go.Figure(data=[go.Candlestick(x=data[tt],
			open=data['Open'], high=data['High'],
			low=data['Low'], close=data['Close'])
			     ])
			fig.update_layout(title_text='Grafico a candela andamento titolo nel tempo', xaxis_rangeslider_visible=True)
			st.plotly_chart(fig)
			
			plot_raw_data1()

	period =0
	if investitore == "Long Term":
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
	
	if investitore == "Short Term":
		st.sidebar.subheader('\n\n3) Selezionare periodo di predizione')
		n_years = st.sidebar.slider('Numero di Giorni :', 0, 1)
		period_y = n_years * 24 * 60

		n_moth = st.sidebar.slider('Numero di ore :',0, 23)
		period_m = n_moth * 60

		n_week = st.sidebar.slider('Numero di minuti :', 0, 59)
		period_w = n_week 

		period = period_y + period_m + period_w 

	st.sidebar.subheader('\n\n4) Selezionare numero dei titoli posseduti o da acquistare e il Prezzo($) di acquisto')
	azioni = st.sidebar.number_input('Numero Azioni Possedute', 0.00)
	prezzo = st.sidebar.number_input('Prezzo pagato per una azione ( In dollari $ ) al momento dell acquisto', 0.00)
	st.sidebar.text('Valore totale :  ' + str(azioni*prezzo))


	if(st.sidebar.button('Procedi con la Previsione del Titolo')):

		
		#st.write(data.tail())
		
		
			
			
		model_load_state = st.info('Sto Creando la Rete Neurale su ' + selected_stock + ' ...')

		# Predict forecast with Prophet.
		df_train = data[[tt,'Close']]
		df_train = df_train.rename(columns={tt: "ds", "Close": "y"})

		model_load_state.info('Sto Allenando la Rete Neurale su ' + selected_stock + ' ...')

		m = Prophet()
		m.fit(df_train)
		if investitore == "Long Term":
			future = m.make_future_dataframe(periods=period)
		if investitore == "Short Term":
			if intervallo == '1h':
				future = m.make_future_dataframe(periods=period, freq='H')
			if intervallo != '1h':
				future = m.make_future_dataframe(periods=period, freq='1m')

		forecast = m.predict(future)

		model_load_state.info('Sto Creando il grafico della predizione su ' + selected_stock + ' ...')

		# Show and plot forecast
		st.subheader('Grafico previsione andamento Titolo ' + selected_stock)
		    
		last_element = forecast["yhat"].iloc[-1]  

		if investitore == "Long Term":		  
			st.write(f'Grafico predizione andamento titolo tra {n_years} anni {n_moth} mesi {n_week} settimane e {n_day} giorni .')
		if investitore == "Short Term":		  
			st.write(f'Grafico predizione andamento titolo tra {n_years} giorni {n_moth} ore e {n_week} minuti .')

		fig1 = plot_plotly(m, forecast)
		st.plotly_chart(fig1)

		st.write("Componenti per la Pervisione del titolo " + selected_stock )
		fig2 = m.plot_components(forecast)
		st.write(fig2)
			
		
		model_load_state.info('Sto Ragionando sulle conclusioni dell Investimento...')

		st.subheader('Conclusioni investimento Titolo ' + selected_stock)

		if investitore == "Long Term":		  
			txt1 = st.text(f'Secondo il modello di previsione il prezzo di un singolo titolo di {selected_stock} \n tra {n_years} anni {n_moth} mesi {n_week} settimane e {n_day} giorni sarà di circa {round(last_element,3)} $ \n\n')
		if investitore == "Short Term":		  
			txt1 = st.text(f'Secondo il modello di previsione il prezzo di un singolo titolo di {selected_stock} \n tra {n_years} giorni {n_moth} ore e {n_week} minuti sarà di circa {round(last_element,3)} $ \n\n')

		

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
			txt3 = st.text(f'Metriche valutazione modello predittivo : \n 1)Errore Medio Assoluto : {round(mae,3)} ')

		model_load_state.success('Previsione su ' + selected_stock + ' Completata ...')
		st.balloons()
		error = st.error('Attenzione !  Questo strumento NON tiene conto di Guerre, Pandemie, Speculazioni, Possibili esplosioni di bolle, Scandali o Colpi di Stato.')
		error2 = st.warning('Quindi è vivamente SCONSIGLIATO investire i propri capitali tenendo conto esclusivamente di questo strumento...')
		error3 = st.info('Invece è CONSIGLIATO fare prima degli accurati studi sul titolo o opzione su cui si vuole investire e solo successivamente fare ulteriori Controlli o Verifiche utilizzando lo strumento...')
		
		st.markdown('<bold> Se ti è stato di aiuto condividi il nostro sito per supportarci </bold>\
				   <ul> \
				  <li><a href="https://www.facebook.com/sharer.php?u=http%3A%2F%2Fintelligenzaartificialeitalia.net%2F" target="blank" rel="noopener noreferrer">Condividi su Facebook</a></li> \
				  <li><a href="https://twitter.com/intent/tweet?url=http%3A%2F%2Fintelligenzaartificialeitalia.net%2F&text=Blog%2C+Forum%2C+Progetti%2C+e+Servizi+Gratuiti+completamente+dedicati+all%27+Intelligenza+Artificiale." target="blank" rel="noopener noreferrer">Condividi su Twitter</a></li> \
				  <li><a href="https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fwww.intelligenzaartificialeitalia.net%2F&title=IntelligenzaArtificialeItalia=Blog%2C+Forum%2C+Progetti%2C+e+Servizi+Gratuiti+completamente+dedicati+all%27+Intelligenza+Artificiale.&source=IntelligenzaArtificialeItalia" target="blank" rel="noopener noreferrer">Condividi su Linkedin</a></li>\
				</ul>', unsafe_allow_html=True)	
		
		st.text("")
		st.text("")
		st.text("")
		st.text("")
		st.write("Proprietà intellettuale di [Intelligenza Artificiale Italia © ](https://intelligenzaartificialeitalia.net)")
		st.write("Hai un idea e vuoi realizzare un Applicazione Web Intelligente? contatta il nostro [Team di sviluppatori © ](mailto:python.ai.solution@gmail.com)")
