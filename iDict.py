
from collections import OrderedDict
import datetime
import base64

class iDict(OrderedDict):
    def __init__(self, node):
        super(OrderedDict, self).__init__()

        i = iter(node)
        for k,v in zip(i,i):
            if v.tag == 'integer':
                self[k.text] = int(v.text)
            elif v.tag == 'string':
                self[k.text] = v.text
            elif v.tag == 'true' or v.tag == 'false':
                self[k.text] = (v.tag == 'true')
            elif v.tag == 'date':
                item = datetime.datetime.strptime(v.text, "%Y-%m-%dT%H:%M:%SZ")
                self[k.text] = item.replace(tzinfo=datetime.timezone.utc)
            elif v.tag == 'dict':
                self[k.text] = iDict(v)
            elif v.tag == 'array':
                self[k.text] = iter(v)
            elif v.tag == 'data':
                self[k.text] = base64.b64decode(v.text)
            else:
                raise TypeError("Unhandled value type: "+v.tag)

#
# Editor modelines  -  https://www.wireshark.org/tools/modelines.html
#
# Local variables:
# c-basic-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# coding: utf8
# mode: python
# End:
#
# vi: set shiftwidth=4 tabstop=4 expandtab fileencoding=utf8 filetype=python:
# :indentSize=4:tabSize=4:noTabs=true:coding=utf8:mode=python:
#
