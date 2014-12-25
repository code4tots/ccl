# globals 'mark' and 'text'

mark = 0
text = """
"""

def at_start_of_text(): return mark == 0
def at_end_of_text(): return mark >= len(text)
def at_start_of_line(): return at_start_of_text() or text[mark-1] == '\n'
def at_end_of_line(): return at_end_of_text() or text[mark] == '\n'

def current_line():
  global mark
  saved_mark = mark
  while not at_start_of_line(): mark -= 1
  line_start = mark
  while not at_end_of_line(): mark += 1
  line_end = mark
  mark = saved_mark
  return text[line_start:line_end]

def skip_empty_lines():
  global mark
  while not at_end_of_text() and current_line().strip() == '':
    while not at_end_of_line(): mark += 1
    if not at_end_of_text(): mark += 1

def execute_statement():
  pass

def execute():
  skip_empty_lines()
  while not at_end_of_text():
    execute_statement()
    skip_empty_lines()


execute()

