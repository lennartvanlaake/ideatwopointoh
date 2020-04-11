class PageSelectProperty():
    def __init__(self, name, display, options):
        self.name = name
        self.options = parse_options(options)
        self.display = display

class PageSelectOption():
    def __init__(self, key, display):
        self.key = key
        self.display = display 

def parse_options(option_tuples):
    return map(lambda option: PageSelectOption(option[0], option[1]), option_tuples)

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
        prop_name = prop.name
        filter_choice = get_request_param(request, prop_name)
        if filter_choice is None:
            continue
        if filter_choice is not getattr(page, prop_name):
            match = False
    return match