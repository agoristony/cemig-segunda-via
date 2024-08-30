from settings import APIKEY_2CAPTCHA
from twocaptcha import TwoCaptcha

def solve_captcha(sitekey, url):
    solver = TwoCaptcha(APIKEY_2CAPTCHA)
    try:
        result = solver.recaptcha(
            sitekey=sitekey,
            url=url,
            )
        return {'error': None, 'solution': result['code']}
    except Exception as e:
        return {'error': str(e)}
        