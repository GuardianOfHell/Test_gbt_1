from django import template
import re

register = template.Library()

@register.filter(name='parse_characteristics')
def parse_characteristics(value):
    """
    Цей фільтр приймає текстовий блок з характеристиками,
    розбиває його на рядки та пари "назва | значення".
    """
    characteristics = []
    # Розбиваємо текст на рядки, ігноруючи порожні
    lines = [line.strip() for line in value.strip().split('\n') if line.strip()]

    for line in lines:
        # Розділяємо рядок по символу "|"
        parts = line.split('|')
        if len(parts) == 2:
            # Додаємо словник з назвою та значенням до списку
            characteristics.append({
                'title': parts[0].strip(),
                'value': parts[1].strip()
            })
    return characteristics
