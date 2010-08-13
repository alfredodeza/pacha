""" Configuration parser. Let's be bold and try to get a better parser
than the Standard Library ConfigParser """

import re

HEADER = re.compile(
r'\['                                 # [
r'(?P<header>[^]]+)'                  # very permissive!
r'\]'                                 # ]
)
OPTION = re.compile(
r'(?P<option>[^:=\s][^:=]*)'          # very permissive!
r'\s*(?P<divider>[:=])\s*'                 # any number of space/tab,
                                      # followed by separator
                                      # (either : or =), followed
                                      # by any # space/tab
r'(?P<value>.*?)(#|$)'                # everything up to eol or a comment
)

class Parse(object):
    """Parses a configuration file"""
    
    def __init__(self,
                 config,
                 new_value = None):
        self.conf = config
        self.new_value = new_value
        self.fileopen()

    def fileopen(self):
        """Open the given file and leave it ready for parsing"""
        try:
            self.config = open(self.conf)
            self.txt = open(self.conf, 'a')
        except IOError, e:
            print e
            return False
        
    def options(self):
        """Return a dictionary of values found in the config file"""
        lines = self.config.read()
        values = {}
        for line in lines.split('\n'):
            if line.startswith('#'): # ommit comments
                pass
            elif not line.strip(): # ommit empty lines
                pass
            else:
                #get_header = HEADER.match(line) #don't do anything just yet
                get_options = OPTION.match(line)
                if get_options:
                    optname, optdivider, optvalue = get_options.group('option',
                                                                        'divider',
                                                                        'value')
                    # make sure we have words without trailing space:
                    new_key = optname.split()[0]
                    new_value = optvalue.split()[0]
                    values[new_key] = new_value
        # matches the attributes from the dicionary to the values:
        for (key, value) in values.items():
            # convert string to list if within brackets
            if value.startswith('['):
                list = eval(value)
                setattr(self, key, list)
            # Convert to dictionary if curly brackets
            elif value.startswith('{'):
                dictionary = eval(value)
                setattr(self, key, dictionary)
            else:
                setattr(self, key, value)
    def text_read(self):
        """Parses a text file line by line. Each line is a value. 
        Returns a list of all the values in the text file.
        Should *not* be edited by hand."""
        lines = self.config.readlines()
        values = []
        for line in lines:
            values.append(line.split('\n')[0])
        return values

    def text_append(self):
        """Appends a value to a newline in a text file"""
        self.txt.write(self.new_value+'\n')
        self.txt.close()
