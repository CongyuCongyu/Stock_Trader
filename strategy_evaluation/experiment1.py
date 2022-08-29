import datetime as dt
import ManualStrategy as ms
import StrategyLearner as sl
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt

def plot_experiment_one():
    df_trades, buying, selling = ms.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    manual_strategy_portvals = compute_portvals(df_trades, 100000, commission=9.95, impact=0.005)

    learner = sl.StrategyLearner(verbose=False, impact=0.0, commission=0.0)  # constructor
    learner.add_evidence(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),sv=100000)
    df_trades = learner.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),sv=100000)
    strategy_learner_portvals = compute_portvals(df_trades, 100000, commission=9.95, impact=0.005)

    benchmark = df_trades
    benchmark[:]=0.0
    benchmark.ix[0]=1000
    benchmark_portvals = compute_portvals(benchmark, 100000, commission=9.95, impact=0.005)

    benchmark_portvals = benchmark_portvals / benchmark_portvals.ix[0]
    manual_strategy_portvals = manual_strategy_portvals / manual_strategy_portvals.ix[0]
    strategy_learner_portvals = strategy_learner_portvals / strategy_learner_portvals.ix[0]


    plt.plot(benchmark_portvals, label="benchmark", color="green")
    plt.plot(manual_strategy_portvals, label="manual strategy", color="red")
    plt.plot(strategy_learner_portvals, label="strategy learner", color="yellow")

    plt.title("in_sample_manual_strategy_VS_strategy_learner")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid()
    plt.savefig("in_sample_manual_strategy_VS_strategy_learner.png")
    plt.close()



