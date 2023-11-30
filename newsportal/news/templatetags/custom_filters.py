from django import template

register = template.Library()

BAD_WORDS = [
    'блин', 'ёлки-палки', 'ёмоё', 'троль'
]


@register.filter()
def censor(text):
    for bad in BAD_WORDS:
        if bad in text.lower():
            text = text.replace(bad, bad[0] + (len(bad) - 1) * '*')
    return text
