"""All filters from shopify's liquid"""
import math

from functools import partial
from .filtermgr import register_filter


class EmptyDrop:

	def __init__(self):
		setattr(self, 'empty?', True)

	def __str__(self):
		return ''

	def __eq__(self, other):
		return not bool(other)

	def __ne__(self, other):
		return not self.__eq__(other)

	def __bool__(self):
		return False

	def __nonzero__(self):
		return False


def _hash(method, base, string=None):
	"""Converts a string into an hashed string within designed method."""
	import hashlib
	import hmac

	if not isinstance(base, bytes):
		base = base.encode()
	if method in hashlib.algorithms_guaranteed:
		h = hashlib.new(method)
		h.update(base)
		return h.hexdigest()
	elif method == "hmac_sha1":
		return hmac.new(base, string.encode(), hashlib.sha1).hexdigest()
	elif method == "hmac_sha256":
		return hmac.new(base, string.encode(), hashlib.sha256).hexdigest()


register_filter(str.capitalize)
register_filter(abs)
register_filter('at_least')(max)
register_filter('at_most')(min)
register_filter('concat')(list.__add__)
register_filter(round)
register_filter('downcase')(str.lower)
register_filter('upcase')(str.upper)
register_filter(__import__('html').escape)
register_filter(str.lstrip)
register_filter(str.rstrip)
register_filter(str.strip)
register_filter(str.replace)
register_filter('size')(len)
register_filter('md5')(partial(_hash, 'md5'))
register_filter('sha1')(partial(_hash, 'sha1'))
register_filter('sha256')(partial(_hash, 'sha256'))
register_filter('hmac_sha1')(partial(_hash, 'hmac_sha1'))
register_filter('hmac_sha256')(partial(_hash, 'hmac_sha256'))


def _get_prop(obj, prop):
	try:
		return obj[prop]
	except (TypeError, KeyError):
		return getattr(obj, prop)


@register_filter('index')
def liquid_index(base, idx):
	if isinstance(base, (str, list, tuple)) and 0 <= idx <= len(base) - 1:
		return base[idx]
	return ""


@register_filter
def split(base, sep):
	"""Split a string into a list
	If the sep is empty, return the list of characters
	"""
	if not sep:
		return list(base)
	return base.split(sep)


@register_filter
def append(base, suffix):
	"""Append a suffix to a string"""
	return f"{base}{suffix}"


@register_filter
def prepend(base, prefix):
	"""Prepend a prefix to a string"""
	return f"{prefix}{base}"


@register_filter
def ceil(base):
	"""Get the ceil of a number"""
	return math.ceil(float(base))


@register_filter
def floor(base):
	"""Get the floor of a number"""
	return math.floor(float(base))


@register_filter('map')
def liquid_map(base, prop):
	"""Map a property to a list of objects"""
	return [_get_prop(bas, prop) for bas in base]


@register_filter
def compact(base):
	"""Remove empties from a list"""
	ret = [bas for bas in base if bas]
	return ret or EmptyDrop()


@register_filter('date')
def liquid_date(base, fmt):
	"""Format a date/datetime"""
	from datetime import datetime
	if base == "now":
		dtime = datetime.now()
	elif base == "today":
		dtime = datetime.today()
	else:
		from dateutil import parser
		dtime = parser.parse(base)
	return dtime.strftime(fmt)


@register_filter
def default(base, deft):
	"""Return the deft value if base is not set.
	Otherwise, return base"""
	if base == 0.0:
		return base
	return base or deft


@register_filter
def divided_by(base, dvdby):
	"""Implementation of / or // """
	if isinstance(dvdby, int):
		return base // dvdby
	return base / dvdby


@register_filter
def escape_once(base):
	"""Escapse html characters only once of the string"""
	import html
	return html.escape(html.unescape(base))


@register_filter
def first(base):
	"""Get the first element of the list"""
	if not base:
		return EmptyDrop()
	return base[0]


@register_filter
def last(base):
	"""Get the last element of the list"""
	if not base:
		return EmptyDrop()
	return base[-1]


@register_filter
def join(base, sep):
	"""Join a list by the sep"""
	if isinstance(base, EmptyDrop):
		return ''
	return sep.join(base)


@register_filter
def minus(base, sep):
	"""Implementation of - """
	return base - sep


@register_filter
def plus(base, sep):
	"""Implementation of + """
	return base + sep


@register_filter
def times(base, sep):
	"""Implementation of * """
	return base * sep


@register_filter
def modulo(base, sep):
	"""Implementation of % """
	return base % sep


