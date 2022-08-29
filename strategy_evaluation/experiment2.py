import datetime as dt
import StrategyLearner as sl
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt

def plot_experiment_two():
    learner1 = sl.StrategyLearner(verbose=False, impact=0.0005, commission=0.0)  # constructor
    learner1.add_evidence(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),sv=100000)
    df_trades = learner1.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),sv=100000)
    strategy_learner1_portvals = compute_portvals(df_trades, 100000, commission=0, impact=0.0005)

    learner2 = sl.StrategyLearner(verbose=False, impact=0.005, commission=0.0)  # constructor
    learner2.add_evidence(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),sv=100000)
    df_trades = learner2.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),sv=100000)
    strategy_learner2_portvals = compute_portvals(df_trades, 100000, commission=0, impact=0.005)

    learner3 = sl.StrategyLearner(verbose=False, impact=0.05, commission=0.0)  # constructor
    learner3.add_evidence(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),sv=100000)
    df_trades = learner3.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),sv=100000)
    strategy_learner3_portvals = compute_portvals(df_trades, 100000, commission=0, impact=0.05)

    strategy_learner1_portvals = strategy_learner1_portvals / strategy_learner1_portvals.ix[0]
    strategy_learner2_portvals = strategy_learner2_portvals / strategy_learner2_portvals.ix[0]
    strategy_learner3_portvals = strategy_learner3_portvals / strategy_learner3_portvals.ix[0]

    plt.plot(strategy_learner1_portvals, label="impact=0.0005", color="green")
    plt.plot(strategy_learner2_portvals, label="impact=0.005", color="red")
    plt.plot(strategy_learner3_portvals, label="impact=0.05", color="yellow")

    plt.title("in_sample_impact_VS_cumulative_return")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid()
    plt.savefig("in_sample_impact_VS_cumulative_return.png")
    plt.close()

    STDEV = []
    daily_return_learner1 = (strategy_learner1_portvals / strategy_learner1_portvals.shift(1) - 1).iloc[1:]
    STDEV.append(daily_return_learner1.std())
    daily_return_learner2 = (strategy_learner2_portvals / strategy_learner2_portvals.shift(1) - 1).iloc[1:]
    STDEV.append(daily_return_learner2.std())
    daily_return_learner3 = (strategy_learner3_portvals / strategy_learner3_portvals.shift(1) - 1).iloc[1:]
    STDEV.append(daily_return_learner3.std())

    print("The STDEV of the learners with impact from 0.0005 to 0.05 are:", STDEV)

