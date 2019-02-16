from threading import current_thread

_requests = {}


# idk this got removed on master. it doesn't work anyways.

def get_username():
    t = current_thread()
    if t not in _requests:
        return None
    return _requests[t]


class RequestMiddleware(object):
    def process_request(self, request):
        _requests[current_thread()] = request
