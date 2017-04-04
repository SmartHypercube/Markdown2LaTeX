#!/usr/bin/python3
# encoding=utf-8

import sys
import mistune

# see http://0x01.me/Python字符编码的一个坑/
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout.detach())
sys.stdin = codecs.getreader('utf8')(sys.stdin.detach())


class LaTeXRenderer(mistune.Renderer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.replace = True

    def block_code(self, code, lang=None):
        code = code.rstrip('\n')
        if lang and code:
            code = self.escape(code)
            return '\\begin{lstlisting}[language=%s, frame=single]\n%s\n\\end{lstlisting}\n\n' % (lang, code)
        if lang:
            lang, _, filename = lang[:-1].partition('[')
            return '\\lstinputlisting[language=%s, frame=single, caption={%s}]{%s}\n\n' % (lang, self.escape(filename), filename)
        code = self.escape(code)
        return '\\begin{lstlisting}[frame=single]\n%s\n\\end{lstlisting}\n\n' % code

    def block_quote(self, text):
        return '\\begin{quote}%s\n\\end{quote}\n\n' % text.rstrip('\n')

    def header(self, text, level, raw=None):
        levels = ['',
                  'section',
                  'subsection',
                  'subsubsection',
                  'paragraph',
                  'subparagraph',
                  'subparagraph']
        return '\\%s{%s}\n\n' % (levels[level], text)

    def hrule(self):
        return '\\hrule\n\n'

    def list(self, body, ordered=True):
        cmd = 'enumerate' if ordered else 'itemize'
        return '\\begin{%s}\n%s\\end{%s}\n\n' % (cmd, body, cmd)

    def list_item(self, text):
        return '\\item %s\n' % text

    def paragraph(self, text):
        return '%s\n\n' % text.strip(' ')

    def table(self, header, body):
        raise NotImplementedError

    def table_row(self, content):
        raise NotImplementedError

    def table_cell(self, content, **flags):
        raise NotImplementedError

    def double_emphasis(self, text):
        return '\\textbf{\\emph{%s}}' % text

    def emphasis(self, text):
        return '\\emph{%s}' % text

    def codespan(self, text):
        return '\\texttt{%s} ' % self.escape(text.rstrip())

    def linebreak(self):
        return '\\\n'

    def strikethrough(self, text):
        raise NotImplementedError

    def text(self, text):
        return self.escape(text)

    def escape(self, text):
        if not text:
            return ''
        newtext = ''
        for c in text:
            if c == '$':
                newtext += c
                self.replace = not self.replace
                continue
            if self.replace:
                # c = c.replace('\\', '\\textbackslash')
                # c = c.replace('{', '\\{')
                # c = c.replace('}', '\\}')
                # c = c.replace('\\textbackslash', '\\textbackslash{}')
                c = c.replace('~', '\\textasciitilde{}')
                c = c.replace('#', '\\#')
                # c = c.replace('$', '\\$')
                c = c.replace('%', '\\%')
                c = c.replace('^', '\\textasciicircum{}')
                c = c.replace('&', '\\&')
                c = c.replace('_', '\\_')
            newtext += c
        return newtext

    def autolink(self, link, is_email=False):
        return self.escape(link)

    def link(self, link, title, text):
        return '\\href{%s}{%s}' % (self.escape(link), self.escape(text))

    def image(self, src, title, text):
        if text:
            return '\\ref{%s}%%\n' \
                   '\\begin{figure}[htbp]\n' \
                   '    \\centering\n' \
                   '    \\includegraphics[width=0.8\\linewidth]{%s}\n' \
                   '    \\caption{%s}\n' \
                   '    \\label{%s}\n' \
                   '\\end{figure}%%\n' \
                   % (text, src, self.escape(title), text)
        return '\\begin{figure}[H]\n' \
               '    \\centering\n' \
               '    \\includegraphics[width=0.8\\linewidth]{%s}\n' \
               '    \\caption{%s}\n' \
               '\\end{figure}\n\n' \
               % (src, self.escape(title))

    def footnote_ref(self, key, index):
        return '\\footnotemark'

    def footnote_item(self, key, text):
        return '\\footnotetext{%s}' % text.rstrip()

    def footnotes(self, text):
        return text


def main():
    text = sys.stdin.read()
    front_matter, _, text = text.partition('\n---\n')
    args = {}
    for l in front_matter.split('\n'):
        if ':' in l:
            key, _, value = l.partition(': ')
            args[key] = value
    title = args['title']
    author = args['author']
    renderer = LaTeXRenderer()
    parser = mistune.Markdown(renderer=renderer)
    print(r'''\documentclass[12pt,a4paper]{article}

\usepackage{ctex}
\usepackage[paper=a4paper,includefoot,margin=54pt]{geometry}
\usepackage[colorlinks,linkcolor=black,anchorcolor=black,citecolor=black,unicode]{hyperref}
\usepackage{float}
\usepackage{listings}

\renewcommand{\lstlistingname}{程序}
\renewcommand{\contentsname}{目录}
\renewcommand{\abstractname}{摘要}
\renewcommand{\refname}{参考文献}
\renewcommand{\indexname}{索引}
\renewcommand{\figurename}{图}
\renewcommand{\tablename}{表}
\renewcommand{\appendixname}{附录}

\begin{document}

\title{%s}
\author{%s}

\maketitle
\tableofcontents
\newpage
''' % (title, author))
    print(parser(text))
    print('\\end{document}')

if __name__ == '__main__':
    main()
