import pandas as pd


def read_wb_report(file_path):
    # Читаем CSV.
    # В твоем файле разделитель - запятая, а кодировка обычно utf-8
    try:
        df = pd.read_excel("data.xlsx")  # Вместо read_csv

        # Нам нужен столбец "Артикул WB" (это колонка F в Excel)
        if 'Артикул WB' in df.columns:
            articles = df['Артикул WB'].tolist()
            # Убираем возможные пустые значения (NaN)
            articles = [str(int(a)) for a in articles if pd.notnull(a)]
            return articles
        else:
            return "Колонка 'Артикул WB' не найдена!"

    except Exception as e:
        return f"Ошибка при чтении: {e}"


# ТЕСТ: Скопируй название своего файла сюда
file_name = "Товары для исключения из акции_Сезон скидок - 2 (автоматические скидки)_11.02.2026 17.20.28.xlsx - Отчёт по скидкам.csv"
print(read_wb_report(file_name))