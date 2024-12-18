import os
import cloudscraper

from onego import files

class SessionChrome(cloudscraper.CloudScraper):

    def __init__(self, profile: str, chrome_version: int = 131, cookies_path: str = '.polinv-session-cookies', *args, **kwargs):
        self.profile = profile
        self.cookies_path = os.path.join(cookies_path, f'{self.profile}.json')
        self.chrome_version = chrome_version or 131

        os.makedirs(cookies_path, exist_ok=True)

        super().__init__(*args, **kwargs)

        user_agent = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.chrome_version}.0.0.0 Safari/537.36'

        self.headers.update({ 'User-Agent': user_agent })
        self.headers.update({ 'Sec-Ch-Ua': f'"Not_A Brand";v="8", "Chromium";v="{self.chrome_version}", "Google Chrome";v="{self.chrome_version}"' })
        self.headers.update({ 'Sec-Ch-Ua-Mobile': '?0' })
        self.headers.update({ 'Sec-Ch-Ua-Platform': '"Windows"' })

    def __info(self): return f'<Session profile={self.profile} />'

    def save_cookies(self):
        cookies = self.export_cookies_dict()
        files.writeJSON(self.cookies_path, cookies)

    def load_cookies(self):
        cookies = files.readJSON(self.cookies_path)
        if not cookies: return []
        for c in cookies: self.cookies.set(c['name'], c['value'], domain=c['domain'], path=c['path'], secure=c['secure'], expires=c['expires'])
        return cookies

    def export_cookies_dict(self):
        return [{ 'name': c.name, 'value': c.value, 'domain': c.domain, 'path': c.path, 'secure': c.secure, 'expires': c.expires } for c in self.cookies]

    def export_cookies(self):
        return [c for c in self.cookies]

    def __str__(self): return self.__info()
    def __repr__(self): return self.__info()

def make_session(profile: str, *args, **kwargs): return SessionChrome(profile, *args, **kwargs)
