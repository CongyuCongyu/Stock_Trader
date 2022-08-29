a stock portfolio trader that makes stock transactions based on three stock indicators: SMA, momentum, and Bollinger Band. 

1. RTLearner.py: Implement a Random Tree learner class
2. BagLearner.py: implement Bootstrap Aggregating as a Python class named BagLearner
3. ManualStrategy.py: Implement a Manual Strategy (manual rule-based trader)
4. StrategyLearner.py: Implement a learner that can learn a trading policy using the learner and the same indicators used in ManualStrategy
5. indicators.py: implements the indicators as functions that operate on DataFrames. The “main” code generates the charts that illustrate indicators in the report.
6. marketsimcode.py: accepts a “trades” DataFrame and calculate the value of the portfolio.
7. experiment1.py: Compare the Manual Strategy with the Strategy Learner in-sample trading JPM
8. experiment2.py: Conduct an experiment with the StrategyLearner that shows how changing the value of impact should affect in-sample trading behavior
9. testproject.py: run all assigned tasks and output all necessary charts and statistics.



To generate all the charts and statistics: in the strategy_evaluation directory, run PYTHONPATH=../:. python testproject.py
Calling testproject.py using the command above should run all assigned tasks and output all necessary charts and statistics.