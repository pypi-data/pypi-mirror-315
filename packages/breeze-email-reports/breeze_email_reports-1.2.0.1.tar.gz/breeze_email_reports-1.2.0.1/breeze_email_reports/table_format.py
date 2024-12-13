import csv
import html
from abc import abstractmethod
from io import IOBase
from typing import List, Tuple, Union, Dict

# Pad string to length, e.g. f'{a<15}' will pad to 15 chars.


class ColSpec:
    def __init__(self,
                 title: str,
                 header_attrs: Dict[str, str] = {},
                 row_attrs: Dict[str, str] = {},
                 width: int = 0):
        """
        Column specifications for table formatter
        :param title: Column title
        :param header_attrs: HTML attributes for header (if appropriate)
        :param row_attrs: HTML attributes for data rows (if appropriate)
        :param width: width of column for text formatting
        """
        self.title_val = title
        self.header_attrs_val = header_attrs if header_attrs else row_attrs
        self.row_attrs_val = row_attrs if row_attrs else header_attrs
        self.width_val = width

    @property
    def title(self):
        return self.title_val

    @property
    def header_attrs(self):
        return self.header_attrs_val

    @property
    def row_attrs(self):
        return self.row_attrs_val

    @property
    def width(self):
        return self.width_val


class _ReportFormatter:
    def __init__(self,
                 column_specs: List[ColSpec],
                 caption: str = "",
                 id_top: bool = True):
        """
        Base settings for report formatters
        :param column_specs: List of column specifications
        :param caption: Caption to put at top of table
        :param id_top: If true(default) identification information is in a row at
            the top of each group. If false, It's in its own spanned column to
            the left of the data.
        """
        self.column_specs = column_specs
        self.columns = len(column_specs)
        self.id_top = id_top
        self.caption = caption

    @abstractmethod
    def format_table(self,
                     data: List[Tuple[str, List[Union[str, List[str]]]]],
                     output: IOBase):
        """
        Format the data in appropriate format and write to output
        :param data: Data for the table
        :param output: Output stream to write to.
        :return: None
        The input data is a list of tuples. The first value is a group header
        that divides subsequent data. (A member name in this context.) The second
        value is a list of tuples, each with label for the tuple followed by values
        for columns in the row. Each column value can be None, a string, or a list
        of strings.

        Note: If self.id_top is true, the string in the first value of each Tuple
        should go in a spanned row the data entry rows.
        If self.id_top is false, the data in the first value of each tuple goes
        in the first column of each group, spanned down across the data values.
        The information from the list of values goes in subsequent rows.
        """
        pass


def _tokenize(v):
    if isinstance(v, float):
        return [f'{v:.2f}']
    elif isinstance(v, str):
        return v.split(';')
    else:
        return v


def _escape_html_value(val: Union[str, List[str]]) -> str:
    if val:
        if isinstance(val, list):
            # For lists in HTML break each item on semicolons (for addresses).
            # But we have to do that before the html.escape() because that
            # introduces semicolons.
            return '<br/>'.join([html.escape(i) for elt in val
                                 for i in _tokenize(elt)
                                 ])
        else:
            return html.escape(val)
    else:
        return ' '


def _attr_str(attrs: Dict[str, str]) -> str:
    """
    Return a string suitable for html style of attribute map
    :param attrs: Attributes
    :return: Attributes turned into a string
    """
    return ' '.join([f'{k}: {v};' for k, v in attrs.items()])


class _HTMLFormatter(_ReportFormatter):
    def __init__(self,
                 *args,
                 top_attrs: Dict[str, str] = {},
                 **kwargs):
        """
        Format as HTML
        :param args: Standard arguments
        :param top_attrs: if id_top is set, HTML attributes for the spanned id row
        :param kwargs:
        """
        _ReportFormatter.__init__(self, *args, **kwargs)
        self.table_header = ('<table border="1" style="border:1px solid #000000;'
                             'border-collapse:collapse" cellpadding="4">\n')
        self.top_attrs = top_attrs

    def format_table(self,
                     data: List[Tuple],
                     output: IOBase):
        """
        Format as an HTML table
        :param data:
        :param output:
        :return:
        """
        output.write('<head>\n<style>\n')
        for c in range(len(self.column_specs)):
            output.write(f'#r1 td:nth-child({c+1}) '
                         f'{{ {_attr_str(self.column_specs[c].row_attrs)} }}\n')
            output.write(f'th td:nth-child({c+1}) '
                         f'{{ {_attr_str(self.column_specs[c].header_attrs)} }}\n')
        for c in range(1, len(self.column_specs)):
            output.write(f'#rn td:nth-child({c}) '
                         f'{{ {_attr_str(self.column_specs[c].row_attrs) }}}\n')

        if self.id_top:
            output.write(f'#hr {{ {_attr_str(self.top_attrs)} }}\n')

        column_specs = self.column_specs
        if not self.id_top:
            # Ignore first column when outputting data rows
            column_specs = column_specs[1:]
        number_columns = len(column_specs)

        output.write(f'th {{ {_attr_str(self.column_specs[0].header_attrs)} }}\n')
        output.write('</style>\n</head>\n<body>\n')

        output.write('<table border="1" style="border:1px thick double black";'
                     'border-collapse:collapse" cellpadding="4">\n')
        if self.caption:
            cap = self.caption.replace('\n', '<br/>')
            output.write(f'<caption><b>{cap}</b></caption>\n')
        nl = '\n'
        row = nl.join([f'  <th>{c.title}</th>'
                       for c in self.column_specs])
        output.write(f'{nl} <tr>{nl}{row}{nl} </tr>{nl}')

        for name, values in data:
            name = html.escape(name)
            if self.id_top:
                # Identifying info goes in first row at the top
                output.write(f'<tr id="hr">\n  <td colspan="{self.columns}" '
                             f'<b>{name}</b></td>\n</tr>\n')
                first_col_data = None
            else:
                # Identifying information goes in first column of first row
                person_info = name.replace('\n', '<br/>\n')
                first_col_data = (f'<tr id="r1"><td rowspan={len(values)}>\n'
                                  f'{person_info}</td>\n')

            for row in values:
                if first_col_data:
                    output.write(first_col_data)
                    first_col_data = None
                else:
                    output.write(f' <tr id="rn">\n')
                for i in range(number_columns):
                    # cs = column_specs[i]
                    colval = _escape_html_value(row[i])
                    output.write(f'  <td>{colval}</td>\n')
                output.write(' </tr>\n')

        output.write('</table>\n')


