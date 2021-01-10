# Zhaoqingzhi 
# 2020-01-10

import pandas as pd
import numpy as np
from scipy.stats.mstats import gmean
import math
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
plt.rc("font",family='YouYuan')
from matplotlib.backends.backend_pdf import PdfPages

class IndicatorCalculator:
    """
     A IndicatorCalculator is used to calculate the indicator of the financial data,including
     annualStd,sharpeRatio,maxDrawdown,calmarRatio,annualDownsideStd,sortinoRatio,skewness,
     kurtosis,averageTop5MaxDrawdown,annualReturn,cumReturn
    """

    def __init__(self,df:pd.DataFrame):
        """
        Args:
              :param df:df from dataframe.
        """
        self.df=df

    def annual_Std(self):
        """
        :return: The annual standard deviation.
        """
        dailyStd = self.df['return'].std()  # 得到日度波动率
        annualStd = dailyStd * math.sqrt(250)  # 得到年化波动率
        return annualStd

    def annual_Return(self):
        """
        :return: Annual return.
        """
        annualReturn = gmean(self.df['return'] + 1) ** 250 - 1  # 得到年化收益率
        return annualReturn

    def cum_Return(self):
        """
        :return: The cumulative return.
        """
        cumReturn=(self.df.loc[self.df.index[-1],'close']-self.df.loc[self.df.index[0],'close'])/self.df.loc[self.df.index[0],'close']
        return cumReturn

    def sharpe_Ratio(self):
        """
        :return:  Sharpe ratio.
        """
        annualReturn=IndicatorCalculator.annual_Return(self)
        annualStd=IndicatorCalculator.annual_Std(self)
        sharpeRatio = annualReturn / annualStd  # 得到夏普比
        return sharpeRatio

    def max_Drawdown(self):
        """
        :return: Max drawdown of the financial series.
        """
        roll_max = self.df['close'].expanding().max()
        maxDrawdown = -1 * np.min(self.df['close'] / roll_max - 1)  # 计算得到最大回撤
        return maxDrawdown

    def calmar_Ratio(self):
        """
        :return: Calmar ratio.
        """
        annualReturn=IndicatorCalculator.annual_Return(self)
        maxDrawdown=IndicatorCalculator.max_Drawdown(self)
        calmarRatio = annualReturn / maxDrawdown
        return calmarRatio

    def annual_DownsideStd(self):
        """
        :return:Annual downside standard deviation.
        """
        num = len(self.df[self.df['return'] < 0]['return'])  # 计算小于0的收益率个数
        dailyDownsideStd = math.sqrt(self.df[self.df['return'] < 0]['return'].apply(lambda x: x * x).sum() / num)  # 计算出日度下行波动率
        annualDownsideStd = dailyDownsideStd * math.sqrt(250)
        return annualDownsideStd

    def sortino_Ratio(self):
        """
        :return: Sortino ratio.
        """
        annualReturn = IndicatorCalculator.annual_Return(self)
        annualDownsideStd=IndicatorCalculator.annual_DownsideStd(self)
        sortinoRatio = annualReturn / annualDownsideStd
        return sortinoRatio

    def skewness(self):
        """
        :return: The skewness of the return.
        """
        return self.df['return'].skew()

    def kurtosis(self):
        """
        :return: The kurtosis of the return.
        """
        return self.df['return'].kurt()

    def average_Top5MaxDrawdown(self):
        """
        :return: The average top 5 max drawdown.
        """
        drawdownList = []  # 定义一个序列，存储不同排名的最大回撤
        for i in range(5):
            # 计算最大回撤
            roll_max = self.df['close'].expanding().max()
            drawdown = -1 * np.min(self.df['close'] / roll_max - 1)  # 计算得到当前阶段最大回撤
            if drawdown <= 0:
                break
            drawdownList.append(drawdown)

            # 找到最大回撤对应的起始index和终止index
            end_point = np.argmin(self.df['close'] / roll_max - 1)
            start_point = np.argmax(self.df['close'][:end_point])

            # 将最大回撤阶段的数据去掉，将两端数据拼接，这里需要处理使得拼接点一致
            df1 = self.df[['close']][:start_point]
            df2 = self.df[['close']][end_point:]
            if not df1.empty and not df2.empty:
                df2['close'] = df2['close'] * (
                            df1.loc[df1.index[-1], 'close'] / df2.loc[df2.index[0], 'close'])  # 将df2的第一个数据与df1的最后一个数据一致
                df = pd.concat([df1, df2])  # 将df1与df2拼接，得到新的df数据
            elif df1.empty and not df2.empty:
                df = df2
            elif not df1.empty and df2.empty:
                df = df1
            elif df1.empty and df2.empty:
                break
        averageTop5MaxDrawdown = pd.Series(drawdownList).mean()
        return averageTop5MaxDrawdown






