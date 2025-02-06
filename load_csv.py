import csv
from locust import HttpUser, task, between
from requests.exceptions import RequestException, Timeout


class MyCsv(HttpUser):
    wait_time = between(0.5, 1)
    req_count = 0
    user_queue = None
    max_requests = 100000

    def on_start(self):
        if MyCsv.user_queue is None:
            with open("./csv/queue1.csv", mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                user_list = list(reader)
                MyCsv.user_queue = iter(user_list)

    @task
    def send_req_with_csv_data(self):
        if self.req_count >= self.max_requests:
            print(f"✅ Reached {self.max_requests} requests. Stopping Locust.")
            self.stop()
            return

        try:
            row = next(MyCsv.user_queue)
        except StopIteration:
            print("✅ All users processed. Stopping test.")
            self.stop()
            return

        user_id = row["user_id"]
        body = {"user_id": user_id}
        hConf = {"Content-Type": "application/json"}

        try:
            res = self.client.post(
                "https://queue-dev.kon-ticket.com/api/v1/queue/waiting_room/enqueue/0dc9a599-c408-4ac8-8aa6-58a801633b03",
                json=body,
                headers=hConf,
                timeout=240,
            )

            self.req_count += 1
            if res.status_code == 201:
                print(f"✅ Success: {user_id}")
            else:
                print(
                    f"⚠️ Failed: {user_id} -> Status: {res.status_code}, Response: {res.text}"
                )
        except Timeout:
            print(f"⏳ Timeout Error: {user_id} -> Request took too long!")
        except RequestException as e:
            print(f"❌ Request Error: {user_id} -> {str(e)}")
