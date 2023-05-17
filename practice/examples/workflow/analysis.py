import pandas as pd
import matplotlib.pyplot as plt
import os
import practice
from practice.frameworks import api
from practice.finance import technical_analysis as ta
import matplotlib; matplotlib.use("TkAgg")


HERE = "practice.examples.workflow.analysis"


class Analysis1(api.Workflow):
    """ Generates a timeseries plot of JPM's stock price """
    TASKS = [
        [0, f"{HERE}.getQuandlData", "ticker", {}, "data"],
        [1, f"{HERE}.toDatetime", ("data", "dateCol"), {}, "dates"],
        [1, f"{HERE}.getColumn", ("data",), {"column": "Close"}, "price"],
        [2, f"{HERE}.plot", ("dates", "price"),
             { "xlabel"  : "Date",
               "ylabels" : ("Price",),
               "title"   : "Price vs Time", },
         "fig"],
    ]

class Analysis2(api.Workflow):
    """ Generates a timeseries plot of JPM's stock price during the 2008 recession """
    TASKS = [
        [0, f"{HERE}.getQuandlData", "ticker", {}, "data"],
        [1, f"{HERE}.toDatetime", ("data", "dateCol"), {}, "dates"],
        [2, f"{HERE}.getDateMask", ("dates", "start", "end"), {}, "dateMask"],
        [3, f"{HERE}.getColumn", ("data",), {"column": "Close"}, "price"],
        [4, f"{HERE}.applyMask", ("dates", "dateMask"), {}, "datesSliced"],
        [4, f"{HERE}.applyMask", ("price", "dateMask"), {}, "priceSliced"],
        [5, f"{HERE}.plot", ("datesSliced", "priceSliced"),
             { "xlabel"  : "Date",
               "ylabels" : ("Price",),
               "title"   : "Price vs Time during the 2008 Recession", },
         "fig"],
    ]

class Analysis3(api.Workflow):
    """ Generates a simple moving average of JPM's stock price during the 2008 recession """
    TASKS = [
        [0, f"{HERE}.getQuandlData", "ticker", {}, "data"],
        [1, f"{HERE}.toDatetime", ("data", "dateCol"), {}, "dates"],
        [2, f"{HERE}.getDateMask", ("dates", "start", "end"), {}, "dateMask"],
        [3, f"{HERE}.getColumn", ("data",), {"column": "Close"}, "price"],
        [4, f"{HERE}.applyMask", ("dates", "dateMask"), {}, "datesSliced"],
        [4, f"{HERE}.applyMask", ("price", "dateMask"), {}, "priceSliced"],
        [5, f"{ta.__name__}.simpleMA", ("priceSliced", "longWindow"), {}, "longSMA"],
        [5, f"{ta.__name__}.simpleMA", ("priceSliced", "shortWindow"), {}, "shortSMA"],
        [6, f"{ta.__name__}.crossover", ("shortSMA", "longSMA", "crossWindow"), {}, "crossSMA"],
        [7, f"{HERE}.plot", ("datesSliced", "priceSliced", "longSMA", "shortSMA", "crossSMA"),
         { "xlabel"  : "Date",
           "ylabels" : ("Price", "longSMA", "shortSMA", "crossover"),
           "title"   : "SMA Crossover System during the 2008 Recession", },
         "fig"],
    ]


def getQuandlData(ticker):
    import quandl
    DF = quandl.get(ticker)
    return DF.reset_index(drop=False)

def getDateMask(dates, start, end):
    """ generates a mask for records within a date range  """
    mask  = dates >= start
    mask &= dates <= end
    return mask

def applyMask(data, mask):
    """ applies a mask to data """
    return data[mask].reset_index(drop=True)

def getColumn(data, column=""):
    """ gets a column from data """
    return data[column]

def toDatetime(data, column):
    """ converts to datetime """
    return pd.to_datetime(data[column])

def plot(x, *values, ylabels=(), xlabel="", title=""):
    """ plots timeseries data """
    plt.ioff()
    fig, ax = plt.subplots()
    fig.suptitle(title)
    fig.autofmt_xdate()
    ax.grid()
    ax.set_xlabel(xlabel)

    for ylabel, value in zip(ylabels, values):
        ax.plot(x, value, label=ylabel)

    if len(values) > 1:
        ax.legend()
    else:
        ax.set_ylabel(ylabels[0])

    return fig


if __name__ == "__main__":

    def driver(data, workflow):
        """ drives a workflow """
        dag = workflow.asDag()
        dag.view()

        results = workflow.run(data)

        fig = results["fig"]
        fig.show()
        return results


    # == Run Analysis 1 ==
    workflow = Analysis1.create()
    data = {
        "ticker"   : "WIKI/JPM",
        "dateCol"  : "Date",
        "valueCol" : "Close", }
    results1 = driver(data, workflow)


    # == Run Analysis 2 ==
    workflow = Analysis2.create()
    data = {
        "ticker"   : "WIKI/JPM",
        "dateCol"  : "Date",
        "valueCol" : "Close",
        "start"    : pd.to_datetime("2007-01-01"),
        "end"      : pd.to_datetime("2009-12-31"), }
    results2 = driver(data, workflow)


    # == Run Analysis 3 ==
    workflow = Analysis3.create()
    data = {
        "ticker"      : "WIKI/JPM",
        "dateCol"     : "Date",
        "valueCol"    : "Close",
        "start"       : pd.to_datetime("2007-01-01"),
        "end"         : pd.to_datetime("2009-12-31"),
        "longWindow"  : 50,
        "shortWindow" : 15,
        "crossWindow" : 1,
    }
    results3 = driver(data, workflow)
