import csv
from locust import HttpUser, task, between, events
from requests.exceptions import RequestException, Timeout
import random

def add_custom_arguments(parser):
    parser.add_argument("--path", type=str, default="/", help="API path")
    parser.add_argument("--method", type=str, default="GET", help="http method")


events.init_command_line_parser.add_listener(add_custom_arguments)

class POSTMetod(HttpUser):
    wait_time = between(1, 3)
    req_count = 0
    user_queue = None
    max_requests = 1000000

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X)",
    ]

    def on_start(self):
        self.pathAPI = self.environment.parsed_options.path
        self.methodAPI = self.environment.parsed_options.method

    @task

    def send_req_form_data(self):
        if self.req_count >= self.max_requests:
            print(f"✅ Reached {self.max_requests} requests. Stopping Locust.")
            self.stop()
            return

        method = (self.methodAPI).upper()

        user_id = "user_id"
        body = {
            "form_config_id": "675957af5bd3a30157566226",
            "ladi_form_id": "FORM33",
            "ladipage_id": "67b0393d7c2d3d00201d1810",
            "form_data": [
            {
                "name": "name",
                "value": "asd"
            },
            {
                "name": "phone",
                "value": "0800000002"
            },
            {
                "name": "address",
                "value": "asd"
            },
            {
                "name": "form_item175",
                "value": [ "รองเท้า Puma Speedcat Archive Red สีแดง  1,890.-" ]
            },
            {
                "name": "form_item191",
                "value": [ "37", "38", "39", "40", "41", "42", "43" ]
            },
            {
                "name": "form_item123",
                "value": [ "รองเท้า Puma Speedcat Archive Pink ชมพู  1,990.-" ]
            },
            {
                "name": "form_item192",
                "value": [ "37", "38", "39", "40" ] },
            {
                "name": "form_item165",
                "value": [ "รองเท้า Puma Speedcat Archive Black สีดำ 1,890.-" ]
            },
            {
                "name": "form_item197",
                "value": [ "40" ]
            },
            {
                "name": "form_item202",
                "value": [ "รองเท้า Puma Speedcat Archive Brown สีน้ำตาล 1,790.-" ]
            },
            {
                "name": "form_item198",
                "value": [ "39", "40" ]
            },
            {
                "name": "form_item203",
                "value": [ "รองเท้า Puma Speedcat Archive Blue  สีน้ำเงิน 1,890.-" ]
            },
            {
                "name": "form_item199",
                "value": [ "37" ]
            },
            {
                "name": "form_item204",
                "value": [ "รองเท้า Puma Speedcat Archive BlackPink สีดำชมพู  1,990.-" ]
            },
            {
                "name": "form_item200",
                "value": [ "37" ]
            },
            {
                "name": "i_agree_terms_and_conditions",
                "value": [ "รับฟรีหมวกแก๊ป Puma Archive Logo Baseball Black สีดำ" ]
            }
            ],
            "data_key": "",
            "status_send": 2,
            "merge_address": "false",
            "total_revenue": 0,
            "time_zone": 7
            }
        # hConf = {
        #         "Content-Type": "application/json",
        #         "Accept": "application/json",
        #         "User-Agent": random.choice(self.user_agents),
        #         }
        hConf = {
            "Origin": "https://www.puma-thailand.asia",
            "Referer": "https://www.puma-thailand.asia/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        }
        res = None

        try:

            if method == "POST":
                res = self.client.post(
                    self.pathAPI,
                    json=body,
                    headers=hConf,
                    timeout=240,
                )
                self.req_count += 1

            else:
                print(f"Unsupport method: {method}")

            if res is not None:
                match method:
                    case "POST":
                        if res.status_code == 200:
                            print(f"✅ Success: at {self.req_count}")
                        else:
                            print(
                                f"⚠️ Failed: {user_id} -> Status: {res.status_code}, Response: {res.text}"
                            )
                self.req_count += 1
            else:
                print(f"Unsupport method: {method}")

        except Timeout:
            print(f"⏳ Timeout Error: -> Request took too long!")
        except RequestException as e:
            print(f"❌ Request Error: -> {str(e)}")
