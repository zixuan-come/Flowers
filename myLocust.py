from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3) # 每次请求间隔1-3秒

    @task
    def test_hello(self):
        self.client.get("/hello/zx")

    @task(3) # 权重 3，执行频率是上面的3倍
    def test_register(self):
        self.client.post("/register", json={
            "username": "test",
            "password": "123456",
            "email": "test@qq.com"
        })




