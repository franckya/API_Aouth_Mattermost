import requests
from pyquery import PyQuery as pq

client_id = '...your_mattermost_client_id...'
user = '...username...'
pw = '...userpass...'

gitlab = 'https://git.example'
chat = 'https://chat.opennms.com'
team = '/opennms-it'

r = requests.get(
    chat + team + '/login/github'
)
q = pq(r.content)
csrf_token = q('#new_ldap_user input[name="authenticity_token"]')[0].value  # watch out, several tokens for ldap vs. normal login, inspect the page to find correct one

r2 = requests.post(
    gitlab + '/users/auth/ldapmain/callback',  # or whatever the browser callback for your auth-method was
    cookies=r.cookies,
    data={
        'authenticity_token': csrf_token,
        'username': user,
        'password': pw,
    }
)

me = requests.get(
    chat + '/api/v1/users/me',
    cookies=r2.cookies,
)
print('me.json()')  # if everything went well you're now authorized
