import datetime as dt
import pandas as pd
import util as ut
import indicators
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt


def testPolicy(
        symbol="IBM",
        sd=dt.datetime(2008, 1, 1),
        ed=dt.datetime(2009, 12, 31),
        sv=10000,
):
    syms = [symbol]
    lookback = 14
    dates = pd.date_range(sd, ed)
    prices_all = ut.get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols

    price_on_sma = indicators.SMA(sd, ed, syms, lookback)
    bbp = indicators.BB(sd, ed, syms, lookback)
    normalized_price, normalized_ema = indicators.ema(sd, ed, syms, lookback)
    ema_minus_price = normalized_ema - normalized_price

    three_indicators = pd.concat((price_on_sma, bbp, ema_minus_price), axis=1)
    three_indicators.columns = ['price_on_sma', 'bbp', 'ema_minus_price']
    three_indicators.fillna(0, inplace=True)
    df_trades = prices.copy(deep=True)
    position = 0
    selling = []
    buying = []

    for i in range(df_trades.shape[0]):
        if (three_indicators.ix[i,"price_on_sma"] ==0
            and three_indicators.ix[i,"bbp"] ==0):
            df_trades.ix[i] = 0
        elif (three_indicators.ix[i,"price_on_sma"]<0.99
            and three_indicators.ix[i,"bbp"]<0.2 and
            three_indicators.ix[i,"ema_minus_price"]>0.01):
            if(position!=1000):
                buying.append(df_trades.index[i])
            df_trades.ix[i] = 1000 - position
            position = 1000

        elif (three_indicators.ix[i,"price_on_sma"]>1.01
            and three_indicators.ix[i,"bbp"]>0.8 and
            three_indicators.ix[i,"ema_minus_price"]<-0.01):
            if(position!=-1000):
                selling.append(df_trades.index[i])
            df_trades.ix[i] = -1000 - position
            position = -1000

        else:
            df_trades.ix[i] = 0
    df_trades.ix[-1] = 0
    return df_trades, buying, selling

def manual_strategy_plot():
    df_trades, buying, selling = testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    manual_strategy_portvals = compute_portvals(df_trades, 100000, commission=9.95, impact=0.005)

    benchmark = df_trades
    benchmark[:]=0.0
    benchmark.ix[0]=1000
    benchmark_portvals = compute_portvals(benchmark, 100000, commission=9.95, impact=0.005)

    benchmark_portvals = benchmark_portvals / benchmark_portvals.ix[0]
    manual_strategy_portvals = manual_strategy_portvals / manual_strategy_portvals.ix[0]

    plt.plot(benchmark_portvals, label="benchmark", color="green")
    plt.plot(manual_strategy_portvals, label="manual strategy", color="red")
    for i in buying:
        plt.axvline(x=i, color ='blue')
    for i in selling:
        plt.axvline(x=i, color='black')
    plt.title("in_sample_manual_strategy_VS_benchmark")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid()
    plt.savefig("in_sample_manual_strategy_VS_benchmark.png")
    plt.close()

    cumulative_return = []
    cumulative_return.append(benchmark_portvals.ix[-1]/benchmark_portvals.ix[0]-1)
    cumulative_return.append(manual_strategy_portvals.ix[-1]/manual_strategy_portvals.ix[0]-1)

    STDEV = []
    daily_return_benchmark = (benchmark_portvals / benchmark_portvals.shift(1) - 1).iloc[1:]
    STDEV.append(daily_return_benchmark.std())
    manual_strategy_portvals = (manual_strategy_portvals / manual_strategy_portvals.shift(1) - 1).iloc[1:]
    STDEV.append(manual_strategy_portvals.std())

    MEAN = []
    MEAN.append(daily_return_benchmark.mean())
    MEAN.append(manual_strategy_portvals.mean())


    df_trades, buying, selling = testPolicy(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)
    manual_strategy_portvals = compute_portvals(df_trades, 100000, commission=9.95, impact=0.005)
    benchmark = df_trades
    benchmark[:]=0.0
    benchmark.ix[0]=1000
    benchmark_portvals = compute_portvals(benchmark, 100000, commission=9.95, impact=0.005)
    benchmark_portvals = benchmark_portvals / benchmark_portvals.ix[0]
    manual_strategy_portvals = manual_strategy_portvals / manual_strategy_portvals.ix[0]

    plt.plot(benchmark_portvals, label="benchmark", color="green")
    plt.plot(manual_strategy_portvals, label="manual strategy", color="red")
    for i in buying:
        plt.axvline(x=i, color ='blue')
    for i in selling:
        plt.axvline(x=i, color='black')
    plt.title("out_sample_manual_strategy_VS_benchmark")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid()
    plt.savefig("out_sample_manual_strategy_VS_benchmark.png")
    plt.close()

    cumulative_return.append(benchmark_portvals.ix[-1]/benchmark_portvals.ix[0]-1)
    cumulative_return.append(manual_strategy_portvals.ix[-1]/manual_strategy_portvals.ix[0]-1)
    daily_return_benchmark = (benchmark_portvals / benchmark_portvals.shift(1) - 1).iloc[1:]
    STDEV.append(daily_return_benchmark.std())
    manual_strategy_portvals = (manual_strategy_portvals / manual_strategy_portvals.shift(1) - 1).iloc[1:]
    STDEV.append(manual_strategy_portvals.std())
    MEAN.append(daily_return_benchmark.mean())
    MEAN.append(manual_strategy_portvals.mean())

    stat_table = []
    stat_table.append(cumulative_return)
    stat_table.append(STDEV)
    stat_table.append(MEAN)
    print("The stats table is:",stat_table)


if __name__ == "__main__":
    print("ManualStrategy main")
