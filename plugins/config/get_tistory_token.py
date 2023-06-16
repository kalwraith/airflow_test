import requests 
# client_id, client_secret, code 노출 주의, 실제 값은 임시로만 넣고 Git에 올라가지 않도록 유의

url='https://www.tistory.com/oauth/access_token'
params={
  'client_id':'023887d1497901515fc74760b581d454',
  'client_secret':'023887d1497901515fc74760b581d454b3f62051120133902384835b42e3569d5f538acb',
  'redirect_uri':'http://tistory.com',
  'code':'12dedfb50fa5077d8d608c0ae17f823ade79ab1bda2b385701b23da2a252913207771d33',
  'grant_type':'authorization_code'
}
resp = requests.get(url, params=params)
print(resp.text)