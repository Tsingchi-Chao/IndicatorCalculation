# IndicatorCalculation
## Indicator.py文件
该文件定义了一个IndicatorCalculator的类，该类包含了计算各个金融常用指标的函数。
指标如下：

年化波动率，年化收益率，累积收益率，夏普比，最大回撤，卡玛比率，年化下行波动率，索提诺比率，skeness,kurtosis,average_Top5MaxDrawdown共计11个金融指标。

## main.py文件
该文件主要是计算各个行业指数滚动60日的金融指标，具体指标即Indicator.py中计算的指标。

计算出指标数值之后，将指标画图并放入pdf中保存至本地。
