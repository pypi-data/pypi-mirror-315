import requests
import threading


class ThreadFluentResponse:
    def __init__(self, thread=None, response=None):
        self.thread = thread  # The thread object if threading is enabled
        self.response = response  # The response object when available
        self.exception = None  # Holds exceptions if they occur

    def wait_for_response(self):
        if self.thread:
            self.thread.join()  
        if self.exception:
            raise self.exception
        return self.response


class ThreadFluent:

    def __init__(self):
        self.session = requests.Session()

    def request(self, method, url, threaded=False, daemon=False, callback=None, **kwargs):

        result = ThreadFluentResponse()  # Custom response container

        def make_request():
            try:
                response = self.session.request(method, url, **kwargs)
                result.response = response  # Store the response in the container
                if callback:
                    callback(result.thread)  # Pass the thread to the callback
            except Exception as e:
                result.exception = e  # Store the exception
                if callback:
                    callback(result.thread)  # Pass the thread to the callback

        if threaded:
            thread = threading.Thread(target=make_request, daemon=daemon)
            thread.start()
            result.thread = thread  # Attach the thread to the custom response
        else:
            make_request()  # Execute synchronously

        return result  # Return the custom response object

    # HTTP method wrappers
    def get(self, url, threaded=False, daemon=False, callback=None, **kwargs):
        return self.request("GET", url, threaded, daemon, callback, **kwargs)

    def post(self, url, threaded=False, daemon=False, callback=None, **kwargs):
        return self.request("POST", url, threaded, daemon, callback, **kwargs)

    def put(self, url, threaded=False, daemon=False, callback=None, **kwargs):
        return self.request("PUT", url, threaded, daemon, callback, **kwargs)

    def delete(self, url, threaded=False, daemon=False, callback=None, **kwargs):
        return self.request("DELETE", url, threaded, daemon, callback, **kwargs)

    def head(self, url, threaded=False, daemon=False, callback=None, **kwargs):
        return self.request("HEAD", url, threaded, daemon, callback, **kwargs)

    def options(self, url, threaded=False, daemon=False, callback=None, **kwargs):
        return self.request("OPTIONS", url, threaded, daemon, callback, **kwargs)

    def patch(self, url, threaded=False, daemon=False, callback=None, **kwargs):
        return self.request("PATCH", url, threaded, daemon, callback, **kwargs)

    # Utilities for session management
    def set_headers(self, headers):
        """
        Set default headers for all requests.
        """
        self.session.headers.update(headers)

    def set_proxy(self, proxies):
        """
        Set proxy configuration for the session.
        """
        self.session.proxies.update(proxies)

    def authenticate(self, auth):
        """
        Set authentication credentials for the session.
        """
        self.session.auth = auth

    def set_retry(self, total=3, backoff_factor=0.3, status_forcelist=(500, 502, 503, 504)):
        """
        Enable automatic retries for failed requests.
        """
        from requests.adapters import HTTPAdapter
        from requests.packages.urllib3.util.retry import Retry

        retries = Retry(total=total, backoff_factor=backoff_factor, status_forcelist=status_forcelist)
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def get_session(self):
        """
        Retrieve the underlying requests session for custom configurations.
        """
        return self.session

    def clear_session(self):
        """
        Clear session cookies and reset configuration.
        """
        self.session = requests.Session()


threadfluent=ThreadFluent()