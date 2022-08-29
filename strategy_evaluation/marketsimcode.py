import pandas as pd
from util import symbol_to_path


def compute_portvals(
        df_trades,
        start_val=100000,
        commission=0,
        impact=0,
):
    def get_close(symbol, date):
        df = pd.read_csv(symbol_to_path(symbol), index_col="Date", parse_dates=True)
        return float(df['Adj Close'][date])

    def calculate_portfolio(portfolio, Date):
        value = 0
        for key in portfolio:
            value = value + get_close(key, Date) * portfolio[key]
        return value

    portfolio = {}
    portfolio_value = pd.DataFrame(columns=["Date", "Value"])
    cash = start_val
    previous_date = "0000-00-00"
    repeat = 1
    df_trades = df_trades.reset_index()

    for index, row in df_trades.iterrows():
        if (row[1] == 0):
            portfolio_value = portfolio_value.append(
                {"Date": str(row[0]), "Value": cash + float(calculate_portfolio(portfolio, row[0]))},
                ignore_index=True)
        else:
            shares = row[1]
            cash = cash - shares * get_close(df_trades.columns[1], row[0]) - commission - shares * get_close(
                df_trades.columns[1], row[0]) * impact
            portfolio[df_trades.columns[1]] = portfolio.get(df_trades.columns[1], 0) + shares
            if (str(row[0]) == previous_date):
                portfolio_value.at[int(index) - repeat, "Value"] = cash + float(
                    calculate_portfolio(portfolio, row[0]))
                previous_date = str(row[0])
                repeat = repeat + 1
            else:
                portfolio_value = portfolio_value.append(
                    {"Date": str(row[0]), "Value": cash + float(calculate_portfolio(portfolio, row[0]))},
                    ignore_index=True)
                previous_date = str(row[0])
    portfolio_value["Date"] = pd.to_datetime(portfolio_value["Date"]).dt.date
    portfolio_value = portfolio_value.set_index("Date")
    return portfolio_value

if __name__ == "__main__":
    print("marketsimcode main")
