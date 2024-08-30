import requests
import pickle, json
from captcha import solve_captcha
import graphql as graphql
from bs4 import BeautifulSoup
import base64    
class Cemig:
    def __init__(self, username, password):
        self.client = requests.Session()
        self.client.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 
                                    'Channel': 'AGV'})
        self.access_token = ""
        self.login(username, password)
        self.get_session_details()
        
    def login(self, username, password):
        try:
            self.load_cookies()
            self.load_auth_header()
        except:
            pass
        if self.get_session_details():
            return self.get_session_details()
        url = 'https://atende.cemig.com.br/Login'
        response = self.client.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        sitekey = soup.find('div', {'class': 'g-recaptcha'}).get('data-sitekey')
        requestVerificationToken = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')
        solution = solve_captcha(sitekey, url)
        if solution.get('error'):
            return solution['error']
        data = {
            'g-recaptcha-response': solution['solution'],
            'Acesso': username,
            'Senha': password,
            '__RequestVerificationToken': requestVerificationToken,
        }
        response = self.client.post(url, data=data, allow_redirects=True)
        try:
            sessaoNova = json.loads(response.cookies.get('SessaoNovaAGV'))
        except TypeError:
            return response.text
        access_token = sessaoNova.get('NovaAGVDadosToken').get('accessToken')
        self.access_token = access_token
        redirect_token = self.client.post('https://atende.cemig.com.br/Home/GetTokenRedirectNewAGV?messageFinalService=&serviceId=&executedServiceId=0&executedServiceName').text.replace('"', '')
        data = {
            'redirectToken': redirect_token,
            'accessToken': access_token,
        }
        self.client.post('https://www.atendimento.cemig.com.br/portal/api/redirect', data=data)
        self.save_cookies()
        self.save_auth_header()
        return self.get_session_details()
        
    def save_cookies(self):
        with open('cookies.pkl', 'wb') as f:
            pickle.dump(self.client.cookies, f)
    
    def load_cookies(self):
        with open('cookies.pkl', 'rb') as f:
            self.client.cookies.update(pickle.load(f))
            
    def save_auth_header(self):
        with open('auth_header.pkl', 'wb') as f:
            pickle.dump({'Authorization': f'Bearer {self.access_token}'}, f)
    
    def load_auth_header(self):
        with open('auth_header.pkl', 'rb') as f:
            self.client.headers.update(pickle.load(f))
        self.access_token = self.client.headers.get('Authorization').split(' ')[1]
    
    def get_session_details(self):
        url = 'https://www.atendimento.cemig.com.br/portal/api/auth/session'
        response = self.client.get(url, headers={'Authorization': f'Bearer {self.access_token}'})
        if response.json().get('data'):
            self.client.headers.update({'P-Id': response.json().get('data').get('protocol').get('pId')})
            self.client.headers.update({'Protocol': response.json().get('data').get('protocol').get('protocol')})
            self.client.headers.update({'Protocol-Id': response.json().get('data').get('protocol').get('protocolId')})
            return response.json()
        return None
    
    

    
    
    
class Customer:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.sites = []
        self.client = Cemig(username, password)
        self.get_site_list()
        
    def get_site_list(self):
        sites = graphql.graphql_query(self.client.client, *graphql.site_list_query())
        if sites:
            self.sites = {
                site['siteNumber']: site 
                for site 
                in sites.get('data').get('siteListByBusinessPartnerV2').get('sites') 
                if site.get('status') != 'Terminated'
                }
        return self.sites
            
    def get_bills_history(self, site):
        response = graphql.graphql_query(self.client.client, *graphql.bills_history_query(site['id']))
        return response.get('data').get('billsHistory').get('bills')
    
    def get_bill_details(self, siteId, bill_identifier):
        return graphql.graphql_query(self.client.client, *graphql.bill_details_query(siteId, bill_identifier)).get('data').get('billDetails').get('bills')[0]
    
    def get_bill_pdf(self, site, bill_identifier):
        site_id = site['id']
        site_number = site['siteNumber']
        details = self.get_bill_details(site_id, bill_identifier)
        ref_month = details.get('referenceMonth').replace('/', '-')
        filename = f'conta-{site_number}-{ref_month}.pdf'
        base64pdf = graphql.graphql_query(self.client.client, *graphql.bill_pdf_query(site_id, bill_identifier)).get('data').get('billPDF').get('pdfBase64')
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(base64pdf))
        response = {
            'value': details.get('value'),
            'pix': details.get('pix'),
            'barCode': details.get('barCode'),
            'file': filename,
        }
        return response