@register_filter
def newline_to_br(base):
	"""Replace newline with `<br />`"""
	return base.replace('\n', '<br />')


@register_filter
def remove(base, string):
	"""Remove a substring from a string"""
	return base.replace(string, '')


@register_filter
def remove_first(base, string):
	"""Remove the first substring from a string"""
	return base.replace(string, '', 1)


@register_filter
def replace_first(base, old, new):
	"""Replace the first substring with new string"""
	return base.replace(old, new, 1)


@register_filter
def reverse(base):
	"""Get the reversed list"""
	if not base:
		return EmptyDrop()
	return list(reversed(base))


@register_filter
def sort(base):
	"""Get the sorted list"""
	if not base:
		return EmptyDrop()
	return list(sorted(base))


@register_filter
def sort_natural(base):
	"""Get the sorted list in a case-insensitive manner"""
	if not base:
		return EmptyDrop()
	return list(sorted(base, key=str.casefold))


@register_filter('slice')
def liquid_slice(base, start, length=1):
	"""Slice a list"""
	if not base:
		return EmptyDrop()
	if start < 0:
		start = len(base) + start
	return base[start:start + length]


@register_filter
def strip_html(base):
	"""Strip html tags from a string"""
	import re
	# use html parser?
	return re.sub(r'<[^>]+>', '', base)


@register_filter
def strip_newlines(base):
	"""Strip newlines from a string"""
	return base.replace('\n', '')


@register_filter
def truncate(base, length, ellipsis="..."):
	"""Truncate a string"""
	lenbase = len(base)
	if length >= lenbase:
		return base

	return base[:length - len(ellipsis)] + ellipsis


@register_filter
def truncatewords(base, length, ellipsis="..."):
	"""Truncate a string by words"""
	# do we need to preserve the whitespaces?
	baselist = base.split()
	lenbase = len(baselist)
	if length >= lenbase:
		return base

	# instead of collapsing them into just a single space?
	return " ".join(baselist[:length]) + ellipsis


@register_filter
def uniq(base):
	"""Get the unique elements from a list"""
	if not base:
		return EmptyDrop()
	ret = []
	for bas in base:
		if not bas in ret:
			ret.append(bas)
	return ret


@register_filter
def url_decode(base):
	"""Url-decode a string"""
	try:
		from urllib import unquote
	except ImportError:
		from urllib.parse import unquote
	return unquote(base)


@register_filter
def url_encode(base):
	"""Url-encode a string"""
	try:
		from urllib import urlencode
	except ImportError:
		from urllib.parse import urlencode
	return urlencode({'': base})[1:]


@register_filter
def url_escape(base):
	# TODO: 转义不准确
	"""Identifies all characters in a string that are not allowed in URLS, and replaces the characters with their escaped variants."""
	try:
		from urllib import parse as urllib_parse
	except ImportError:
		import urllib as urllib_parse
	return urllib_parse.quote_plus(base.encode("utf-8"))


@register_filter
def url_param_escape(base):
	# TODO: 转义不准确
	"""Identifies all characters in a string that are not allowed in URLS, and replaces the characters with their escaped variants."""
	try:
		from urllib import parse as urllib_parse
	except ImportError:
		import urllib as urllib_parse
	return urllib_parse.quote_plus(base.encode("utf-8"))


@register_filter
def where(base, prop, value):
	"""Query a list of objects with a given property value"""
	ret = [bas for bas in base if _get_prop(bas, prop) == value]
	return ret or EmptyDrop()


@register_filter
def t(base, prop, value):
	""""""
	pass


@register_filter
def camelcase(base):
	"""Converts a string into CamelCase."""
	import re
	return "".join([bas.capitalize() for bas in re.sub(r"-+", '-', base).split('-')])


@register_filter
def pluralize(base, singular, plural):
	"""Outputs the singular or plural version of a string based on the value of a number. The first parameter is the singular string and the second parameter is the plural string."""
	if not isinstance(base, (int, float)):
		return None
	return f"{base} {singular}" if base <= 1 else f"{base} {plural}"


def liquid_str_format_time(base, _format="%a, %b %d, %y"):
	from datetime import datetime
	if isinstance(base, datetime):
		return base.strftime(_format)
	return ""


register_filter('date')(liquid_str_format_time)
register_filter('time_tag')(liquid_str_format_time)


@register_filter
def default(base, default_value):
	null_values = [None, False, '']
	if base in null_values:
		return default_value
	return base


@register_filter
def _json(base):
	import json
	return json.dumps(base)


