"""gui.py

Whereas kv.py is meant to be a wrapper for kivy,
gui.py is meant to be a super simple gui library.

It uses kivy internally, but this may change in the future.
"""
import kivy
import kivy.app
import kivy.clock
import kivy.properties
import kivy.uix.button
import kivy.uix.label
import kivy.uix.widget
import kivy.uix.boxlayout
import kivy.vector

def MakeApp(widget):
  app = kivy.app.App()
  app.build = lambda : widget['__rawPython__']

  def Run():
    app.run()
    return 0

  return {
      '__rawPython__': app,
      'run': Run,
  }

def MakeButton(text, on_press):
  button = kivy.uix.button.Button(text=text, on_press=lambda x: on_press())
  return {
      '__rawPython__': button,
  }

def MakeLabel(text):
  label = kivy.uix.label.Label(text=text)

  def SetText(new_text):
    label.text = new_text
    return new_text

  return {
      '__rawPython__': label,
      'setText': SetText,
      'getText': lambda: label.text,
  }

def MakeLayout(children, orientation):
  if orientation not in ('horizontal', 'vertical'):
    raise ValueError('orientation must be one of horizontal or vertical '
                     'but found ' + repr(orientation))

  layout = kivy.uix.boxlayout.BoxLayout(orientation=orientation)
  for child in children:
    layout.add_widget(child['__rawPython__'])
  return {
      '__rawPython__': layout,
  }

def MakeVerticalLayout(children):
  return MakeLayout(children, orientation='vertical')

def MakeHorizontalLayout(children):
  return MakeLayout(children, orientation='horizontal')

def Load():
  return {
      'app': MakeApp,
      'button': MakeButton,
      'label': MakeLabel,
      'layouty': MakeVerticalLayout,
      'layoutx': MakeHorizontalLayout,
  }

