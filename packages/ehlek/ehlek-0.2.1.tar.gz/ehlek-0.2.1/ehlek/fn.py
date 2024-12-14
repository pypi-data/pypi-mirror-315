import ccxt
import pandas
import numpy
import ta
import pyupbit
def add(a,b) :
    return a+b

def calculate_atr(data, period):
    """Calculate Average True Range (ATR)."""
    high_low = data['high'] - data['low']
    high_close = numpy.abs(data['high'] - data['close'].shift(1))
    low_close = numpy.abs(data['low'] - data['close'].shift(1))
    true_range = pandas.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    return atr

def ut_bot_alert(data, key_value=2, atr_period=1):
    """Implement UT Bot Alert logic to calculate UT value."""
    # Copy necessary fields
    temp_data = data[['close', 'high', 'low']].copy()
    temp_data['ATR'] = calculate_atr(temp_data, atr_period)
    temp_data['nLoss'] = key_value * temp_data['ATR']

    # Initialize xATRTrailingStop
    temp_data['xATRTrailingStop'] = numpy.nan

    for i in range(len(temp_data)):
        prev_stop = temp_data['xATRTrailingStop'].iloc[i - 1] if i > 0 else 0
        prev_close = temp_data['close'].iloc[i - 1] if i > 0 else 0

        if temp_data['close'].iloc[i] > prev_stop and prev_close > prev_stop:
            temp_data.loc[i, 'xATRTrailingStop'] = max(prev_stop, temp_data['close'].iloc[i] - temp_data['nLoss'].iloc[i])
        elif temp_data['close'].iloc[i] < prev_stop and prev_close < prev_stop:
            temp_data.loc[i, 'xATRTrailingStop'] = min(prev_stop, temp_data['close'].iloc[i] + temp_data['nLoss'].iloc[i])
        else:
            temp_data.loc[i, 'xATRTrailingStop'] = (
                temp_data['close'].iloc[i] - temp_data['nLoss'].iloc[i]
                if temp_data['close'].iloc[i] > prev_stop
                else temp_data['close'].iloc[i] + temp_data['nLoss'].iloc[i]
            )

    # Determine Buy and Sell signals
    temp_data['Buy'] = (
        (temp_data['close'] > temp_data['xATRTrailingStop']) &
        (temp_data['close'].shift(1) <= temp_data['xATRTrailingStop'].shift(1))
    )
    temp_data['Sell'] = (
        (temp_data['close'] < temp_data['xATRTrailingStop']) &
        (temp_data['close'].shift(1) >= temp_data['xATRTrailingStop'].shift(1))
    )

    # Generate UT signals based on Buy and Sell
    data['UT'] = temp_data.apply(lambda row: 'LONG' if row['Buy'] else ('SHORT' if row['Sell'] else None), axis=1)

    return data

def smma(series, length):
    """Calculate Smoothed Moving Average (SMMA)"""
    smma = series.ewm(alpha=1/length, adjust=False).mean()
    return smma

def zlema(series, length):
    """Calculate Zero Lag EMA (ZLEMA)"""
    ema1 = series.ewm(span=length, adjust=False).mean()
    ema2 = ema1.ewm(span=length, adjust=False).mean()
    d = ema1 - ema2
    return ema1 + d

def detect_cross_signals(df):
    """Detect Golden Cross and Dead Cross signals for Impulse MACD"""
    # Shifted values for cross detection
    prev_macd = df['ImpulseMACD'].shift(1)
    prev_signal = df['ImpulseMACDSignal'].shift(1)

    # Initialize 'imp' column with None
    df['imp'] = None

    # Detect Golden Cross: Both lines below 0 and MACD crosses above Signal
    df.loc[
        (prev_macd < prev_signal) & (df['ImpulseMACD'] > df['ImpulseMACDSignal']) &
        (df['ImpulseMACD'] < 0) & (df['ImpulseMACDSignal'] < 0),
        'imp'
    ] = 'LONG'

    # Detect Dead Cross: Both lines above 0 and MACD crosses below Signal
    df.loc[
        (prev_macd > prev_signal) & (df['ImpulseMACD'] < df['ImpulseMACDSignal']) &
        (df['ImpulseMACD'] > 0) & (df['ImpulseMACDSignal'] > 0),
        'imp'
    ] = 'SHORT'

    return df

