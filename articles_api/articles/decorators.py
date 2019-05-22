from rest_framework.response import Response
from rest_framework.views import status

def validate_request(fn):
    def decorated(*args, **kwargs):
        title = args[0].request.data.get("title", "")
        author = args[0].request.data.get("author", "")
        if not title and not author:
            return Response(
                data={
                    "message": "Title and author required to create article"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated
