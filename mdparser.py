import json

class JSONToMarkdownParser(object):
    def parse(self, content_in, filename_out):
        with open(filename_out, 'w') as f_out:
            python_type = json.loads(content_in)
            lines = python_type['root']['children']

            for line in lines:
                tag = line.get('type')
                text = line.get("text")
                formats = line.get("formats")
                checked = line.get("checked")

                parsed_line = self.format_text(tag, text, formats, checked)

                print(parsed_line, file=f_out)

    def format_text(self, tag, text, formats, checked):

        conversion_table = { "h1" : ("# ", '')
                           , "h2" : ("## ", '')
                           , "h3" : ("### ", '')
                           , "p" : ('', '')
                           , "cl" : ("[x] " if checked else "[ ] ", "")
                           , "b" : ('*', '*')
                           , "i" : ('_', '_')
                           , "code" : ('`', '`')
                           , "pre" : ("``` \n", "\n```")
                           , "ul": ("- ", '')
                           , "ol": ("1. ", '')
                           }

        if formats:
            chars = list(text)

            position_list = []
            for (i_tag, indexes) in formats.items():
                for index in indexes:
                    position_list.append((i_tag, index))

            position_list.sort(key=lambda x: x[1])

            offset_counter = 0
            for (i_tag, index) in position_list:
                chars.insert(index + offset_counter, conversion_table[i_tag][0])
                offset_counter += 1

            text = "".join(chars)

        opening = conversion_table[tag][0]
        closing = conversion_table[tag][1]
        return "{}{}{}".format(opening, text, closing)