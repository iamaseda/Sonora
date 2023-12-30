import spotipy.util as util
import sonoraTest.sonicScraper as sonicScraper
import requests


def logout():
    
    #internally initiates OAuth 2.0 authorizatoin flow and retrieves necessary access token
    token = util.prompt_for_user_token(sonicScraper.username,
                                    sonicScraper.scope,
                                    client_id=sonicScraper.client_id,
                                    client_secret=sonicScraper.client_secret,
                                    redirect_uri=sonicScraper.redirect_uri,
                                    show_dialog=True)
    url = 'https://accounts.spotify.com/authorize'
    url += '?response_type=token'
    url += '&client_id=' + requests.utils.quote(sonicScraper.client_id)
    url += '&scope=' + requests.utils.quote(sonicScraper.scope)
    url += '&redirect_uri=' + requests.utils.quote(sonicScraper.redirect_uri)
    url += '&state=' + requests.utils.quote(sonicScraper.state)

    return token


if __name__ == "__main__":
    logout()