def _splitval(val: str, cs: ColSpec, splits: str = ';: ') \
        -> Tuple[str, Union[str, None]]:
    """
    Split a string if too long
    :param val: Value to split
    :param cs: ColSpec with desired length
    :return: Tuple, parts of val before and after the split
    """
    # use .strip() to remove pre and post whitespace
    if not val:
        return '', None
    if len(val) <= cs.width:
        return val, ''
    last_found = cs.width - 1
    found_char = None
    for c in splits:
        end = cs.width if c == ' ' else cs.width - 1
        found = val.rfind(c, 0, end)
        if found > 0:
            last_found = found
            found_char = c
            break

    first = val[:last_found] if found_char == ' ' else val[:last_found + 1]
    second = val[last_found + 1:]
    return first, second


class _ToFileFormatter(_ReportFormatter):
    def __init__(self, *args, **kwargs):
        _ReportFormatter.__init__(self, *args, **kwargs)
        # self.line_mark = '   |'
        # self.row_prefix = self.line_mark
        # for cs in self.column_specs:
        #     self.line_mark += ''.rjust(cs.width, '-') + '|'

    def format_table(self,
                     data: List[Tuple],
                     output: IOBase):
        """
        Format as an text table
        :param data:
        :param output:
        :return:
        """
        for section in data:
            name, values = section
            self.start_section(name, output)
            for row in values:
                more = True
                self.start_group(output)
                # print(self.line_mark, file=output)
                while more:
                    # print(self.row_prefix, end='', file=output)
                    more = False
                    next_values = []
                    this_row = []
                    for i in range(min(len(row), self.columns)):
                        cs = self.column_specs[i]
                        colval = row[i]
                        nextval = []
                        if colval:
                            if isinstance(colval, list):
                                curval = colval[0]
                                nextval = colval[1:]
                                if nextval:
                                    more = True
                            else:
                                curval = colval
                                nextval = []
                            curval, overflow = self.splitval(curval, cs)
                            if overflow:
                                nextval = [overflow] + nextval
                                more = True
                        else:
                            curval = ''
                        this_row.append(curval if curval else '')
                        next_values.append(nextval)

                    self.emit_row(this_row, output)
                    row = next_values

            # print(self.line_mark, file=output)
            self.end_section(output)
        self.finish_output(output)

    @abstractmethod
    def start_section(self, name: str, output: IOBase):
        pass

    def end_section(self, output: IOBase):
        pass

    def start_group(self, output):
        pass

    def splitval(self, val: str, cs: ColSpec) -> Tuple[str, Union[str, None]]:
        return val, None

    def emit_row(self, values: List[str], output: IOBase):
        pass

    def finish_output(self, output: IOBase):
        pass


class _TextFormatter(_ToFileFormatter):
    def __init__(self, *args, **kwargs):
        _ToFileFormatter.__init__(self, *args, **kwargs)
        self.line_mark = '   |'
        self.row_prefix = self.line_mark
        for cs in self.column_specs:
            self.line_mark += ''.rjust(cs.width, '-') + '|'

    def start_section(self, name: str, output: IOBase):
        print('', file=output)
        print(name, file=output)

    def start_group(self, output):
        print(self.line_mark, file=output)

    def splitval(self, val: str, cs: ColSpec) -> Tuple[str, str]:
        ret_val, overflow = _splitval(val, cs)
        return ret_val.replace('\n', ';'), ('+' + overflow) if overflow else None

    def emit_row(self, values: List[str], output: IOBase):
        print(self.row_prefix, end='', file=output)
        for i in range(len(values)):
            v = values[i]
            cs = self.column_specs[i]
            v = v.ljust(cs.width)
            print(v + '|',
                  end='',
                  file=output)
            output.flush()
        print('', file=output)

    def end_section(self, output: IOBase):
        print(self.line_mark, file=output)


class _CSVFormatter(_ToFileFormatter):
    def __init__(self, *args, **kwargs):
        _ToFileFormatter.__init__(self, *args, **kwargs)
        self.writer = None

    def start_section(self, name: str, output: IOBase):
        if not self.writer:
            self.writer = csv.writer(output)
        self.writer.writerow([name])

    def emit_row(self, values: List[str], output: IOBase):
        self.writer.writerow([''] + values)
