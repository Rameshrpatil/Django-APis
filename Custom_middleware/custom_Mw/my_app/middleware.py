class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Before view request middleware executed")
        
        response = self.get_response(request)
        
        print("After view response middleware executed")

        return response
