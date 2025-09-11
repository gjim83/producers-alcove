pages = {
    'index.html': {
        'path': '/',
        'display': 'home',
        'subtitle': 'the platform to empower creatives'
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
    'static/css/main.css': {}
}


class CssDefaults:
    bg_color = '#BCCAD0'
    font_color = '#707A7E'
    font_color_dark = '#495054'
    font_color_white = '#F8F8FF'
    font_color_light = "#90979B"
    menu_bg_color = 'rgb(188,202,208,0.8)' # same as bg_color but slightly transparent


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
            if filename != self.filename and data
        ]

    @property
    def css(self):
        return CssDefaults
