import json


def json_load_file(file_name,code = 'utf-8'):
    f = open(file_name, 'r',encoding=code)
    return json.load(f)


def json_load_str(s: str):
    return json.loads(s)


def json_write_file(filename, data):
    f = open(filename, 'w')
    json.dump(data, f, ensure_ascii=False)


def json_to_str(data: str):   # 将python对象转化为字符串，与loads相反
    return json.dumps(data)