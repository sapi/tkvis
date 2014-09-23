from src.config import cfg


class Widget(object):
    '''
    The Widget class contains class methods designed to work with certain
    kinds of Tkinter objects.

    This is an abstract base class and should not be used directly.

    '''
    @classmethod
    def descriptionOf(cls, tkWidget):
        '''
        Return a description of the given widget.

        @param tk.Widget $tkWidget
          The widget to describe.

        @retval str
          The description of the widget.

        '''
        return tkWidget.__class__.__name__

    @classmethod
    def higlight(cls, tkWidget, asParent=False):
        '''
        Highlight the given widget.

        The means of doing this may depend on the type of the widget.

        Different types of widgets are intended to be handled by different
        subclasses of Widget.

        @param tk.Widget $tkWidget
          The widget to highlight.

        @param bool $asParent [optional]
          Whether the parent highlighting style should be used.  Defaults to
          False.

        @retval object
          The old value which was changed by the highlight.

        '''
        raise NotImplementedError()

    @classmethod
    def clearHighlight(cls, tkWidget, old):
        '''
        Clear the highlight on the given widget, and restore the given value.

        @param tk.Widget $tkWidget
          The widget to clear the highlight from.
        @param object $old
          The value to restore (most often the old value changed by a call
          to .highlight).

        '''
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
        col = cfg.COLORS.PARENT_VIEW if asParent else cfg.COLORS.ACTIVE_VIEW

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
        col = cfg.COLORS.PARENT_VIEW if asParent else cfg.COLORS.ACTIVE_VIEW

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
    '''
    Describe the given widget.

    @param tk.Widget $tkWidget
      The widget to describe.

    @retval str
      The description of the widget.

    '''
    name = tkWidget.__class__.__name__
    return WIDGETS.get(name, DEFAULT).descriptionOf(tkWidget)


def highlight(tkWidget, asParent=False):
    '''
    Highlight the given widget.

    @param tk.Widget $tkWidget
      The widget to highlight.

    @param bool $asParent [optional]
      Whether the parent highlighting style should be used.  Defaults to
      False.

    @retval object
      The old value which was changed by the highlight.

    '''
    name = tkWidget.__class__.__name__
    return WIDGETS.get(name, DEFAULT).highlight(tkWidget, asParent=asParent)


def clear_highlight(tkWidget, old):
    '''
    Clear the highlight on the given widget, and restore the given value.

    @param tk.Widget $tkWidget
      The widget to clear the highlight from.
    @param object $old
      The value to restore (most often the old value changed by a call
      to .highlight).

    '''
    name = tkWidget.__class__.__name__
    return WIDGETS.get(name, DEFAULT).clearHighlight(tkWidget, old)
