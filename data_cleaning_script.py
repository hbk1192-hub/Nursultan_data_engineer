import pandas as pd
import re

# 1. Создаем "грязные" данные для демонстрации (имитация выгрузки из CRM)
data = {
    'client_name': [' иван петров ', 'Мария С.', '  ольга  ', 'Иван Петров', 'Сергей'],
    'phone': ['89001112233', '+7 (900) 111-22-33', '9001112233', '8-900-111-22-33', 'unknown'],
    'last_visit': ['2023-01-15', '15.01.2023', '2023/01/15', '2023-01-15', None],
    'total_spent': ['1500,50', '2100', ' 1800 ', '1500.50', '0']
}

df = pd.DataFrame(data)

def clean_data(df):
    # Копия для работы
    df_clean = df.copy()

    # Очистка имен: убираем пробелы и делаем заглавные буквы
    df_clean['client_name'] = df_clean['client_name'].str.strip().str.title()

    # Очистка телефонов: оставляем только цифры и приводим к формату 7900...
    def fix_phone(phone):
        digits = re.sub(r'\D', '', str(phone))
        if len(digits) == 11 and digits.startswith(('7', '8')):
            return '7' + digits[1:]
        elif len(digits) == 10:
            return '7' + digits
        return None

    df_clean['phone'] = df_clean['phone'].apply(fix_phone)

    # Работа с датами: приводим разные форматы к единому YYYY-MM-DD
    df_clean['last_visit'] = pd.to_datetime(df_clean['last_visit'], errors='coerce')

    # Очистка сумм: заменяем запятые на точки и переводим в числовой формат (float)
    df_clean['total_spent'] = df_clean['total_spent'].str.replace(',', '.').astype(float)

    # Удаляем дубликаты (например, Иван Петров встретился дважды)
    df_clean = df_clean.drop_duplicates(subset=['client_name', 'phone'])

    return df_clean

# Запуск очистки
final_df = clean_data(df)

# Вывод результата
print("--- Очищенные данные ---")
print(final_df)

# Сохранение (имитация)
# final_df.to_csv('cleaned_clients.csv', index=False)
