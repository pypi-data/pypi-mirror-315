import pandas as pd


class Econ:
    def __init__(self, data):

        self.defId = [int(i.get('defId')) for i in data]
        self.srcId = [int(i.get('srcId')) for i in data]
        self.regionId = [float(i.get('regionId')) for i in data]
        self.publishDateTime = [i.get('publishDateTime') for i in data]
        self.publishDate = [i.get('publishDate') for i in data]
        self.unit = [i.get('unit') for i in data]
        self.priorValue = [
            float(i.get('priorValue', '0').replace('%', '')) if i.get('priorValue') else 0.0
            for i in data
        ]

        self.period = [i.get('period') for i in data]
        self.source = [i.get('source') for i in data]
        self.type = [i.get('type') for i in data]
        self.name = [i.get('name') for i in data]
        self.indicatorType = [i.get('indicatorType') for i in data]
        self.frequency = [i.get('frequency') for i in data]
        self.fxType = [i.get('fxType') for i in data]
        self.regionCode = ['regionCode' for i in data]
        self.frequencyName = [i.get('frequencyName') for i in data]



        self.data_dict = { 
            'def_id': self.defId,
            'src_id': self.srcId,
            'region_id': self.regionId,
            'publish_time': self.publishDateTime,
            'publish_date': self.publishDate,
            'unit': self.unit,
            'prior_value': self.priorValue,
            'period': self.period,
            'source': self.source,
            'type': self.type,
            'name': self.name,
            'indicator_type': self.indicatorType,
            'frequency': self.frequency,
            'fx_type': self.fxType,
            'region_code': self.regionCode,
            'frequency_name': self.frequencyName
        }


        self.as_dataframe = pd.DataFrame(self.data_dict)



class EarningsSurprises:
    def __init__(self, ticker, values):
        self.tickerId = [int(i.get('tickerId')) for i in ticker]
        self.name = [i.get('name') for i in ticker]
        self.symbol = [i.get('symbol') for i in ticker]
        self.tradeTime = [i.get('tradeTime') for i in ticker]
        self.close = [float(i.get('close')) for i in ticker]
        self.change = [float(i.get('change')) for i in ticker]
        self.changeRatio = [round(float(i.get('changeRatio'))*100,2) for i in ticker]
        self.marketValue = [float(i.get('marketValue')) for i in ticker]
        self.volume = [float(i.get('volume')) for i in ticker]
        self.turnoverRate = [float(i.get('turnoverRate')) for i in ticker]
        self.peTtm = [float(i.get('peTtm')) for i in ticker]
        self.dividend = [float(i.get('dividend')) for i in ticker]
        self.preClose = [float(i.get('preClose')) for i in ticker]
        self.fiftyTwoWkHigh = [float(i.get('fiftyTwoWkHigh')) for i in ticker]
        self.fiftyTwoWkLow = [float(i.get('fiftyTwoWkLow')) for i in ticker]
        self.open = [float(i.get('open')) for i in ticker]
        self.high = [float(i.get('high')) for i in ticker]
        self.low = [float(i.get('low')) for i in ticker]
        self.vibrateRatio = [float(i.get('vibrateRatio')) for i in ticker]
        self.ask_price = [float(i.get('askPrice')) if i.get('askPrice') is not None else 0.0 for i in ticker]
        self.bid_price = [float(i.get('bidPrice')) if i.get('bidPrice') is not None else 0.0 for i in ticker]



        self.tickerId = [float(i.get('tickerId')) for i in values]
        self.surpriseRatio = [float(i.get('surpriseRatio')) for i in values]
        self.afterLast = [float(i.get('afterLast')) for i in values]
        self.fiscalYear = [float(i.get('fiscalYear')) for i in values]
        self.quarter = [i.get('quarter') for i in values]
        self.releaseDate = [i.get('releaseDate') for i in values]
        self.eps = [float(i.get('eps')) for i in values]


        self.data_dict = {
            "ticker_id": [int(i.get('tickerId')) for i in ticker],
            "name": [i.get('name') for i in ticker],
            "symbol": [i.get('symbol') for i in ticker],
            "trade_time": [i.get('tradeTime') for i in ticker],
            "close": [float(i.get('close')) for i in ticker],
            "change": [float(i.get('change')) for i in ticker],
            "change_ratio": [round(float(i.get('changeRatio')) * 100, 2) for i in ticker],
            "market_value": [float(i.get('marketValue')) for i in ticker],
            "volume": [float(i.get('volume')) for i in ticker],
            "turnover_rate": [float(i.get('turnoverRate')) for i in ticker],
            "pe_ttm": [float(i.get('peTtm')) for i in ticker],
            "dividend": [float(i.get('dividend')) for i in ticker],
            "pre_close": [float(i.get('preClose')) for i in ticker],
            "fifty_high": [float(i.get('fiftyTwoWkHigh')) for i in ticker],
            "fifty_low": [float(i.get('fiftyTwoWkLow')) for i in ticker],
            "open": [float(i.get('open')) for i in ticker],
            "high": [float(i.get('high')) for i in ticker],
            "low": [float(i.get('low')) for i in ticker],
            "vibrate_ratio": [float(i.get('vibrateRatio')) for i in ticker],
            "ask_price": [float(i.get('askPrice')) if i.get('askPrice') is not None else 0.0 for i in ticker],
            "bid_price": [float(i.get('bidPrice')) if i.get('bidPrice') is not None else 0.0 for i in ticker],
            "surprise_ratio": [float(i.get('surpriseRatio')) for i in values],
            "after_last": [float(i.get('afterLast')) for i in values],
            "fiscal_year": [float(i.get('fiscalYear')) for i in values],
            "quarter": [i.get('quarter') for i in values],
            "release_date": [i.get('releaseDate') for i in values],
            "eps": [float(i.get('eps')) for i in values],
        }


        self.as_dataframe = pd.DataFrame(self.data_dict)


