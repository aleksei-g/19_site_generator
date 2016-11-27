import markdown
import re
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern


DIV_QUESTION = r'(\[q\s)(.*?)\]'


class AttrTagPattern(Pattern):
    def __init__(self, pattern, tag, attrs):
        Pattern.__init__(self, pattern)
        self.tag = tag
        self.attrs = attrs

    def handleMatch(self, m):
        el = markdown.util.etree.Element(self.tag)
        el.text = m.group(3)
        for (key, val) in self.attrs.items():
            el.set(key, val)
        return el


class EditorWrapper(markdown.preprocessors.Preprocessor):
    def run(self, lines):
        text = "\n".join(lines)
        text = text.split("\n\n")
        new_text = []
        for block in text:
            if block.startswith('===\n') and block.endswith('\n==='):
                new_lines = []
                editor_medium_text = re.search(
                    r'(?<====\npower medium\n===\n)[\s\S]*?(?=\n===)', block)
                solution_text = re.search(r'(?<=\n===\n)[\s\S]+?(?=\n===)',
                                          block[editor_medium_text.regs[0][1]:]
                                          )
                new_lines.append('\n<div class="editor_wrapper">')
                editor_medium_str = ''.join(
                    ('<div class="editor medium" id="editor_id_power">',
                     editor_medium_text.group(),
                     '</div>'))
                new_lines.append(editor_medium_str)
                new_lines.append('<div class="editor_actions"></div>')
                solution_str = ''.join(
                    ('<div class="solution" style="display: none">',
                     solution_text.group(),
                     '</div>'))
                new_lines.append(solution_str)
                new_lines.append('</div>\n')
                new_block = "\n".join(new_lines)
            else:
                new_block = block + '\n'
            new_text.extend(new_block.split('\n'))
        return new_text


class MyExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('div_editor_wrapper', EditorWrapper(md), '_begin')
        div_question_tag = AttrTagPattern(DIV_QUESTION, 'div',
                                          {'class': 'question'})
        md.inlinePatterns.add('div_question', div_question_tag, '>not_strong')
