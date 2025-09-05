class loggingMiddleware():

    #setup
    def __init__(self, get_response):
        self.get_response = get_response

    #where the actual processing happen
    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.
        print(f"Request received: {request.META}")

        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.
        print(f"Response sent for: {request.path}")
        print(response)
        return response