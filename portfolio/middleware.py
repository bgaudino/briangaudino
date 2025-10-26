def htmx_middleware(get_response):
    def middleware(request):
        request.is_htmx = request.headers.get("HX-Request") == "true"
        return get_response(request)

    return middleware
