from airflow.models import Variable
from airflow.models.baseoperator import BaseOperator
from config.chatgpt import get_chatgpt_response
from config.pykrx_api import get_prompt_for_chatgpt
from config.tistory import set_tistory_post
import pendulum

class TistoryWritePostByChatgptOperator(BaseOperator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    

    def execute(self, context):
        chatgpt_api_key = Variable.get('chatgpt_api_key')
        tistory_access_token = Variable.get('tistory_access_token')

        now =  pendulum.now()
        now_yyyymmmdd = now.strftime('%Y%m%d')
        yyyy = now.year
        mm = now.month
        dd = now.day
        hh = now.hour
        ticker_name_lst, fluctuation_rate_lst, prompt_of_kospi_top_5_lst = get_prompt_for_chatgpt(now_yyyymmmdd, market='KOSPI')

        for idx, prompt in enumerate(prompt_of_kospi_top_5_lst):
            ticker_name = ticker_name_lst[idx]
            fluctuation_rate = fluctuation_rate_lst[idx]
            fluctuation_rate = round(fluctuation_rate*100, 1)
            chatgpt_resp = get_chatgpt_response(api_key=chatgpt_api_key, 
                                                prompt=prompt,
                                                temperature=0.5)
            chatgpt_resp = chatgpt_resp.replace('\n','<br/>')
            set_tistory_post(access_token=tistory_access_token,
                             blog_name='hjkim-sun',
                             title=f'{yyyy}/{mm}/{dd} {hh}시 KOSPI 급등 {fluctuation_rate}% {ticker_name} 주목!',
                             content=chatgpt_resp,
                             tag_lst=['KOSPI급등','급등주',ticker_name])
            

        ticker_name_lst, prompt_of_kosdaq_top_5_lst = get_prompt_for_chatgpt(now_yyyymmmdd, market='KOSDAQ')
        for prompt in prompt_of_kosdaq_top_5_lst:
            ticker_name = ticker_name_lst[idx]
            chatgpt_resp = get_chatgpt_response(api_key=chatgpt_api_key, 
                                                prompt=prompt,
                                                temperature=0.5)
            set_tistory_post(access_token=tistory_access_token,
                             blog_name='hjkim-sun',
                             title=f'{yyyy}/{mm}/{dd} {hh}시 KOSDAQ 급등주 {ticker_name} 주목!',
                             content=chatgpt_resp,
                             tag_lst=['KOSPI급등','급등주',ticker_name])