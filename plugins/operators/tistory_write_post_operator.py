import requests
from airflow.models import Variable
from airflow.models.baseoperator import BaseOperator

class TistoryWritePostOperator(BaseOperator):
    def __init__(self, title, content, tag_lst, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.content = content
        self.tag_lst = tag_lst

    def execute(self, context):
        access_token = Variable.get('tistory_access_token')
        tags = ','.join(self.tag_lst)
        params={
            'access_token':access_token,
            'blogName':'hjkim-sun',
            'title': self.title,
            'content':self.content,
            'visibility':3,        # (0: 비공개 - 기본값, 1: 보호, 3: 발행)
            'category':0,
            'tag':tags,
            'acceptComment':0     # 댓글 허용 (0, 1 - 기본값)
        }

        url = 'https://www.tistory.com/apis/post/write'
        resp = requests.post(url=url, params=params)
        return resp.text
