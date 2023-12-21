import spotipy.util as util
import sonicScraper



def logout():
    
    #internally initiates OAuth 2.0 authorizatoin flow and retrieves necessary access token
    token = util.prompt_for_user_token(sonicScraper.username,
                                    sonicScraper.scope,
                                    client_id=sonicScraper.client_id,
                                    client_secret=sonicScraper.client_secret,
                                    redirect_uri=sonicScraper.redirect_uri,
                                    show_dialog=True)
    return token


if __name__ == "__main__":
    logout()