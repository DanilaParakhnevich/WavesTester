import requests

class WavesManager:

    def get_course_by_asset_names(self, amount_asset, price_asset):
        url = f'https://api.wavesplatform.com/v0/pairs/{amount_asset}/{price_asset}'

        # response comes as json
        response = requests.get(url)
        return float(response.json()['data']['lastPrice'])
