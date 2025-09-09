import yaml

from copy import deepcopy


MOD_KEY_MAP = {
    'mac': {
        '_shift': {
            'ui_char': '⇧',
            'keycode': [16]
        },
        '_command': {
            'ui_char': '⌘',
            'keycode': [224, 91, 93]
        },
        '_option': {
            'ui_char': '⌥',
            'keycode': [18]
        },
        '_control': {
            'ui_char': '⌃',
            'keycode': [17]
        },
        '_esc': {
            'ui_char': '␛',
            'keycode': [27]
        },
        '_tab': {
            'ui_char': '⇥',
            'keycode': [9]
        },
        '_return': {
            'ui_char': '⏎',
            'keycode': [13]
        },

    },
    'windows': {
        '_shift': {
            'ui_char': '⇧'
        },
        '_esc': {
            'ui_char': '␛',
            'keycode': [27]
        }
    }
}


with open("poc/shortcuts.yaml") as f:
    SHORTCUTS = yaml.load(f, Loader=yaml.FullLoader)


def get_shortcuts_index_map():
    """
    Maps shortcut characters to indexes where they appear

    :return: dict where main keys are OS, next level key is a character and the value is a list
    of entries from main shortcut db where they appear
    """
    index_map = {
        'mac': {},
        'windows': {}
    }
    for i, sc in enumerate(SHORTCUTS['shortcuts']):
        for plat in index_map.keys():
            for char in sc[plat].get('chars', []):
                index_map[plat].setdefault(char, set()).add(i)
            for modkey in sc[plat].get('mod', []):
                index_map[plat].setdefault(modkey, set()).add(i)

    # this will be JSON-ified later so convert sets to lists otherwise it goes poof
    for scs_per_os in index_map.values():
        for char, indices in scs_per_os.items():
            scs_per_os[char] = list(indices)

    return index_map


INDEX_MAP = get_shortcuts_index_map()


def get_ui_shortcuts_data():
    """
    Converts the raw shortcut data into appropriate formatting for UI

    :return:
    """
    ui_sc_data = []
    for sc in SHORTCUTS['shortcuts']:
        new_sc = deepcopy(sc)
        for _os in ['mac', 'windows']:
            if 'mod' in new_sc[_os].keys():
                new_sc[_os]['mod'] = [
                    MOD_KEY_MAP[_os].get(key, {}).get(
                        'ui_char', key.replace('_', '').title()
                    )
                    for key in new_sc[_os]['mod']
                ]

            if 'chars' in new_sc[_os].keys():
                new_sc[_os]['chars'] = [char.upper() for char in new_sc[_os]['chars']]
        ui_sc_data.append(new_sc)

    return ui_sc_data


UI_SC_DATA = get_ui_shortcuts_data()
