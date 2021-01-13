#author:Zhaoqingzhi
#date:2021-01-13


import pandas as pd
import numpy as np
from scipy.stats.mstats import gmean
import math
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
plt.rc("font",family='YouYuan')
from matplotlib.backends.backend_pdf import PdfPages
import Indicator as Ind

def Indicator_calculation(dic_windCode:dict)->pd.DataFrame:
    """
    Args:
        dic_windCode(dict):A dictionary whose key,value is the name of industry and dataframe.The dataframe should include 'return' and
    'close' two columns.

    Returns:
        pd.Dataframe:A dataframe that includes the indicators.
    """
    df=pd.read_excel(r'./数据/新能源指数.xlsx',index_col=0)#日期以新能源指数为标准，因为新能源指数最晚
    dataIndicators=pd.DataFrame()#建立存储计算出的指标的结果的dataframe
    for count in range(59,len(df)):#开始遍历，一直到最后
        print(count,end=' ')
        start_date=df.index[count-59]
        end_date=df.index[count]
        for key in dic_windCode.keys():
            data=dic_data[key]
            try:
                data=data.loc[start_date:end_date,:]
                ind = Ind.IndicatorCalculator(data)
                dataIndicators.loc[end_date,key+'sharpeRatio']=ind.sharpe_Ratio()
                dataIndicators.loc[end_date,key+'calmarRatio']=ind.calmar_Ratio()
                dataIndicators.loc[end_date,key+'sortinoRatio']=ind.sortino_Ratio()
                dataIndicators.loc[end_date,key+'maxDrawdown']=ind.max_Drawdown()
                dataIndicators.loc[end_date,key+'downsideStd']=ind.annual_DownsideStd()
                dataIndicators.loc[end_date,key+'annualStd']=ind.annual_Std()
                dataIndicators.loc[end_date,key+'skewness']=ind.skewness()
                dataIndicators.loc[end_date,key+'kurtosis']=ind.kurtosis()
                dataIndicators.loc[end_date,key+'averageTop5MaxDrawdown']=ind.average_Top5MaxDrawdown()
                dataIndicators.loc[end_date,key+'annualReturn']=ind.annual_Return()
                dataIndicators.loc[end_date,key+'cumReturn']=ind.cum_Return()
            except:
                print(key,end=' ')
                continue
    return dataIndicators


def Draw_picture(dataIndicators:pd.DataFrame,dic_windCode:dict,path):
    """
    Args:
        dataIndicators(pd.DataFrame):It's the dataframe that includes the indicators.
        dic_windCode(dict):A dictionary whose key,value is the name of industry and dataframe.The dataframe should include 'return' and
    'close' two columns.
        path: The path of the pdf that will be saved.

    Returns:
        The pdf that includes the pictures will be saved according to the path.
    """
    with PdfPages(path) as pdf:
        for industry in list(dic_windCode.keys())[4:]:
            indicators = ['annualReturn', 'cumReturn', 'sharpeRatio', 'maxDrawdown', 'calmarRatio', 'downsideStd',
                          'sortinoRatio', 'skewness', 'kurtosis', 'averageTop5MaxDrawdown']
            plt.figure(dpi=200, figsize=(20, 20))
            plt.suptitle(industry, fontsize=40, fontweight='bold')
            for i in range(10):
                plt.subplot(5, 2, i + 1)
                plt.plot(dataIndicators['中证500' + indicators[i]], c='y', linestyle='--', label='中证500')
                plt.plot(dataIndicators['沪深300' + indicators[i]], c='purple', linestyle='--', label='沪深300')
                plt.plot(dataIndicators['创业板指' + indicators[i]], c='g', label='创业板指')
                plt.plot(dataIndicators['上证50' + indicators[i]], c='b', label='上证50')
                plt.plot(dataIndicators[industry + indicators[i]], c='r', label=industry)
                plt.title(indicators[i])
                plt.legend()
            pdf.savefig()
            plt.close()


def main():
    industry=['中证500','沪深300','上证50','创业板指','农林牧渔','采掘','化工','钢铁','有色金属','电子','家用电器','食品饮料',
             '纺织服装','轻工制造','医药生物','公用事业','交通运输','房地产','商业贸易','休闲服务','综合','建筑材料','建筑装饰','电气设备',
             '国防军工','计算机','传媒','通信','银行','非银金融','汽车','机械设备','新能源汽车指数','新能源指数']
    windCode=['000905.SH','000300.SH','000016.SH','399006.SZ','801010.SI','801020.SI','801030.SI','801040.SI','801050.SI',
              '801080.SI','801110.SI','801120.SI','801130.SI','801140.SI','801150.SI','801160.SI','801170.SI', '801180.SI','801200.SI',
              '801210.SI','801230.SI','801710.SI','801720.SI','801730.SI','801740.SI','801750.SI','801760.SI','801770.SI,',
               '801780.SI','801790.SI','801880.SI','801890.SI','884076.WI','884035.WI']
    dic_windCode=dict(zip(industry, windCode))
    dataIndicators = pd.read_excel(r'./计算结果/全行业指标_60.xlsx', index_col=0)
    path='./画图结果/全行业指标计算_60.pdf'
    Draw_picture(dataIndicators,dic_windCode,path)

if __name__=="__main__":
    main()


