"""
Tag for paginate

{% if paginate.next.is_link %}
    <a href="{{ paginate.next.url }}">{{ paginate.next.title }}</a>
{% endif %}
"""

from varname import namedtuple
from ..tagmgr import register_tag
from ..tag import Tag
from ..tagfrag import try_render

ForLoop = namedtuple(  # pylint: disable=invalid-name
	['first', 'index', 'index0', 'last',
	 'length', 'rindex', 'rindex0']
)


@register_tag
class TagPaginate(Tag):
	"""Class for paginate tag"""

	SYNTAX = r"""
    inner_tag: tag_paginate
    !tag_paginate: $tagnames VAR "in" atom paginate_args*
    ?paginate_args: paginate_current_offset_arg | paginate_current_page_arg | paginate_items_arg | paginate_parts_arg | paginate_next_arg | paginate_previous_arg | paginate_page_size_arg | paginate_pages_arg
    paginate_current_offset_arg: "current_offset" ":" (int|var)
    paginate_current_page_arg: "current_page" ":" (int|var)
    paginate_items_arg: "items" ":" (int|var)
    paginate_parts_arg: "parts" ":" (int|var)
    paginate_next_arg: "next" ":" (int|var)
    paginate_previous_arg: "previous" ":" (int|var)
    paginate_page_size_arg: "page_size" ":" (int|var)
    paginate_pages_arg: "pages" ":" (int|var)
    """

	def t_paginate_current_offset_arg(self, arg):
		"""Transformer for paginate_current_offset_arg"""
		return ('current_offset', arg)

	def t_paginate_current_page_arg(self, arg):
		"""Transformer for paginate_current_page_arg"""
		return ('current_page', arg)

	def t_paginate_items_arg(self, arg):
		"""Transformer for paginate_items_arg"""
		return ('items', arg)

	def t_paginate_parts_arg(self, arg):
		"""Transformer for paginate_parts_arg"""
		return ('items', arg)

	def t_paginate_next_arg(self, arg):
		"""Transformer for paginate_next_arg"""
		return ('next', arg)

	def t_paginate_previous_arg(self, arg):
		"""Transformer for paginate_previous_arg"""
		return ('previous', arg)

	def t_paginate_page_size_arg(self, arg):
		"""Transformer for paginate_page_size_arg"""
		return ('page_size', arg)

	def t_paginate_pages_arg(self, arg):
		"""Transformer for paginate_pages_arg"""
		return ('pages', arg)

	def t_tag_tablerow(self, tagname, varname, _in, atom, *args):
		"""Transformer for tag tablerow"""
		return TagPaginate(tagname, (varname, atom, args))

	def _render(self, local_envs, global_envs):
		rendered = ''
		varname, obj, args = self.data
		obj = try_render(obj, local_envs, global_envs)
		args = dict(args)
		for key, val in args.items():
			args[key] = try_render(val, local_envs, global_envs)

		offset = args.get('offset')
		limit = args.get('limit')

		# parameters
		if offset is not None and limit is not None:
			obj = obj[offset: (offset + limit)]
		elif offset is not None:
			obj = obj[offset:]
		elif limit is not None:
			obj = obj[:limit]

		# make it avaiable for generators
		obj = list(obj)
		lenobj = len(obj)

		cols = args.get('cols', lenobj)
		# chunks
		rows = [obj[i:i + cols] for i in range(0, lenobj, cols)]
		local_envs_inside = local_envs.copy()
		for i, row in enumerate(rows):
			rendered += f'<tr class="row{i + 1}">'
			for j, col in enumerate(row):
				local_envs_inside[varname] = col
				rendered += f'<td class="col{j + 1}">'
				rendered += self._children_rendered(local_envs_inside,
													global_envs)
				rendered += '</td>'

			rendered += '</tr>'

		return rendered
