"""Tag section

{% section 'bloglist_inner_content' %}
"""

from ..tagmgr import register_tag
from ..tag import Tag


@register_tag
class TagSection(Tag):
	"""Class for section tag."""
	VOID = True
	SYNTAX = r"""
	inner_tag: tag_section
	!tag_section: $tagnames STRING
	"""

	def t_tag_section(self, tagname, section_name):
		"""Transformer for tag section."""
		return TagSection(tagname, section_name)

	def _render(self, local_envs, global_envs):
		# Variables created inferred by include tag are sections liquid object
		section = global_envs["envs"].get(str(self.data).strip("'"), "")
		if hasattr(section, "render"):
			return section.render(settings=global_envs.get("settings", dict()))
		return ""
