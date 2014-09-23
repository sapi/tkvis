from src.model.namespaces import Namespace


_d = {
    'ARROW_PROPS': {
            'HEAD_HEIGHT_FRAC': .3,
            'HEAD_WIDTH_FRAC': .2,
            'LINE_WIDTH_FRAC': .05,
            'TOP_SPACE_PX': 5,
        },

    'COLORS': {
        'ACTIVE_VIEW': 'red',
        'PARENT_VIEW': 'green',

        'PACKED_SPACE': 'red4',

        'DUMMY_BACKGROUND': 'gray80',
        'DUMMY_FRAME': 'gray60',
        },

    'PACKINFO': {
        'WIDTH': 100,
        'HEIGHT': 100,
        'DUMMY_SIZE': 20,
        },
    }


cfg = Namespace(**_d)
