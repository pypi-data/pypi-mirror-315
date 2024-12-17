import base64
from django.contrib.auth import authenticate
from django.http import HttpResponse

class BasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.include_paths = ["/api/v1"]

    def __call__(self, request):
        if any([request.path.startswith(path) for path in self.include_paths]):
            if 'HTTP_AUTHORIZATION' in request.META:
                auth_data = request.META['HTTP_AUTHORIZATION'].split()
                if len(auth_data) == 2 and auth_data[0].lower() == "basic":
                    username, password = base64.b64decode(auth_data[1]).decode('utf-8').split(':', 1)
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        request.user = user
                        return self.get_response(request)

            response = HttpResponse("Unauthorized", status=401)
            return response

        return self.get_response(request)
