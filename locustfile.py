import random
import time
import threading
from locust import FastHttpUser, TaskSet, between, events
from gevent.event import Event

products = [
    '0PUK6V6EV0',
    '1YMWWN1N4O',
    '2ZYFJ3GM2N',
    '66VCHSJNUP',
    '6E92ZMYYFZ',
    '9SIQT8TOJO',
    'L9ECAV7KIM',
    'LS4PSXUNUM',
    'OLJCESPC7Z']

# Modified task functions to check if the test is still running
def index(l):
    if l.parent.is_test_running():
        l.client.get("/")

def setCurrency(l):
    if l.parent.is_test_running():
        currencies = ['EUR', 'USD', 'JPY', 'CAD']
        l.client.post("/setCurrency", {'currency_code': random.choice(currencies)})

def browseProduct(l):
    if l.parent.is_test_running():
        l.client.get("/product/" + random.choice(products))

def viewCart(l):
    if l.parent.is_test_running():
        l.client.get("/cart")

def addToCart(l):
    if l.parent.is_test_running():
        product = random.choice(products)
        l.client.get("/product/" + product)
        l.client.post("/cart", {
            'product_id': product,
            'quantity': random.choice([1,2,3,4,5,10])})

def checkout(l):
    if l.parent.is_test_running():
        addToCart(l)
        l.client.post("/cart/checkout", {
            'email': 'someone@example.com',
            'street_address': '1600 Amphitheatre Parkway',
            'zip_code': '94043',
            'city': 'Mountain View',
            'state': 'CA',
            'country': 'United States',
            'credit_card_number': '4432-8015-6152-0454',
            'credit_card_expiration_month': '1',
            'credit_card_expiration_year': '2039',
            'credit_card_cvv': '672',
        })

class UserBehavior(TaskSet):
    def on_start(self):
        self.wait_for_test_start()
        index(self)

    def wait_for_test_start(self):
        self.parent.all_users_spawned.wait()

    tasks = {index: 1,
        setCurrency: 2,
        browseProduct: 10,
        addToCart: 2,
        viewCart: 3,
        checkout: 1}

class WebsiteUser(FastHttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 10)
    all_users_spawned = Event()
    test_start_time = None
    test_duration = 60  # Duration in seconds after all users are spawned

    def is_test_running(self):
        return time.time() - self.test_start_time <= self.test_duration if self.test_start_time else False

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    def on_spawn_complete(**kwargs):
        WebsiteUser.all_users_spawned.set()
        WebsiteUser.test_start_time = time.time()
        print(f"All users spawned, starting {WebsiteUser.test_duration} second test")
        environment.runner.stats.reset_all()
        
        def stop_test():
            time.sleep(WebsiteUser.test_duration)
            print("Test duration reached, stopping test")
            environment.runner.quit()
        
        threading.Thread(target=stop_test, daemon=True).start()

    environment.events.spawning_complete.add_listener(on_spawn_complete)