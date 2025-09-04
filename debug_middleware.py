class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log all incoming requests
        if request.method in ['PUT', 'POST', 'DELETE']:
            print(f"\n=== MIDDLEWARE DEBUG ===")
            print(f"Method: {request.method}")
            print(f"Path: {request.path}")
            print(f"Content-Type: {request.content_type}")
            print(f"User: {request.user}")
            print(f"Is authenticated: {request.user.is_authenticated}")
            if hasattr(request, 'body'):
                print(f"Body: {request.body[:500]}...")  # First 500 chars
            print(f"=== MIDDLEWARE DEBUG END ===\n")
        
        response = self.get_response(request)
        return response