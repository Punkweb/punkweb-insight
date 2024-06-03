from django import template

register = template.Library()


@register.filter
def duration(value):
    value = int(value)
    hours = value // 3600
    minutes = (value % 3600) // 60
    seconds = value % 60

    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"
