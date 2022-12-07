import requests
import ApiConfig as apiconfig

if __name__ == '__main__':
    response = requests.get(apiconfig.getMetricUrl)
    apiconfig.jprint(response.json())
