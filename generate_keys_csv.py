import pandas as pd

api_key = input('API key: ', )
api_key_secret = input('API key secret: ', )
access_token = input('Access token: ', )
access_token_secret = input('Access token secret: ', )
keys = pd.DataFrame(index=[0], data={'access_token': access_token,
                                     'access_token_secret': access_token_secret,
                                     'api_key': api_key,
                                     'api_key_secret': api_key_secret})
keys.to_csv('keys.csv')
