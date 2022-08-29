import datetime as dt
import pandas as pd
from util import get_data
import numpy as np
import matplotlib.pyplot as plt

def SMA(sd, ed, symbols,lookback):
    price = get_data(symbols, pd.date_range(sd, ed))
    price.fillna(method="ffill", inplace=True)
    price.fillna(method="bfill", inplace=True)
    price = price.drop(columns=["SPY"])
    price = price/price.ix[0,]

    sma = price.cumsum()
    sma.values[lookback:,:] = (sma.values[lookback:,:]-sma.values[:-lookback,:])/lookback
    sma.ix[:lookback,:] = np.nan

    price_on_sma = sma.copy(deep=True)
    for day in range(lookback,price.shape[0]):
        for symbol in symbols:
            sma.ix[day,symbol]=price.ix[day,symbol]/sma.ix[day,symbol]
    return price_on_sma


def BB(sd, ed, symbols,lookback):
    price = get_data(symbols, pd.date_range(sd, ed))
    price.fillna(method="ffill", inplace=True)
    price.fillna(method="bfill", inplace=True)
    price = price.drop(columns=["SPY"])
    price = price/price.ix[0,]

    sma = price.cumsum()
    sma.values[lookback:,:] = (sma.values[lookback:,:]-sma.values[:-lookback,:])/lookback
    sma.ix[:lookback,:] = np.nan
    rolling_std = price.rolling(window=lookback,min_periods=lookback).std()
    top_band = sma+(2*rolling_std)
    bottom_band = sma-(2*rolling_std)
    bbp = (price-bottom_band)/(top_band-bottom_band)
    return bbp


def momentum(sd,ed,symbols,lookback):
    price = get_data(symbols, pd.date_range(sd, ed))
    price.fillna(method="ffill", inplace=True)
    price.fillna(method="bfill", inplace=True)
    price = price.drop(columns=["SPY"])
    price = price/price.ix[0,]
    momentum = price / price.shift(periods=lookback) - 1
    momentum = pd.DataFrame(data=momentum.ix[:, 0])
    return momentum

def ema(sd, ed, symbols, lookback):

    delta = dt.timedelta(lookback * 2)
    extedned_sd = sd - delta
    price = get_data(symbols, pd.date_range(extedned_sd, ed))
    price = price[symbols]
    price.fillna(method="ffill", inplace=True)
    price.fillna(method="bfill", inplace=True)
    ema = price.ewm(span=lookback, adjust=False).mean()
    ema = ema.truncate(before=sd)
    price = price.truncate(before=sd)
    normalized_price = price[symbols[0]] / price[symbols[0]][0]
    normalized_ema = ema[symbols[0]] / ema[symbols[0]][0]
    return normalized_price, normalized_ema

def macd(sd, ed, symbols):
    delta = dt.timedelta(52)
    extedned_sd = sd - delta
    price = get_data(symbols, pd.date_range(extedned_sd, ed))
    price = price[symbols]
    price.fillna(method="ffill", inplace=True)
    price.fillna(method="bfill", inplace=True)
    ema_12 = price.ewm(span=12, adjust=False).mean()
    ema_26 = price.ewm(span=26, adjust=False).mean()
    macd_raw = ema_12 - ema_26
    macd_signal = macd_raw.ewm(span=9, adjust=False).mean()
    macd_raw = macd_raw.truncate(before=sd)
    macd_signal = macd_signal.truncate(before=sd)
    return macd_raw, macd_signal


def plot_indicators():
    symbols = ["JPM"]
    lookback = 14
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)

    price, sma, price_on_sma = SMA(sd, ed, symbols,lookback)
    plt.plot(price, label="Price")
    plt.plot(sma, label="SMA")
    plt.plot(price_on_sma, label="Price/SMA")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Price/SMA(14 days)")
    plt.legend()
    plt.grid()
    plt.savefig("SMA.png")
    plt.close()

    upper_band, lower_band, bbp = BB(sd, ed, symbols, lookback)
    plt.plot(price, label="Price")
    plt.plot(upper_band, label="Upper_band")
    plt.plot(lower_band, label="Bottom_band")
    plt.plot(bbp, label = "BBP")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("BBP(14 days)")
    plt.legend()
    plt.grid()
    plt.savefig("BBP.png")
    plt.close()

    Momentum = momentum(sd, ed, symbols, lookback)
    plt.plot(Momentum, label="momentum")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("momentum(14 days)")
    plt.legend()
    plt.grid()
    plt.savefig("momentum.png")
    plt.close()
    
    normalized_price, normalized_ema = ema(sd, ed, symbols, lookback)
    plt.plot(normalized_price, label="Price")
    plt.plot(normalized_ema, label="EMA")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("EMA(14 days)")
    plt.legend()
    plt.grid()
    plt.savefig("EMA.png")
    plt.close()

    macd_raw, macd_signal = macd(sd, ed, symbols)
    plt.plot(macd_raw, label="MACD_RAW")
    plt.plot(macd_signal, label="MACD_SIGNAL")
    plt.xlabel("Date")
    plt.xlabel("fold")
    plt.title("MACD")
    plt.legend()
    plt.grid()
    plt.savefig("MACD.png")
    plt.close()


if __name__ == "__main__":
    plot_indicators()