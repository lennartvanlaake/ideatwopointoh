class PageSelectProperty:
    def __init__(self, name, display, options, key_list=None):
        self.name = name
        self.options = parse_options(options)
        self.display = display
        self.key_list = key_list


class PageSelectOption:
    def __init__(self, key, display):
        self.key = key
        self.display = display


class EventDay:
    def __init__(self, day, event_list):
        self.day = day
        self.event_list = event_list


def get_event_days(pages):
    page_dict = {}
    for page in pages:
        date = page.specific.date
        if date not in page_dict.keys():
            page_dict[page.specific.date] = EventDay(date, [page])
        else:
            page_dict[page.specific.date].event_list.append(page)

    event_list = list(page_dict.values())
    event_list.sort(key=lambda ed: ed.day)
    return event_list


def parse_options(option_tuples):
    return map(lambda option: PageSelectOption(option[0], option[1]), option_tuples)


def filter_children(page, clazz):
    children = page.get_children().live()
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
        choice_list = request.GET.getlist(prop.name)
        if choice_list is None or choice_list == []:
            continue
        if not match_choices(choice_list, typed_page, prop):
            match = False
    return match


def match_choices(choice_list, typed_page, prop):
    if not prop.key_list:
        return match_choice(choice_list, getattr(typed_page, prop.name))
    return any(match_choice == getattr(typed_page, key) for key in prop.key_list)


def match_choice(choice_list, property_value):
    return any(choice == property_value for choice in choice_list)