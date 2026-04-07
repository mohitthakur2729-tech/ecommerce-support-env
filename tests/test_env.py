from env.enviroment import EcommerceSupportEnv
from env.models import Action

env = EcommerceSupportEnv(difficulty="medium")
obs = env.reset()

print("Initial State:", obs)

done = False

steps = ["ask_order_id", "verify_order", "process_refund"]

i = 0

while not done and i < len(steps):
    action = Action(
        action_type=steps[i],
        content=f"Performing {steps[i]}"
    )

    result = env.step(action)

    print("Reward:", result.reward)
    print("Done:", result.done)
    print("Progress:", result.info)

    done = result.done
    i += 1