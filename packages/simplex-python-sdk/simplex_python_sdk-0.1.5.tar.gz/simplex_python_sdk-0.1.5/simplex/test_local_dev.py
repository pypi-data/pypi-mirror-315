from simplex import Simplex

import os
from dotenv import load_dotenv

load_dotenv()

def open_feedback_loop():
    high_level_task = "Find a flight from New York to San Francisco on January 1st, 2025"
    url = "https://www.google.com/travel/flights"

    client = Simplex(api_key=os.getenv("SIMPLEX_API_KEY"))
    client.browser_actor.navigate_to_url(url)
    state = client.browser_actor.take_screenshot()

    for i in range(3):
        next_step = client.get_next_step(high_level_task, state)
        print(next_step)
        actions = client.step_to_action(next_step, state)
        print(actions)

        for action in actions:
            client.browser_actor.execute(action)
            state = client.browser_actor.take_screenshot()

    client.browser_actor.close()
    client.browser_actor.save_recording("output.mp4")

def closed_feedback_loop():
    high_level_task = "Find a flight from New York to San Francisco on January 1st, 2025"
    url = "https://www.google.com/travel/flights"

    client = Simplex(api_key=os.getenv("SIMPLEX_API_KEY"))
    client.browser_actor.navigate_to_url(url)
    state = client.browser_actor.take_screenshot()

    while not client.is_task_complete(high_level_task, state):

        step_complete = False

        ## add critic here for every step
        while not step_complete:
            next_step = client.get_next_step(high_level_task, state)
            actions = client.step_to_action(next_step, state)

            for action in actions:
                client.browser_actor.execute(action)
                state = client.browser_actor.take_screenshot()

            step_complete = client.is_step_complete(next_step, state)

        
    client.browser_actor.save_recording("output.mp4")


def precomputed_trajectory():
    client = Simplex(api_key=os.getenv("SIMPLEX_API_KEY"))
    high_level_task = "Find a flight from New York to San Francisco on January 1st, 2025"
    url = "https://www.google.com/travel/flights"

    client.browser_actor.navigate_to_url(url)
    state = client.browser_actor.take_screenshot()

    ## use your own planner or calculate the trajectory yourself
    trajectory = ["click on round trip", 
                  "click on one way", 
                  "type in departure of New York", 
                  "type in destination of San Francisco", 
                  "enter date of January 1st, 2025", 
                  "click on search"]

    ## can add some max iters here as well
    for next_step in trajectory:
        actions = client.step_to_action(next_step, state)

        for action in actions:
            client.browser_actor.execute(action)
            state = client.browser_actor.take_screenshot()
        
    client.browser_actor.close()
    client.browser_actor.save_recording("output.mp4")



if __name__ == "__main__":
    precomputed_trajectory()

    

    










