"""private Dictionary<string, TradeBarConsolidator> _consolidators;
private Dictionary<string, RollingWindow<TradeBar>> _history;"""

"""public override void Initialize()
{
	SetStartDate(2019, 1, 1);  //Set Start Date
	AddForex(“EURGBP”, Resolution.Minute);

	_consolidators = new Dictionary<string, TradeBarConsolidator>
	{
		{ “1H”,  new TradeBarConsolidator(TimeSpan.FromMinutes(60)) },
		{ “6H”,  new TradeBarConsolidator(TimeSpan.FromMinutes(360)) },
	};

	_histroy = new Dictionary<string, RollingWindow<TradeBar>>
	{
		{ “1H”,  new RollingWindow<TradeBar>(50) },
		{ “6H”,  new RollingWindow<TradeBar>(20) },
	};


	{
		_consolidators[kvp.Key].DataConsolidated += (s, e) => _history[kvp.Key].Add(e);
		SubscriptionManager.AddConsolidator(“EURGBP”, kvp.Value);
	}


	foreach (var data in History(“EURGBP”, TimeSpan.FromDays(30)))
	{
		foreach (var consolidator in _consolidators.Values)
		{
			consolidator.Update(dta);
		}
	}


_consolidators[“1H”].DataConsolidated += On1HData;
}"""

"""If we want to access the close price 22 bars ago of the 1H timeframe: - so from here can take data and calc RSI

var value = _history[“1H”][22].Close;"""
