import pandas as pd

email = input('email: ', )
password = input('password: ', )
keys = pd.DataFrame(index=[0], data={'email': email,
                                     'password': password})
keys.to_csv('auth.csv')
print('Authentication saved successfully')
