import kivy
import kivy.app
import kivy.clock
import kivy.properties
import kivy.uix.label
import kivy.uix.widget
import kivy.uix.stacklayout
import kivy.uix.boxlayout
import kivy.vector

def MakeApp():
  d = dict()
  app = kivy.app.App()
  app.build = lambda: d['build']()['__rawPython__']

  def SetTitle(title):
    app.title = title

  d.update({
      'setTitle': SetTitle,
      'run': app.run,
      '__rawPython__': app,
  })
  return d

def BindWidgetMethods(d, widget):

  def AddWidget(child):
    widget.add_widget(child['__rawPython__'])
  d['addWidget'] = AddWidget

def MakeWidget(dd=None):
  dd = dd or dict()
  widget = kivy.uix.widget.Widget()
  d = dict()
  BindWidgetMethods(d, widget)
  d.update({
      '__rawPython__': widget,
  })
  return d

def MakeLabel(dd):
  if isinstance(dd, str):
    dd = {'text': dd}

  label = kivy.uix.label.Label()
  d = dict()

  def SetText(text):
    label.text = text

  def GetText():
    return label.text

  d.update({
      'getText': GetText,
      'setText': SetText,
      '__rawPython__': label,
  })
  label.text = dd['text']
  return d

# TODO: StackLayout doesn't work as expected...
def MakeStackLayout(dd=None):
  dd = dd or dict()
  stackLayout = kivy.uix.stacklayout.StackLayout()
  d = dict()
  BindWidgetMethods(d, stackLayout)
  d.update({
      '__rawPython__': stackLayout,
  })
  return d

def MakeBoxLayout(dd=None):
  dd = dd or dict()
  boxLayout = kivy.uix.boxlayout.BoxLayout()
  d = dict()
  BindWidgetMethods(d, boxLayout)
  d.update({
      '__rawPython__': boxLayout,
  })
  return d

def Load():
  return {
      'rawKivyModule': kivy,
      'app': MakeApp,
      'uix': {
          'widget': MakeWidget,
          'label': MakeLabel,
          'stackLayout': MakeStackLayout,
          'boxLayout': MakeBoxLayout,
      }
  }
