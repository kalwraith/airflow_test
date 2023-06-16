from pykrx import stock
import pandas as pd 

def get_prompt_for_chatgpt(yyyymmdd, market):
    ticker_name_lst = []
    fluctuation_rate_lst = []
    return_prompt_lst = []
    ohlcv_df = stock.get_market_ohlcv(date=yyyymmdd, market=market) # (market: KOSPI/KOSDAQ/KONEX/ALL)
    ohlcv_df.reset_index(inplace=True)

    funda_df = stock.get_market_fundamental(yyyymmdd, market=market)
    funda_df.reset_index(inplace=True)

    merged_df = pd.merge(left=ohlcv_df, right=funda_df, how='inner',on='티커')
    merged_df = merged_df.sort_values(by='등락률',ascending=False)
    merged_df.reset_index(inplace=True)

    for idx, row in merged_df.iterrows():
        ticker_name = stock.get_market_ticker_name(row['티커'])
        start_value = row['시가']
        end_value = row['종가']
        trading_vol = row['거래량']
        fluctuation_rate = row['등락률']
        bps = row['BPS']
        per = row['PER']
        pbr = row['PBR']
        eps = row['EPS']
        div = row['DIV']
        dps = row['DPS']
        report_str = f'''오늘 마감한 {ticker_name}의 주식 정보야.
        종목명: {ticker_name}
        시가: {start_value}
        종가: {end_value}
        거래량: {trading_vol}
        등락률: {fluctuation_rate}
        BPS: {bps}
        per: {per}
        pbr: {pbr}
        eps: {eps}
        div: {div}
        dps: {dps}
        {ticker_name}에 대한 기업 정보와 위 주식 정보를 이용해서 리포트를 만들어줘'''
        
        ticker_name_lst.append(ticker_name)
        return_prompt_lst.append(report_str)
        fluctuation_rate_lst.append(fluctuation_rate)
        if idx >= 5:
            break
    return ticker_name_lst, fluctuation_rate_lst, return_prompt_lst