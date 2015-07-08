import sys

def parse(s):
	d = []
	stack = []
	i = 0
	def skip_comments_and_spaces():
		j = i
		while s[j:j+1].isspace() or s[j:j+1] == '#':
			if s[j:j+1] == '#':
				while s[j:j+1] and s[j:j+1] != '\n':
					j += 1
			else:
				j += 1
		return j
	i = skip_comments_and_spaces()
	while i < len(s):
		a = i
		if s.startswith(("'", '"', "r'", 'r"'), i):
			raw = False
			if s[i] == 'r':
				i += 1
				raw = True
			if s.startswith(('"""', "'''"), i):
				q = s[i:i+3]
				i += 3
			else:
				q = s[i]
				i += 1
			while not s.startswith(q, i):
				if i > len(s):
					raise SyntaxError()
				if not raw and s.startswith('\\' + q[0], i):
					i += 2
				else:
					i += 1
			i += len(q)
			d.append({
				'type': 'str',
				'value': eval(s[a:i]),
			})
		else:
			while i < len(s) and not s[i].isspace():
				i += 1
			value = s[a:i]
			if value == '(':
				stack.append(len(d))
				d.append({
					'type': '(',
					'value': None}) # Eventually 'value' should point to matching ')'
			elif value == ')':
				j = stack.pop()
				d[j]['value'] = len(d)
				d.append({
					'type': ')',
					'value': j}) # 'value' points to matching '('
			else:
				try:
					value = float(value)
					d.append({
						'type': 'num',
						'value': value})
				except ValueError:
					if value.startswith('.'):
						d.append({
							'type': 'attr',
							'value': value[1:]})
					elif value.startswith('='):
						d.append({
							'type': 'assign',
							'value': value[1:]})
					elif value.startswith(','):
						d.append({
							'type': 'push',
							'value': value[1:]})
					else:
						d.append({
							'type': 'id',
							'value': value})
		i = skip_comments_and_spaces()
	return d

def swiftify(d):
	if isinstance(d, (float, int)):
		return str(d)
	if isinstance(d, str):
		return ''.join(('"', ''.join('\\u{%x}' % ord(c) for c in d), '"'))
	elif isinstance(d, list):
		return ''.join(('[', ','.join(swiftify(item) for item in d), ']'))
	elif isinstance(d, dict):
		return ''.join(('[', ','.join('%s:%s' % tuple(map(swiftify, pair)) for pair in d.items()), ']'))
	else:
		raise ValueError(d)

if __name__ == '__main__':
	print('let opcodes : [Opcode] = %s' % swiftify(parse(sys.stdin.read())))
