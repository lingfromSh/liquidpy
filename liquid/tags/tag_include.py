"""Tag increment

{% include 'collection-sidebar' %}
{% include 'blog-sidebar' %}
"""
from ..tagmgr import register_tag
from ..tag import Tag


@register_tag
class TagInclude(Tag):
	"""Class for tag include"""
	VOID = True
	SYNTAX = r"""
    inner_tag: tag_include
    !tag_include: $tagnames STRING
    """

	def t_tag_include(self, tagname, snippet_name):
		"""Transformer for tag include"""
		return TagInclude(tagname, snippet_name)

	def _render(self, local_envs, global_envs):
		# Variables created inferred by include tag are snippets object
		# TODO: self.data [Token]
		snippet = global_envs["envs"].get(str(self.data).strip("'"), "")
		if hasattr(snippet, "render"):
			return snippet.render(settings=global_envs.get("settings", dict()))
		return ""