def highlight(open_tag, close_tag, base, match_item=None):
	import re
	if match_item and re.match(base, match_item):
		print(base, match_item)
		return f"{open_tag}{base}{close_tag}"
	# print(base, match_item)
	return base


register_filter('highlight')(partial(highlight, '<strong>', '</strong>'))
register_filter('highlight_active')(partial(highlight, '<span class="active">', '</span>', match_item='.*'))


@register_filter
def placeholder_svg_tag(base, class_name):
	return f"<svg class='{class_name}' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 525.5 525.5'>{base}</svg>"


@register_filter
def weight_with_unit(base):
	# TODO: lack general unit
	return f"{base}"


# Color
def rgba_to_rgba(value) -> tuple:
	if len(value) == 4:
		return tuple([int(v) for v in value[:3]] + [float(value[3])])
	elif len(value) == 3:
		return tuple([int(v) for v in value] + [1])
	else:
		return 0, 0, 0, 0


def hex_to_rgba(value) -> tuple:
	hex_string = value.lstrip("#")

	def to_base10(v):
		return int(v, 16)

	rgb = [to_base10(hex_string[i:i + 2]) for i in range(0, len(hex_string), 2)]
	return tuple(rgb + [1])


def hsl_to_rgba(value) -> tuple:
	h, s, l = float(value[0]), float(value[1].rstrip("%")) / 100, float(value[2].rstrip("%")) / 100
	a = float(value[3]) if len(value) == 4 else 1.0
	if s > 0:
		v_1_3 = 1.0 / 3
		v_1_6 = 1.0 / 6
		v_2_3 = 2.0 / 3

		q = l * (1 + s) if l < 0.5 else l + s - (l * s)
		p = l * 2 - q
		hk = h / 360.0  # h 规范化到值域 [0, 1) 内
		tr = hk + v_1_3
		tg = hk
		tb = hk - v_1_3

		rgb = [
			tc + 1.0 if tc < 0 else
			tc - 1.0 if tc > 1 else
			tc
			for tc in (tr, tg, tb)
		]

		rgb = [
			p + ((q - p) * 6 * tc) if tc < v_1_6 else
			q if v_1_6 <= tc < 0.5 else
			p + ((q - p) * 6 * (v_2_3 - tc)) if 0.5 <= tc < v_2_3 else
			p
			for tc in rgb
		]

		rgb = list(int(i * 256) for i in rgb)

	# s == 0 的情况
	else:
		rgb = [l, l, l]

	return tuple(rgb + [a])


class Color:
	def __init__(self, rgba):
		self.rgba = rgba

	@property
	def hex(self):
		# TODO: return tuple
		def to_hex(v):
			return f"0{hex(v).lstrip('0x')}" if v <= 15 else f"{hex(v).lstrip('0x')}"

		return "#" + "".join((to_hex(int(c * self.rgba[3])) for c in self.rgba[:3]))

	@property
	def rgb(self):
		# TODO: return tuple
		if self.rgba[3] < 1.0:
			return "rgba(%d, %d, %d, %0.1f)" % self.rgba
		return "rgb(%d, %d, %d)" % self.rgba[:3]

	@property
	def hsl(self):
		# TODO: return tuple

		r, g, b = (c / 255 for c in self.rgba[:3])
		a = self.rgba[3]
		max_c, min_c = max(r, g, b), min(r, g, b)
		plus_c = max_c + min_c
		minus_c = max_c - min_c
		# Compute Hue
		if max_c == min_c:
			h = 0
		elif max_c == r and g >= b:
			h = 60 * (g - b) / minus_c
		elif max_c == r and g < b:
			h = 60 * (g - b) / minus_c + 360
		elif max_c == g:
			h = 60 * (b - r) / minus_c + 120
		elif max_c == b:
			h = 60 * (r - g) / minus_c + 240

		# Compute Lightness
		l = plus_c / 2

		# Compute Saturation
		if l == 0 or max_c == min_c:
			s = 0
		elif 0 < l <= 0.5:
			s = minus_c / plus_c
		else:
			s = minus_c / (2 - plus_c)

		return f"hsla({int(h + 1)}, {int(s * 100)}%, {int(l * 100)}%, {round(a, 1)})" if a < 1.0 else f"hsl({int(h + 1)} ,{int(100 * s)}%, {int(100 * l)}%)"

	@property
	def red(self):
		return self.rgba[0]

	@red.setter
	def red(self, value):
		_rgba = list(self.rgba)
		_rgba[0] = value
		self.rgba = tuple(_rgba)

	@property
	def green(self):
		return self.rgba[1]

	@green.setter
	def green(self, value):
		_rgba = list(self.rgba)
		_rgba[1] = value
		self.rgba = tuple(_rgba)

	@property
	def blue(self):
		return self.rgba[2]

	@blue.setter
	def blue(self, value):
		_rgba = list(self.rgba)
		_rgba[2] = value
		self.rgba = tuple(_rgba)

	@property
	def alpha(self):
		return self.rgba[3]

	@property
	def hue(self):
		return self.hsl.split(",")[0].strip("hsla()% ")

	@property
	def saturation(self):
		return self.hsl.split(",")[1].strip("hsla()% ")

	@property
	def lightness(self):
		return self.hsl.split(",")[2].strip("hsla()% ")

	@property
	def brightness(self):
		return (round(((self.red * 299) + (self.green * 587) + (self.blue * 114)) / 1000, 2)) % 125

	def saturate(self, value):
		h, s, l, a = self.hue, int(self.saturation), self.lightness, self.rgba[3]
		if s + value < 0:
			s = '0'
		elif s + value > 100:
			s = '100'
		else:
			s = str(s + value)
		self.rgba = hsl_to_rgba((h, s, l, a))

	def lighten(self, value):
		h, s, l, a = self.hue, int(self.saturation), self.lightness, self.rgba[3]
		if l + value < 0:
			l = '0'
		elif l + value > 100:
			l = '100'
		else:
			l = str(l + value)
		self.rgba = hsl_to_rgba((h, s, l, a))

	def __sub__(self, other):
		if not isinstance(other, Color):
			raise ValueError
		return (abs(self.red - other.red) + abs(self.green - other.green) + abs(self.blue - other.blue)) % 500


