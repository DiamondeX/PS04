import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def search_wikipedia(query):
    # Убедитесь, что у вас установлен geckodriver в PATH или укажите путь к нему
    driver = webdriver.Firefox()
    driver.get("https://ru.wikipedia.org/wiki/Основная_страница")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "searchInput"))
    )
    search_box.send_keys(query)
    search_box.send_keys(Keys.ENTER)
    link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, query))
    )
    link.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "p"))
    )

    return driver


def scroll_paragraphs(driver):
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    for i, paragraph in enumerate(paragraphs, 1):
        if paragraph.text.strip() == "": # Пропускаем пустые параграфы
            continue
        print(f"Параграф {i}:\n {paragraph.text[:200]}...\n")  # Показываем первые 200 символов
        if input("Нажмите Enter для следующего параграфа или 'q' для выхода: ").lower() == 'q':
            break


def navigate_links(driver):
    # links = driver.find_elements(By.CSS_SELECTOR, "div.hatnote.navigation-not-searchable a")
    # for element in :
    #     # Чтобы искать атрибут класса
    #     css_class = element.get.attribute("class")
    #     if css_class == "hatnote navigation-not-searchable":
    #         hatnotes.append(element)
    #
    # # print(hatnotes)
    # hatnote = random.choice(hatnotes)
    #
    # # Для получения ссылки мы должны найти на сайте тег "a" внутри тега "div"
    # link = hatnote.find_element(By.TAG_NAME, "a").get.attribute("href")
    # browser.get(link)

    links = driver.find_elements(By.CSS_SELECTOR, "div.hatnote.navigation-not-searchable.ts-main a")
    for i, link in enumerate(links[:9], 1):  # Ограничиваем до 9 ссылок для примера
        print(f"{i}. {link.text}")

    choice = input("Выберите номер ссылки или 'q' для выхода: ")
    if choice.lower() != 'q':
        link = links[int(choice) - 1]
        driver.get(link.get_attribute('href'))
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "p"))
        )
        print("Статья открылась!")


def main():
    query = input("Введите запрос для поиска в Википедии: ")
    driver = search_wikipedia(query)

    while True:
        print("\n1. Листать параграфы текущей статьи")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")

        choice = input("Выберите действие: ")
        if choice == '1':
            scroll_paragraphs(driver)
        elif choice == '2':
            navigate_links(driver)
        elif choice == '3':
            driver.quit()
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()