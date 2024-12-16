from .Trading_Data_Stream import Trading_Data_Stream
from .Fetch_Trading_Data import Fetch_Trading_Data
from datetime import datetime
from .FiinIndicator import _FiinIndicator
from typing import Union
from .DateCorr import FindDateCorrelation
import pandas as pd

class FiinSession:
    def __init__(self, username: str, password: str):...

    def login(self) -> FiinSession: ...
   
    def FiinIndicator(self) -> _FiinIndicator: ...
    
    def Trading_Data_Stream(self, 
                        tickers: list, 
                        callback: callable) -> Trading_Data_Stream: ...
    # """Using this class to stream real-time stock market matching data """
    
    def Fetch_Trading_Data(self,
                 realtime: bool,
                 tickers: list, 
                 fields:list, 
                 adjusted: bool, 
                 period:Union[int, None] = None, 
                 by:str = '1M',
                 from_date: Union[str, datetime, None] = None,
                 to_date: Union[str, datetime, None] = None,
                 callback: callable = None,
                 wait_for_full_timeFrame: bool = False) -> Fetch_Trading_Data: ...

    def FindDateCorrelation (self) -> FindDateCorrelation: ...


class RealTimeData:
    """RealTimeData is a class that represents a real-time data of a stock. This class is 
    a structure that contains all the information of a stock at a specific time. You can use 
    to_dataFrame() method to convert this class to a pandas DataFrame."""
    def __init__(self, data: pd.DataFrame) -> None:
        self.__private_attribute = data
        self.Ticker: str
        self.TotalMatchVolume: int
        self.MarketStatus: str
        self.TradingDate: str
        self.ComGroupCode: str
        self.ReferencePrice: float
        self.Open: float
        self.Close: float
        self.High: float
        self.Low: float
        self.Change: float
        self.ChangePercent: float
        self.MatchVolume: int
        self.MatchValue: float
        self.TotalMatchValue: float
        self.TotalBuyTradeVolume: int
        self.TotalSellTradeVolume: int
        self.TotalDealVolume: int
        self.TotalDealValue: float
        self.ForeignBuyVolumeTotal: int
        self.ForeignBuyValueTotal: float
        self.ForeignSellVolumeTotal: int
        self.ForeignSellValueTotal: float
        
    def to_dataFrame(self) -> pd.DataFrame: ...
    
class BarDataUpdate:
    """This class is used to store both the real-time data and the historical data of a stock. You can use to_dataFrame() method to convert this data to a pandas.
    """
    def __init__(self, data) -> None:
        self.__private_attribute: pd.DataFrame
        self.Timestamp: Union[str, datetime]
        self.Open: float
        self.High: float
        self.Low: float
        self.Close: float
        self.Volume: int
        self.Ticker: str 
        self.BU: int
        self.SD: int
        self.FB: float
        self.FS: float
        self.FN: float
    def to_dataFrame(self) -> pd.DataFrame: ...


    


