import csv
from locust import HttpUser, task, between, events
from requests.exceptions import RequestException, Timeout


def add_custom_arguments(parser):
    parser.add_argument("--path", type=str, default="/", help="API path")
    parser.add_argument("--file", type=str, default=None, help=".csv path")
    parser.add_argument("--method", type=str, default="GET", help="http method")


events.init_command_line_parser.add_listener(add_custom_arguments)


class MyCsv(HttpUser):
    wait_time = between(0.1, 0.5)
    req_count = 0
    user_queue = None
    max_requests = 100000

    def on_start(self):
        self.pathAPI = self.environment.parsed_options.path
        self.pathCSV = self.environment.parsed_options.file
        self.methodAPI = self.environment.parsed_options.method

        # print(f"FilePath {self.pathCSV}")
        # print(f"APIPath {self.pathAPI}")
        # print(f"APIPath {self.methodAPI}")

        if not self.pathCSV:
            raise ValueError("Error: You must provide a CSV file path using --file")

        if MyCsv.user_queue is None:
            with open(self.pathCSV, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                user_list = list(reader)
                MyCsv.user_queue = iter(user_list)

    @task
    def send_req_with_csv_data(self):
        if self.req_count >= self.max_requests:
            print(f"✅ Reached {self.max_requests} requests. Stopping Locust.")
            self.stop()
            return

        method = (self.methodAPI).upper()

        try:
            row = next(MyCsv.user_queue)
        except StopIteration:
            print("✅ All users processed. Stopping test.")
            self.stop()
            return

        user_id = row["user_id"]
        body = {"user_id": user_id}
        hConf = {"Content-Type": "application/json"}
        res = None
        try:
            if method == "GET":
                res = self.client.get(
                    self.pathAPI,
                    headers=hConf,
                    timeout=240,
                )
            elif method == "POST":
                res = self.client.post(
                    self.pathAPI,
                    json=body,
                    headers=hConf,
                    timeout=240,
                )
                self.req_count += 1

            elif method == "DELETE":
                res = self.client.delete(
                    self.pathAPI,
                    json=body,
                    headers=hConf,
                    timeout=240,
                )
            else:
                print(f"Unsupport method: {method}")
            if res is not None:
                match method:
                    case "GET":
                        if res.status_code == 200:
                            print(f"✅ Success: {user_id} At {self.req_count}")
                        else:
                            print(f"❌ Error: {self.req_count} At {self.req_count}")
                    case "POST":
                        if res.status_code == 201:
                            print(f"✅ Success: {user_id}")
                        else:
                            print(
                                f"⚠️ Failed: {user_id} -> Status: {res.status_code}, Response: {res.text}"
                            )
                # self.req_count += 1
            else:
                print(f"Unsupport method: {method}")

        except Timeout:
            print(f"⏳ Timeout Error: {user_id} -> Request took too long!")
        except RequestException as e:
            print(f"❌ Request Error: {user_id} -> {str(e)}")
