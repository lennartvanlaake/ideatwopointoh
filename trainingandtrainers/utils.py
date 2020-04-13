class PageSelectProperty():
    def __init__(self, name, display, options):
        self.name = name
        self.options = parse_options(options)
        self.display = display


class PageSelectOption:
    def __init__(self, key, display):
        self.key = key
        self.display = display


def parse_options(option_tuples):
    return map(lambda option: PageSelectOption(option[0], option[1]), option_tuples)


def filter_children(page, clazz):
    children = page.get_children()
    content_children = []
    for child in children:
        for grandchild in child.get_children():
            typed_grandchild = grandchild.specific
            if isinstance(typed_grandchild, clazz):
                content_children.append(grandchild)
    return content_children


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


def get_query_string(request):
    return request.GET.get("query")


def apply_query(page, request, contains_properties):
    query_string = get_query_string(request)
    if query_string is None:
        return True
    for prop in contains_properties:
        if not hasattr(page, prop):
            continue
        if isinstance(prop, tuple):
            for sub_prop in prop:
                if contains(query_string, getattr(page, sub_prop)):
                    return True
        if contains(query_string, getattr(page, prop)):
            return True
    return False


def contains(first, second):
    return first.lower() in second.lower()


def apply_filters(page, request, exact_match_properties):
    match = True
    typed_page = page.specific
    for prop in exact_match_properties:
        prop_name = prop.name
        filter_choice = request.GET.getlist(prop_name)
        if filter_choice is None or filter_choice == []:
            continue
        if not match_choices(filter_choice, getattr(typed_page, prop_name)):
            match = False
    return match


def match_choices(choice_list, value):
    return any(choice == value for choice in choice_list)
