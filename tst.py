from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 3)  # Random wait time between 1 and 3 seconds
    host = "https://web-uat.kon-ticket.com"  # Set target website URL

    # Timeout setting (30 seconds)
    timeout = 30

    @task
    def load_main_page(self):
        self.client.get("/", timeout=self.timeout)
        # Simulate a GET request to the homepage
        # print(f"Main page response status: {response.status_code}")

    # @task(3)
    # def load_about_page(self):
    #     response = self.client.get(
    #         "/about", timeout=self.timeout
    #     )  # Simulate a GET request to /about page
    #     print(f"About page response status: {response.status_code}")
