import sched, time

s = sched.scheduler(time.time, time.sleep)

def test():
    event = s.enter(3,1,print,"ello you cunt")
    return event


test()