def impulse_macd(df, lengthMA=26, lengthSignal=12):
    """Calculate LazyBear's Impulse MACD"""
    close = df['HA_Close']
    high = df['HA_High']
    low = df['HA_Low']

    tmp = df.copy()
    # HLC3 Calculation
    tmp['hlc3'] = (high + low + close) / 3

    # SMMA Calculations
    tmp['hi'] = smma(high, lengthMA)
    tmp['lo'] = smma(low, lengthMA)

    # ZLEMA Calculation
    tmp['mi'] = zlema(tmp['hlc3'], lengthMA)

    # Impulse MACD Value
    tmp['ImpulseMACD'] = numpy.where(tmp['mi'] > tmp['hi'], tmp['mi'] - tmp['hi'],
                          numpy.where(tmp['mi'] < tmp['lo'], tmp['mi'] - tmp['lo'], 0))

    # Signal Line
    tmp['ImpulseMACDSignal'] = tmp['ImpulseMACD'].rolling(window=lengthSignal).mean()

    # Histogram
    tmp['Histo'] = tmp['ImpulseMACD'] - tmp['ImpulseMACDSignal']

    df['ImpulseMACD'] = tmp['ImpulseMACD'].fillna(0).round(1)
    df['ImpulseMACDSignal'] = tmp['ImpulseMACDSignal'].fillna(0).round(1)
    df['Histo'] = tmp['Histo'].fillna(0).round(1)
    return df

def fetch_binance_data(symbol, timeframe, limit=500):
    exchange = ccxt.binance({'options': { 'defaultType': 'future' }})
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pandas.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    df['time'] = pandas.to_datetime(df['time'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Seoul').dt.strftime('%Y-%m-%d %H:%M:%S')
    return df[['time','open','high','low','close','volume']]

def fetch_upbit_data(symbol, timeframe, limit=200):
    ohlcv = pyupbit.get_ohlcv(ticker=symbol, interval=timeframe, count=limit).reset_index()
    df = pandas.DataFrame(ohlcv, columns=['index', 'open', 'high', 'low', 'close', 'volume'])
    df['time'] = df['index']
    df.drop('index', axis=1, inplace=True)
    return df[['time','open','high','low','close','volume']]

def spider(df):
    
    df['HA_Close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    # HA-Open
    for i in range(len(df)):
        if i == 0:
            df['HA_Open'] = (df['open'].iloc[0] + df['close'].iloc[0]) / 2
        else :
            df.loc[i,'HA_Open'] = (df['HA_Open'].iloc[i-1] + df['HA_Close'].iloc[i-1]) / 2
   
    df['HA_Open'] = df['HA_Open'].round(1)

    # HA-High 계산
    df['HA_High'] = df[['high', 'HA_Open', 'HA_Close']].max(axis=1).round(1)

    # HA-Low 계산
    df['HA_Low'] = df[['low', 'HA_Open', 'HA_Close']].min(axis=1).round(1)     

    # rsi
    df['rsi'] = ta.momentum.RSIIndicator(df['HA_Close']).rsi().fillna(0)

    # EMA 200
    df['EMA_200'] = ta.trend.ema_indicator(df['HA_Close'], window=200).fillna(0).round(1)
    
    # 캔들 색
    df['side'] = df.apply(
        lambda row: 'LONG' if row['HA_Close'] > row['HA_Open'] else 'SHORT', axis=1
    )
    
    # 캔들 타입
    df['candle_type'] = numpy.where(
        (df['side'] == 'SHORT') & (df['HA_High'] == df[['HA_Open', 'HA_Close']].max(axis=1)), '1',
        numpy.where(
            (df['side'] == 'LONG') & (df['HA_Low'] == df[['HA_Open', 'HA_Close']].min(axis=1)), '1',
            ''
        )
    )
    
    # stc 
    df['K'] = (ta.momentum.StochRSIIndicator(close=df['HA_Close']).stochrsi_k().fillna(0) * 100).round(2)
    df['D'] = (ta.momentum.StochRSIIndicator(close=df['HA_Close']).stochrsi_d().fillna(0) * 100).round(2)

    df['Stoch_Cross'] = numpy.where(
        (df['K'] > df['D']) & (df['K'].shift(1) <= df['D'].shift(1)), 'LONG',
        numpy.where(
            (df['K'] < df['D']) & (df['K'].shift(1) >= df['D'].shift(1)), 'SHORT',
            None
        )
    )

    # HA_Close와 EMA200의 차이를 계산
    df['Line_Cross_val'] = (df['HA_Close'] - df['EMA_200']).round(1)

    df['Line_Cross'] = numpy.where(
        (df['HA_Close'] > df['EMA_200']) & (df['HA_Close'].shift(1) <= df['EMA_200'].shift(1)), 'LONG',
        numpy.where(
            (df['HA_Close'] < df['EMA_200']) & (df['HA_Close'].shift(1) >= df['EMA_200'].shift(1)), 'SHORT',
            None
        )
    )
    
    df = impulse_macd(df)
    df = detect_cross_signals(df)
    df = ut_bot_alert(df)
    return df

# if __name__ == "__main__" :
    # symbol = 'BTC/USDT'
    # timeframe = '5m'
    # limit = 400
    # df = fetch_binance_data(symbol=symbol, timeframe=timeframe, limit=limit)

    # symbol = 'KRW-ETH'
    # timeframe = 'minute5'
    # limit = 200

    # df = fetch_upbit_data(symbol=symbol, timeframe=timeframe, limit=limit)
    # df = spider(df)
    # print(df)