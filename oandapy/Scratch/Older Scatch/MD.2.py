"""from Alphas.RsiAlphaModel import RsiAlphaModel


class RSIAlgorithm(QCAlgorithm):

    def Initialize(self):

    self.SetStartDate(2017, 1, 1)
    self.SetEndDate(2018, 1, 1)
    self.SetCash(10000)

    RSI_Period = 14
    self.RSI_OB = 68
    self.RSI_OS = 33
    self.Allocate = 0.25

    Currency_Pairs = EURGBP


for each(var pair in _currencyPairs)
{
    AddForex(pair, Resolution.Minute);
RSIDay[pair] = new
Dictionary < string, ExponentialMovingAverage > ();
RSIHour[pair] = new
Dictionary < string, ExponentialMovingAverage > ();
M[pair] = new
Dictionary < string, Momentum > ();
}"""