# Python program killing
# threads using stop
# flag
 
import threading
import time
 
def run(stop):
    while True:
        print('thread running')
        time.sleep(1)
        if stop():
                break
                 
def main():
        stop_threads = False
        t1 = threading.Thread(target = run, args =(lambda : stop_threads, ))
        t1.start()
        time.sleep(10)
        stop_threads = True
        t1.join()
        print('thread killed')
main()

########### 2econddddddd #########

# Python program showing
# how to kill threads
# using set/reset stop
# flag
 
import threading
import time
 
def run():
    while True:
        print('thread running')
        global stop_threads
        if stop_threads:
            break
 
stop_threads = False
t1 = threading.Thread(target = run)
t1.start()
time.sleep(1)
stop_threads = True
t1.join()
print('thread killed')




##### 3333333rrrrrddd


# SuperFastPython.com
# example of canceling a running task
import asyncio
 
# define a coroutine for a task
async def task_coroutine():
    # report a message
    print('executing the task')
    # block for a moment
    await asyncio.sleep(1)
 
# custom coroutine
async def main():
    # report a message
    print('main coroutine started')
    # create and schedule the task
    task = asyncio.create_task(task_coroutine())
    # wait a moment
    await asyncio.sleep(0.1)
    # cancel the task
    was_cancelled = task.cancel()
    # report whether the cancel request was successful
    print(f'was canceled: {was_cancelled}')
    # wait a moment
    await asyncio.sleep(1)
    # check the status of the task
    print(f'canceled: {task.cancelled()}')
    # report a final message
    print('main coroutine done')
 
# start the asyncio program
asyncio.run(main())