def global_data(request):
    current_url = request.path
    return locals()