def color_factory(color):
	if color.startswith("#"):
		color = hex_to_rgba(color.lstrip("#"))
	elif color.startswith("rgb"):
		color = rgba_to_rgba(color.strip("rgba()").split(","))
	elif color.startswith("hsl"):
		color = hsl_to_rgba(color.strip("hsla()").split(","))
	return Color(color)


def convert_color(scope, color):
	if scope == 'rgb':
		return color_factory(color).rgb
	elif scope == "hsl":
		return color_factory(color).hsl
	elif scope == "hex":
		return color_factory(color).hex


@register_filter
def color_extract(color, channel):
	color = color_factory(color)
	return getattr(color, channel)


@register_filter
def color_mix(color, mix_color, amplitude):
	color = color_factory(color).rgba
	mix_color = color_factory(mix_color).rgba

	mixed = [amplitude / 100 * (a + b) for a, b in zip(color, mix_color)]
	return "rgba(%d, %d, %d, %0.3f)" % (mixed[0], mixed[1], mixed[2], mixed[3])


@register_filter
def color_contrast(fg_color, bg_color):
	# TODO: contrast function
	fg = color_factory(fg_color)
	bg = color_factory(bg_color)
	print(fg - bg, fg.brightness - bg.brightness)
	ans = abs((fg - bg) / (fg.brightness - bg.brightness))
	return ans if ans > 1 else 1 / ans


@register_filter
def color_modify(color, channel, value):
	_color = color_factory(color)
	setattr(_color, channel, value)
	if _color.alpha < 1:
		return _color.rgb
	if color.startswith('#'):
		return _color.hex
	elif color.startswith('hsl'):
		return _color.hsl
	return _color.rgb


def change_color_lightness(method, color, value):
	color = color_factory(color)
	value = value if method == "lighten" else -value
	color.lighten(value)
	return color.hex


def change_color_saturation(method, color, value):
	color = color_factory(color)
	value = value if method == "saturate" else -value
	color.saturate(value)
	return color.hex


@register_filter
def color_brightness(color):
	color = color_factory(color)
	return color.brightness


@register_filter
def color_difference(color1, color2):
	color1 = color_factory(color1)
	color2 = color_factory(color2)
	return color1 - color2


@register_filter
def brightness_difference(color1, color2):
	color1 = color_factory(color1)
	color2 = color_factory(color2)
	return int(abs(color1.brightness - color2.brightness))


register_filter('color_to_rgb')(partial(convert_color, 'rgb'))
register_filter('color_to_hsl')(partial(convert_color, 'hsl'))
register_filter('color_to_hex')(partial(convert_color, 'hex'))
register_filter('color_lighten')(partial(change_color_lightness, 'lighten'))
register_filter('color_darken')(partial(change_color_lightness, 'darken'))
register_filter('color_saturate')(partial(change_color_saturation, 'saturate'))
register_filter('color_desaturate')(partial(change_color_saturation, 'desaturate'))
