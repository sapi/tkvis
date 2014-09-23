class Widget(object):
    HIGHLIGHT_COLOR = 'red'
    PARENT_HIGHLIGHT_COLOR = 'yellow'

    @classmethod
    def descriptionOf(cls, tkWidget):
        return tkWidget.__class__.__name__

    @classmethod
    def higlight(cls, tkWidget, asParent=False):
        raise NotImplementedError()

    @classmethod
    def clearHighlight(cls, tkWidget, old):
        raise NotImplementedError()


class WidgetWithTextDescription(Widget):
    @classmethod
    def descriptionOf(cls, tkWidget):
        desc = super(WidgetWithTextDescription, cls).descriptionOf(tkWidget)
        return '{} - "{}"'.format(desc, tkWidget.cget('text'))


class WidgetWithBackgroundHighlight(Widget):
    @classmethod
    def highlight(cls, tkWidget, asParent=False):
        oldBG = tkWidget.cget('bg')
        col = cls.PARENT_HIGHLIGHT_COLOR if asParent else cls.HIGHLIGHT_COLOR

        tkWidget.config(bg=col)

        return oldBG

    @classmethod
    def clearHighlight(cls, tkWidget, old):
        tkWidget.config(bg=old)


class Frame(WidgetWithBackgroundHighlight):
    pass


class Button(WidgetWithTextDescription):
    @classmethod
    def highlight(cls, tkWidget, asParent=False):
        oldFG = tkWidget.cget('fg')
        col = cls.PARENT_HIGHLIGHT_COLOR if asParent else cls.HIGHLIGHT_COLOR

        tkWidget.config(fg=col)

        return oldFG

    @classmethod
    def clearHighlight(cls, tkWidget, old):
        tkWidget.config(fg=old)


class Label(WidgetWithTextDescription, WidgetWithBackgroundHighlight):
    pass


WIDGETS = {
        'Button': Button,
        'Frame': Frame,
        'Label': Label,
    }
DEFAULT = WidgetWithBackgroundHighlight


def describe(tkWidget):
    name = tkWidget.__class__.__name__
    return WIDGETS.get(name, DEFAULT).descriptionOf(tkWidget)


def highlight(tkWidget, asParent=False):
    name = tkWidget.__class__.__name__
    return WIDGETS.get(name, DEFAULT).highlight(tkWidget, asParent=asParent)


def clear_highlight(tkWidget, old):
    name = tkWidget.__class__.__name__
    return WIDGETS.get(name, DEFAULT).clearHighlight(tkWidget, old)
