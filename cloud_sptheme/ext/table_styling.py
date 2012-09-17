"""cloud_sptheme.ext.table_styling -- add directives for styling tables

This extension is an initial attempt at doing table column styling.
It currently attempts to parse the latex-specific ``tabularcolumns`` directive,
and generates css styling for table columns and cells based on the subset
of the latex directives which it understands.

This currently includes all the commands ``|lrcLRCJX``,
though vertical bars only generate css classes, and leave it up to the theme
to add them.

.. todo::

    * document this
    * add some unittests
    * consider a separate directive which isn't as latex-specific as tabularcolumns
      (could generate default value for that directive, though)
"""
import inspect
import sys
from docutils import nodes
from sphinx.builders.html import HTMLTranslator

def lex_tabcolspec(spec, warn):
    "helper to turn tabularcolumns string into (cmd, param) tokens"
    cmd = param = err = None
    level = 0
    for char in spec:
        if level:
            if char == "}":
                level -= 1
                if not level:
                    if cmd:
                        yield cmd, param
                cmd = param = None
            else:
                if char == "{":
                    level += 1
                param += char
            continue
        if cmd:
            yield cmd, None
        if char == "{":
            if not cmd:
                err = True
            param = ""
            level = 1
        elif char in "\\}":
            err = True
            cmd = None
        else:
            cmd = char
    if cmd:
        yield cmd, param
    if err:
        warn("can't fully parse string: %r" % spec)

class TableStylingHTMLTranslatorMixin(HTMLTranslator):
    """class which adds support for table-styling directive"""

    def __init__(self, *args, **kwds):
        # hack for classobj, instead of super()
        mro = inspect.getmro(self.__class__)
        self.__parent = mro[mro.index(TableStylingHTMLTranslatorMixin)+1]
        self.__parent.__init__(self, *args, **kwds)
        self.tabspecmap = None

    # maps cmds w/ no params -> css style
    _tabspec_noparam = dict(
        l="text-align: left; whitespace: no-wrap",
        r="text-align: right; whitespace: no-wrap",
        c="text-align: center; whitespace: no-wrap",
        L="text-align: left",
        R="text-align: right",
        C="text-align: center",
        J="text-align: justify",
        X="vertical-align: top",
    )

    # maps paragraph+alignment directives -- expects {width} param
    _tabspec_valign = dict(p="top", m="middle", b="bottom")

    # maps barcount to class that will be added
    _tabspec_bar = ["no-left-border", "left-border", "double-left-border"]

    def _get_tabspec_style(self, cmd, param, warn):
        "convert directive for single column into css style & width"
        style = self._tabspec_noparam.get(cmd)
        if style is not None:
            if param:
                warn("unexpected '{...}' parameter after %r command" % cmd)
            return style, None

        valign = self._tabspec_valign.get(cmd)
        if valign:
            style = "vertical-align: " + valign
            width = None
            if not param:
                warn("expected width after %r command" % cmd)
            elif param and re.match("^\d(\.\d+)(pt|mm|cm|in|ex|em|%)$", param):
                width = param
            return style, width

        warn("unknown command %r" % cmd)
        return None, None

    def visit_tabular_col_spec(self, node):
        "parse tabularcolumns spec into column widths, styles, and classes"
        # the tabularcolumns format was intended for latex,
        # this attempts to translate a subset of the spec to css.
        # info taken from
        #   http://en.wikibooks.org/wiki/LaTeX/Tables
        #   http://www.tug.org/TUGboat/tb28-3/tb90hoeppner.pdf
        def warn(msg):
            self.builder.warn("tabularcolumns specification: " + msg,
                              (self.builder.current_docname, self.node.line))
        spec = node['spec']
        self.tabspecmap = tabspecmap = {}
        idx = 0
        bars = 0
        for cmd, param in lex_tabcolspec(spec, warn):
            if cmd == "|":
                if bars == 2:
                    warn("too many bar in a row")
                else:
                    bars += 1
                continue
            elif cmd in "<>@":
                continue
            style, width = self._get_tabspec_style(cmd, param, warn)
            bcls = self._tabspec_bar[bars]
            bars = 0
            if idx:
                tabspecmap[idx-1]['classes'].append(bcls.replace("left","right"))
            # NOTE: 'width' used by colgroup, style/classes used by td elements
            tabspecmap[idx] = dict(style=style, width=width, classes=[bcls])
            idx += 1
        if idx:
            bcls = self._tabspec_bar[bars]
            tabspecmap[idx-1]['classes'].append(bcls.replace("left","right"))
        raise nodes.SkipNode

    def _write_colspec(self, idx, node, twidth):
        "write single <col> entry"
        try:
            width = self.tabspecmap[idx]['width']
        except KeyError:
            width = None
        if width is None:
            width = '%i%%' % int(node['colwidth'] * 100.0 / twidth + 0.5)
        self.body.append(self.emptytag(node, 'col', width=width))

    def write_colspecs(self):
        "write <colgroup> contents"
        # overridden from base class
        # (docutils.writers.html4css1:HTMLTranslator.write_colspecs)
        # in order to allow width to be customized
        twidth = 0
        for node in self.colspecs:
            twidth += node['colwidth']
        for idx, node in enumerate(self.colspecs):
            self._write_colspec(idx, node, twidth)
        self.colspecs = []

    def _get_entry_options(self, node):
        "generates (tagname, attrmap) for table cell entry"
        # replicated from base visit_entry() method
        atts = {'class': []}
        if isinstance(node.parent.parent, nodes.thead):
            atts['class'].append('head')
        if node.parent.parent.parent.stubs[node.parent.column]:
            # "stubs" list is an attribute of the tgroup element
            atts['class'].append('stub')
        if atts['class']:
            tagname = 'th'
        else:
            tagname = 'td'
        if 'morerows' in node:
            atts['rowspan'] = node['morerows'] + 1
        if 'morecols' in node:
            atts['colspan'] = node['morecols'] + 1
            node.parent.column += node['morecols']

        # add tabspecmap options
        col = node.parent.column
        if self.tabspecmap and col in self.tabspecmap:
            opts = self.tabspecmap[col]
            if 'classes' in opts:
                atts['class'].extend(opts['classes'])
            if 'style' in opts:
                atts['style'] = opts['style']

        # replicated from base visit_entry() method
        if atts['class']:
            atts['class'] = ' '.join(atts['class'])
        else:
            del atts['class']
        return tagname, atts

    def visit_entry(self, node):
        "visit table cell entry"
        # overridden from base class to allow style & class to be modified
        tagname, atts = self._get_entry_options(node)
        node.parent.column += 1
        self.body.append(self.starttag(node, tagname, '', **atts))
        self.context.append('</%s>\n' % tagname.lower())
        if len(node) == 0:              # empty cell
            self.body.append('&nbsp;')
        self.set_first_last(node)

    def depart_table(self, node):
        "clear tabspecmap after table rendered"
        self.__parent.depart_table(self, node)
        self.tabspecmap = None

def install_translator(app):
    """install mixin class into html translator"""
    builder = app.builder
    if builder.name != "html":
        return
    cur = builder.translator_class
    assert issubclass(cur, HTMLTranslator)
    base = TableStylingHTMLTranslatorMixin
    if issubclass(cur, base):
        pass
    if issubclass(base, cur):
        builder.translator_class = base
    else:
        class TableStylingHTMLTranslator(base, cur):
            "dynamically created class, merging mixin into custom translator"
            pass
        builder.translator_class = TableStylingHTMLTranslator

def setup(app):
    app.connect('builder-inited', install_translator)
