import prometheus_client as prom
import requests
import time


def check_url(url):
    """This function checks url and if connectable returns
    the status code and response time """

    response = requests.get(url)
    return response.status_code, response.elapsed.total_seconds()


if __name__ == '__main__':
    url = ["https://httpstat.us/200", "https://httpstat.us/503"]
    site = {"https://httpstat.us/200": {"reachable": 1, "response_time": 0.0},
            "https://httpstat.us/503": {"reachable": 0, "response_time": 0.0}, }
    sample_url_up_gauge = prom.Gauge('sample_external_url_up', '', ['url'])
    sample_external_url_response_ms_gauge = prom.Gauge('sample_external_url_response_ms', '', ['url'])
    prom.start_http_server(8080)

    while True:
        for i in url:
            status, response_time = check_url(i)
            if status == 200:
                site[i]["reachable"] = 1
                print(f"Site " + i + " is reachable")
            else:
                site[i]["reachable"] = 0
                print(f"Site " + i + " is unreachable")
            site[i]["response_time"] = response_time
            sample_url_up_gauge.labels(i).set(site[i]["reachable"])
            sample_external_url_response_ms_gauge.labels(i).set(site[i]["response_time"])
        time.sleep(30)
