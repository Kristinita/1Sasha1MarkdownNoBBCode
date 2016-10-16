#
# 	Base on codes:
# 	https://gist.github.com/sma/1513929
#	https://github.com/m3mnoch/MarkdownToBBCode/blob/master/MarkdownToBBCode.py
#


import sublime, sublime_plugin
import re, sys

class MarkdowntobbcodeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		allcontent = sublime.Region(0, self.view.size())

		regionString = self.markdown_to_bbcode(str(self.view.substr(allcontent)))
		self.view.replace(edit, allcontent, regionString)

	def markdown_to_bbcode(self,s):

		def translate(p="%s", g=1):
			def inline(m):
				s = m.group(g)
				#
				# Headers
				#
				s = re.sub(r"^#\s+(.*?)\s*$", "[h1]\\1[/h1]", s)   # # Header first level
				s = re.sub(r"^##\s+(.*?)\s*$", "[h2]\\1[/h2]", s)  # ## Header second level
				s = re.sub(r"^###\s+(.*?)\s*$", "[h3]\\1[/h3]", s) # ### Header third level
				s = re.sub(r"^####\s+(.*?)\s*$", "[h4]\\1[/h4]", s)# #### Header fourth level
				#
				# Lists
				#
				s = re.sub(r"(?m)^[-+*]\s+(.*)$", translate("№[list]\n[*]%s\n[/list]"), s) # + Marked + List
				s = re.sub(r"(?m)^\d+\.\s+(.*)$", translate("№[list=1]\n[*]%s\n[/list]"), s) # 1. Numbered 2. List
				#
				# Quote
				#
				s = re.sub(r"^> (.*)$", "[quote]\\1[/quote]", s) # > Quote
				#
				# Thematic break
				#
				s = re.sub(r"^-{3}(\s*)$", "[hr]", s)
				return p % s
			return inline

		#
		# URL and images
		#
		s = re.sub(r"!\[(.*?)\]\((.*?)\)", "[img]\\2[/img]", s)   # ![IMG description](URL of image), alt attribute not supported in many forums
		s = re.sub(r"\[(.*?)\]\((.*?)\)", "[url=\\2]\\1[/url]", s)# [URL description](URL link)
		s = re.sub(r"<(https?:\S+)>", "[url]\\1[/url]", s)        # <URL>
		#
		# Code
		#
		s = re.sub(r"`{3}([^`]+)`{3}", "[code]\\1[/code]", s)# ```Multiline\n\code```
		s = re.sub(r"`([^`]+)`", "[code]\\1[/code]", s)      # `Code`
		s = re.sub(r"(?m)^ {4}(.*)$", "№[code]\\1[/code]", s)# Code fragment after 4 spaces
		s = re.sub(r"(?m)^\t(.*)$", "№[code]\\1[/code]", s)  # Code fragment after tab
		#
		# Bold and italic
		#
		s = re.sub(r"_{2}([\s\S]+?)_{2}", "[b]\\1[/b]", s)  # __Bold__
		s = re.sub(r"_([^_]+?)_", "[i]\\1[/i]", s)   		# _Italic_ Needs hack (?<=\s), because _ symbol often use in URLs
		s = re.sub(r"\*{2}([\s\S]+?)\*{2}", "[b]\\1[/b]", s)# **Bold**
		s = re.sub(r"\*([^\*]+?)\*", "[i]\\1[/i]", s)       # *Italic*.
		#
		# Strikethrough text
		#
		s = re.sub(r"~{2}([\s\S]+?)~{2}", "[s]\\1[\s]", s)
		#
		# Dependencies. Not delete these lines!
		#
		s = re.sub(r"(?m)^((?!№).*)$", translate(), s)
		s = re.sub(r"(?m)^№\[", "[", s)
		s = re.sub(r"\[/code]\n\[code(=.*?)?]", "\n", s)
		s = re.sub(r"\[/list]\n\[list(=1)?]\n", "", s)
		s = re.sub(r"\[/quote]\n\[quote]", "\n", s)

		return s
