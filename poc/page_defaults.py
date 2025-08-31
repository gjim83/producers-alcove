pages = {
    'index.html': {
        'path': '/',
        'menu_display': 'home',
        'page_name': "producer's alcove_:home",
        'page_subtitle': None
    },
    'search.html': {
        'path': '/search',
        'menu_display': 'shortcut search',
        'page_name': "producer's alcove_:shortcut search",
        'page_subtitle': 'protools shortcut search'
    },
    'note2Hz.html': {
        'path': '/note2Hz',
        'menu_display': 'note to Hz calculator',
        'page_name': "producer's alcove_:note to Hz",
        'page_subtitle': 'note to Hz calculator'
    },
    'note2ms.html': {
        'path': '/note2ms',
        'menu_display': 'note to ms calculator',
        'page_name': "producer's alcove_:note to ms",
        'page_subtitle': 'note to ms calculator'
    },
}


key_map = {
    'menu_display': 'display',
    'page_subtitle': 'subtitle'
}


class PageDefaults:

    def __init__(self, filename):
        self.filename = filename

        for attr, value in pages[filename].items():
            setattr(self, key_map.get(attr, attr), value)

    @property
    def dropmenu_items(self):
        ret = []
        for filename, data in pages.items():
            if filename == self.filename:
                continue
            ret.append({key_map.get(k, k): v for k, v in data.items()})

        return ret
