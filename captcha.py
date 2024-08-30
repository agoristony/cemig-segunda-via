from settings import APIKEY_2CAPTCHA
from twocaptcha import TwoCaptcha

def solve_captcha(sitekey, url):
    api_key = os.getenv('APIKEY_2CAPTCHA')
    solver = TwoCaptcha(api_key)
    try:
        result = solver.recaptcha(
            sitekey=sitekey,
            url=url,
            )

    except Exception as e:
        return {'error': str(e)}
    else:
        return {'error': None, 'solution': result['code']}