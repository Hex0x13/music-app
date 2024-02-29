import json
from requests import post, get
from dotenv import load_dotenv
import os
import base64
from datetime import datetime


class SpotifyAPI:
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(SpotifyAPI, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self) -> None:
        if self.__initialized:
            return
        self.__initialized = True

        if not load_dotenv():
            exit()
        self.__client_id = os.getenv('CLIENT_ID')
        self.__client_secret = os.getenv('CLIENT_SECRET')
        self.__expires_at = None
        self.__access_token = None
        self.__init_token()

    def __init_token(self) -> None:
        auth_string = f"{self.__client_id}:{self.__client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = json.loads(post(url, headers=headers, data=data).content)

        self.__access_token = result.get("access_token")
        self.__expires_at = datetime.now().timestamp() + result.get("expires_in")

    def get_playlists(self, playlist_id) -> dict:
        if self.__expires_at and datetime.now().timestamp() >= self.__expires_at:
            self.__init_token()
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {"Authorization": f"Bearer {self.__access_token}"}
        result = get(url, headers=headers)
        return json.loads(result.content)