class Alerts:
    def __init__(self, ticker, values):

        self.alert_dict = { 
            4: 'rising_bid',
            5: 'falling_bid',
            23: 'fall_by_pct',
            22: 'rise_by_pct',
            20: 'rapid_increase',
            10: 'lg_volume_flat',
            2: 'lg_order_sell',
            8: 'lg_volume_rising',
            9: 'lg_volume_falling',
            17: 'top_reversal',
            1: 'lg_order_buy',
            7: 'sharp_increase',
            16: 'rebound'




            
        }

        self.symbol = [i.get('symbol') for i in ticker]
        self.name = [i.get('name') for i in ticker]
        self.alertType = [self.alert_dict.get(i.get('alertType')) for i in values]
        self.date = [i.get('date') for i in values]
        self.time = [i.get('time') for i in values]
        self.volume = [float(i.get('volume')) if i.get('volume') is not None else 0.0 for i in values]
        self.changeRatio = [round(float(i.get('changeRatio'))*100,2) if i.get('changeRatio') is not None else 0.0 for i in values]
        self.sid = [i.get('sid') for i in values]


        self.data_dict = { 
            'ticker': self.symbol,
            'name': self.name,
            'alert_type': self.alertType,
            'date': self.date,
            'time': self.time,
            'volume': self.volume,
            'change_ratio': self.changeRatio,

        }

        self.as_dataframe = pd.DataFrame(self.data_dict)




class EarningsData:
    def __init__(self, data):

        self.earningsReleaseId = [i.get('earningsReleaseId') for i in data]
        self.quoteId = [i.get('quoteId') for i in data]
        self.eventId = [i.get('eventId') for i in data]
        self.regionId = [i.get('regionId') for i in data]
        self.eventType = [i.get('eventType') for i in data]
        self.startDate = [i.get('startDate') for i in data]
        self.endDate = [i.get('endDate') for i in data]
        self.startDateTime = [i.get('startDateTime') for i in data]
        self.endDateTime = [i.get('endDateTime') for i in data]
        self.isActual = [i.get('isActual') for i in data]
        self.timePeriod = [i.get('timePeriod') for i in data]
        self.year = [i.get('year') for i in data]
        self.quarter = [i.get('quarter') for i in data]
        self.status = [i.get('status') for i in data]
        self.isUpcoming = [i.get('isUpcoming') for i in data]
        self.epsEstimate = [float(i.get('epsEstimate',0)) for i in data]
        self.lastReleaseDate = [i.get('lastReleaseDate') for i in data]
        self.isLive = [i.get('isLive') for i in data]
        self.nonGaapEpsEstimate = [float(i.get('nonGaapEpsEstimate',0)) for i in data]
        self.epsLastYear = [float(i.get('epsLastYear',0)) for i in data]
        self.nonGaapEpsLastYear = [i.get('nonGaapEpsLastYear') for i in data]
        ticker = [i.get('ticker') for i in data]
        self.symbol = [i.get('symbol') for i in ticker]
        self.name = [i.get('name') for i in ticker]
        self.change_ratio = [round(float(i.get('changeRatio'))*100,2) for i in ticker]
        self.volume = [float(i.get('volume')) for i in ticker]




        self.data_dict = { 
            'ticker': self.symbol,
            'name': self.name,
            'change_ratio': self.change_ratio,
            'volume': self.volume,
            'release_id': self.earningsReleaseId,
            'quote_id': self.quoteId,
            'event_id': self.eventId,
            'start_date': self.startDate,
            'start_datetime': self.startDateTime,
            'end_date': self.endDate,
            'end_datetime': self.endDateTime,
            'year': self.year,
            'quarter': self.quarter,
            'last_earnings': self.lastReleaseDate,
            'eps_estimate': self.epsEstimate,
            'eps_last_year': self.epsLastYear,
            'non_gap_eps_est': self.nonGaapEpsEstimate,
            'non_gap_eps_last': self.nonGaapEpsLastYear,
            
            

            


        }


        self.as_dataframe = pd.DataFrame(self.data_dict)