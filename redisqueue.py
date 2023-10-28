import time
import redis
from nltk.tokenize import word_tokenize
from rq import Queue
r = redis.Redis()
q= Queue(connection=r)


def task_in_background():  
    try:
        delay = 10  
        print("Running Task")  
        print("Simulates the {delay} seconds")
        time.sleep(delay)  
        print("Completed Task")  
    except Exception as e:
        print(e)

def execute_redis_fn():
    print("ok")
    job = q.enqueue(task_in_background)
    q_len = type(q)
    print(job.id)   