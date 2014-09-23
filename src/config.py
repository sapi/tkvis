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

        'RESERVED_SPACE': 'red4',

        'DUMMY_BACKGROUND': 'gray80',
        'DUMMY_FRAME': 'gray60',

        'ERROR': 'red',
        'WARNING': 'orange',
        },

    'PACKINFO': {
        'WIDTH': 100,
        'HEIGHT': 100,
        'DUMMY_SIZE': 20,
        },

    'MESSAGES': {
        'NOT_PACKED': 'Widget was not packed',
        'BAD_ANCHOR': 'Anchor in same axis as pack is ineffective',
        'INCONSISTENT_CHILD_PACKING': 'Child widgets are packed to different sides',
        },
    }


cfg = Namespace(**_d)
