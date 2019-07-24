'''
    mock_server.py: simulates long running Manor tasks

'''
import time
import random
import json

# min/max for emulation time in seconds
EMU_TIME_MIN = 1
EMU_TIME_MAX = 600

def call_manor(request_id, ip_address, port, payload, msg_queue, emu_time):
    """
    This method simulates a long running manor api call.
    caller thread is executed to call this method, and caller thread is expected to be tied up until this ends
    :param request_id: caller supplied request ID
    :param ip_address: IP address, not used
    :param port: TCP port, not used
    :param payload: payload, will be used in the return message
    :param msg_queue: a thread safe blocking queue that we send back status to caller
    :param emu_time: an integer from 1 to 600, emulating the time to execute (in seconds)
    :return: none
    """

    # we only accept 1 to 600 inclusive
    if emu_time < EMU_TIME_MIN:
        emu_time = EMU_TIME_MIN
    if emu_time > EMU_TIME_MAX:
        emu_time = EMU_TIME_MAX

    # decide how many responses we will send back
    n = random.randint(5, 20)

    # interval between responses
    response_interval = emu_time / float(n)

    for i in range(n):
        time.sleep(response_interval)
        reply_msg = dict()
        reply_msg['request_id'] = request_id
        reply_msg['current_step'] = i + 1
        reply_msg['total_steps'] = n
        reply_msg['ip_address'] = ip_address
        reply_msg['port'] = port
        reply_msg['payload'] = payload
        msg_queue.put(json.dumps(reply_msg))

    return

