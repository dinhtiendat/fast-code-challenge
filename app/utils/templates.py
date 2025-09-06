from fastapi.templating import Jinja2Templates


def datetime_format(value, _format="%y-%m-%d %H:%M:%S"):
    return value.strftime(_format)


def int_format(value):
    return int(value)


def mapper_status(status):
    if status:
        return "Success"
    else:
        return "Fail"


templates = Jinja2Templates(directory="app/templates")
templates.env.filters['datetime_format'] = datetime_format
templates.env.filters['int_format'] = int_format
templates.env.filters['mapper_status'] = mapper_status
