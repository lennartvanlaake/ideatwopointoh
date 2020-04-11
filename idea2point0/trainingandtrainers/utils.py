class PageSelectProperty():
    def __init__(self, name, options):
        self.name = name
        self.options = options 

def filter_pages(pages, request, exact_match_properties, contains_properties):
    new_pages = []
    for page in pages:
        if page_filter_function(page, request, exact_match_properties, contains_properties):
            new_pages.append(page)
    return new_pages

def page_filter_function(page, request, exact_match_properties, contains_properties):
    matches_query = apply_query(page, request, contains_properties) 
    matches_filter = apply_filters(page, request, exact_match_properties)
    return matches_query and matches_filter


def get_request_param(request, param):
    return request.GET.get(param)

def get_query_string(request):
    return get_request_param(request, "query")

def apply_query(page, request, contains_properties):
    query_string = get_query_string(request)
    if query_string is None:
        return True
    for prop in contains_properties:
        if query_string.lower() in getattr(page, prop).lower():
            return True
    return False

def apply_filters(page, request, exact_match_properties):
    match = True
    for prop in exact_match_properties:
        filter_choice = get_request_param(request, prop)
        if filter_choice is None:
            continue
        if filter_choice is not getattr(page, prop):
            match = False
    return match