import random

import overdue
from overdue.stopper import timecapped_to

with overdue.timeout_set_to(1, raise_exception=False) as timeout:
    for _ in range(9999999999999999999):
        random.random() * random.random() * 999_999_999 / random.random() * 123412341234
    print("did")
print(f"Triggered: {timeout.triggered}")


@timecapped_to(1)
def asdf() -> None:
    for _ in range(9999999999999999999):
        random.random() * random.random() * 999_999_999 / random.random() * 123412341234
    print("did")

asdf()
