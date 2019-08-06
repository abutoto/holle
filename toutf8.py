def replaceholder(value):
    #把一个不知道什么类型的返回值，改造为全部由utf8编码的东西
    if isinstance(value, str):
        #code_format = chardet.detect(value)
        #utf8_str = value.decode(code_format["encoding"]).encode("utf8")
        return value
    if isinstance(value, unicode):
        utf8_str = value.encode('utf8')
        return utf8_str
    if isinstance(value, dict):
        utf8_dict = {}
        for key in value:
            utf8_key = replaceholder(key)
            utf8_dict[utf8_key] = replaceholder(value[key])
        return utf8_dict
    if isinstance(value, (list, tuple)):
        utf8_list = []
        for v in value:
            utf8_value = replaceholder(v)
            utf8_list.append(utf8_value)
        return utf8_list
    return value
