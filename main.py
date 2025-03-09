from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Инициализация веб-драйвера
driver = webdriver.Chrome()  # Убедитесь, что chromedriver находится в PATH
driver.get("https://wikipedia.org")


def search_wikipedia(query):
    """Функция для поиска статьи на Википедии."""
    search_box = driver.find_element(By.ID, "searchInput")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Ждем загрузки страницы


def list_paragraphs():
    """Функция для вывода параграфов текущей статьи."""
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    for i, paragraph in enumerate(paragraphs):
        print(f"Параграф {i + 1}: {paragraph.text[:100]}...")  # Выводим первые 100 символов


def get_linked_pages():
    """Функция для получения связанных страниц."""
    links = driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output a")
    linked_pages = []
    for link in links:
        href = link.get_attribute("href")
        if href and "wiki" in href and "#" not in href:
            linked_pages.append((link.text, href))
    return linked_pages[:5]  # Возвращаем первые 5 ссылок


def main():
    try:
        while True:
            query = input("Введите запрос для поиска на Википедии (или 'exit' для выхода): ")
            if query.lower() == "exit":
                break

            search_wikipedia(query)

            while True:
                print("\nВыберите действие:")
                print("1. Листать параграфы текущей статьи")
                print("2. Перейти на одну из связанных страниц")
                print("3. Вернуться к поиску")
                choice = input("Введите номер действия: ")

                if choice == "1":
                    list_paragraphs()
                elif choice == "2":
                    linked_pages = get_linked_pages()
                    print("\nСвязанные страницы:")
                    for i, (title, _) in enumerate(linked_pages):
                        print(f"{i + 1}. {title}")

                    page_choice = input("Введите номер страницы для перехода: ")
                    if page_choice.isdigit() and 1 <= int(page_choice) <= len(linked_pages):
                        selected_page = linked_pages[int(page_choice) - 1][1]
                        driver.get(selected_page)
                        time.sleep(2)
                    else:
                        print("Неверный выбор. Попробуйте снова.")
                elif choice == "3":
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()