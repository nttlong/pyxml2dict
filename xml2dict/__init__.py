def parse_node(root):
    ret = {}
    if not hasattr(root,"tagName"):
        return
    property_name = root.tagName
    children = [n for n in root.childNodes if hasattr(n,"tagName")]
    if hasattr(root,"attributes") and root.attributes.length>0:
        _type = root.attributes.get("type", None)
        _value = root.attributes.get("value", None)
        if _value != None:
            _value = _value.value
        if _type != None:
            _type = _type.value
        data_type = None
        if _type != None:
            if not __builtins__.has_key(_type):
                raise Exception("'{0}' is invalid data type".format(_type))
            data_type = __builtins__[_type]
        if data_type == list:
            lst = [parse_node(n) for n in children]
            ret.update({
                property_name:lst
            })
        elif data_type == None:
            ret.update({
                property_name:_value
            })
        else:
            ret.update({
                property_name: data_type(_value)
            })
    else:
        sub = {}
        for n in children:
            ret_n = parse_node(n)
            if ret_n != None:
                sub.update(ret_n)
        ret.update({
            property_name:sub
        })

    return ret




def load_from_file(file_path):
    from xml.dom import minidom
    nodes = minidom.parse(file_path)
    return parse_node(nodes.childNodes[0])
