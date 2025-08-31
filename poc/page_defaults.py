pages = {
    'index.html': {
        'path': '/',
        'display': 'home',
        'subtitle': None
    },
    'search.html': {
        'path': '/search',
        'display': 'shortcut search',
        'subtitle': 'protools shortcut search'
    },
    'note2Hz.html': {
        'path': '/note2Hz',
        'display': 'note to Hz calculator',
        'subtitle': 'note to Hz calculator'
    },
    'note2ms.html': {
        'path': '/note2ms',
        'display': 'note to ms calculator',
        'subtitle': 'note to ms calculator'
    },
}


class PageDefaults:

    def __init__(self, filename):
        self.filename = filename

        for attr, value in pages[filename].items():
            setattr(self, attr, value)

    @property
    def dropmenu_items(self):
        """
        Returns data for all pages but itself, to generate dropdown menu items
        """
        return [
            data
            for filename, data in pages.items()
            if filename != self.filename
        ]
