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
        [0, f"{HERE}.getFilepath", "ticker", {}, "filepath"],
        [1, f"{pd.__name__}.read_csv", "filepath", {}, "data"],
        [2, f"{HERE}.toDatetime", ("data", "dateCol"), {}, "dates"],
        [2, f"{HERE}.getColumn", ("data",), {"column": "Close"}, "price"],
        [3, f"{HERE}.plot", ("dates", "price"),
             { "xlabel"  : "Date",
               "ylabels" : ("Price",),
               "title"   : "Price vs Time", },
         "fig"],
    ]

class Analysis2(api.Workflow):
    """ Generates a timeseries plot of JPM's stock price during the great recession """
    TASKS = [
        [0, f"{HERE}.getFilepath", "ticker", {}, "filepath"],
        [1, f"{pd.__name__}.read_csv", "filepath", {}, "data"],
        [2, f"{HERE}.toDatetime", ("data", "dateCol"), {}, "dates"],
        [3, f"{HERE}.getDateMask", ("dates", "start", "end"), {}, "dateMask"],
        [4, f"{HERE}.getColumn", ("data",), {"column": "Close"}, "price"],
        [5, f"{HERE}.applyMask", ("dates", "dateMask"), {}, "datesSliced"],
        [5, f"{HERE}.applyMask", ("price", "dateMask"), {}, "priceSliced"],
        [6, f"{HERE}.plot", ("datesSliced", "priceSliced"),
             { "xlabel"  : "Date",
               "ylabels" : ("Price",),
               "title"   : "Price vs Time during the Great Recession", },
         "fig"],
    ]


class Analysis3(api.Workflow):
    """ Generates a simple moving average of JPM's stock price during the great recession """
    TASKS = [
        [0, f"{HERE}.getFilepath", "ticker", {}, "filepath"],
        [1, f"{pd.__name__}.read_csv", "filepath", {}, "data"],
        [2, f"{HERE}.toDatetime", ("data", "dateCol"), {}, "dates"],
        [3, f"{HERE}.getDateMask", ("dates", "start", "end"), {}, "dateMask"],
        [4, f"{HERE}.getColumn", ("data",), {"column": "Close"}, "price"],
        [5, f"{HERE}.applyMask", ("dates", "dateMask"), {}, "datesSliced"],
        [5, f"{HERE}.applyMask", ("price", "dateMask"), {}, "priceSliced"],
        [6, f"{ta.__name__}.simpleMA", ("priceSliced", "longWindow"), {}, "longSMA"],
        [6, f"{ta.__name__}.simpleMA", ("priceSliced", "shortWindow"), {}, "shortSMA"],
        [7, f"{HERE}.plot", ("datesSliced", "priceSliced", "longSMA", "shortSMA"),
         { "xlabel"  : "Date",
           "ylabels" : ("Price", "longSMA", "shortSMA"),
           "title"   : "Simple Moving Averages (SMAs) during the Great Recession", },
         "fig"],
    ]


class Analysis4(api.Workflow):
    """ Generates a exponential moving average of JPM's stock price during the great recession """
    TASKS = [
        [0, f"{HERE}.getFilepath", "ticker", {}, "filepath"],
        [1, f"{pd.__name__}.read_csv", "filepath", {}, "data"],
        [2, f"{HERE}.toDatetime", ("data", "dateCol"), {}, "dates"],
        [3, f"{HERE}.getDateMask", ("dates", "start", "end"), {}, "dateMask"],
        [4, f"{HERE}.getColumn", ("data",), {"column": "Close"}, "price"],
        [5, f"{HERE}.applyMask", ("dates", "dateMask"), {}, "datesSliced"],
        [5, f"{HERE}.applyMask", ("price", "dateMask"), {}, "priceSliced"],
        [6, f"{ta.__name__}.expMA", ("priceSliced", "longWindow"), {}, "longEMA"],
        [6, f"{ta.__name__}.expMA", ("priceSliced", "shortWindow"), {}, "shortEMA"],
        [7, f"{HERE}.plot", ("datesSliced", "priceSliced", "longEMA", "shortEMA"),
         { "xlabel"  : "Date",
           "ylabels" : ("Price", "longEMA", "shortEMA"),
           "title"   : "Exponential Moving Averages (EMAs) during the Great Recession", },
         "fig"],
    ]



def getFilepath(ticker):
    """ gets the filepath for a given ticker """
    relpath  = f"practice/data/{ticker.lower()}.csv.gz"
    parts    = [os.path.dirname(practice.__file__), ".."]
    parts   += relpath.split("/")
    return os.path.join(*parts)


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
        w = workflow.create()
        dag = w.buildDag()
        dag.view()

        results = w.run(data)
        fig = results["fig"]
        fig.show()
        return results


    data = {
        "ticker"   : "jpm",
        "dateCol"  : "Date",
        "valueCol" : "Close", }
    results1 = driver(data, Analysis1)


    data = {
        "ticker"   : "jpm",
        "dateCol"  : "Date",
        "valueCol" : "Close",
        "start"    : pd.to_datetime("2007-01-01"),
        "end"      : pd.to_datetime("2009-12-31"), }
    results2 = driver(data, Analysis2)


    data = {
        "ticker"      : "jpm",
        "dateCol"     : "Date",
        "valueCol"    : "Close",
        "start"       : pd.to_datetime("2007-01-01"),
        "end"         : pd.to_datetime("2009-12-31"),
        "longWindow"  : 30,
        "shortWindow" : 5, }
    results3 = driver(data, Analysis3)

    data = {
        "ticker"      : "jpm",
        "dateCol"     : "Date",
        "valueCol"    : "Close",
        "start"       : pd.to_datetime("2007-01-01"),
        "end"         : pd.to_datetime("2009-12-31"),
        "longWindow"  : 30,
        "shortWindow" : 5, }

    results4 = driver(data, Analysis4)
