import requests

class WavesManager:

    def get_course_by_asset_names(self, amount_asset_name, price_asset_name) -> float:
        url = f'https://api.wavesplatform.com/v0/pairs/{WavesManager.get_asset_id_by_name(self, amount_asset_name)}/{WavesManager.get_asset_id_by_name(self, price_asset_name)}'

        response = requests.get(url)
        return float(response.json()['data']['lastPrice'])

    def get_asset_id_by_name(self, asset_name) -> str:
        url = f'https://api.wavesplatform.com/v0/assets?ticker={asset_name}&limit=1'

        response = requests.get(url)
        return response.json()['data'][0]['data']['id']

