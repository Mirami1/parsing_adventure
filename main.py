from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json


def work(url: str):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    driver.implicitly_wait(10)  # ожидание по возможному безействию

    driver.find_element_by_xpath(
        "//a[@class='header-mobile-toggle inline-block-item vertical-middle hide-for-xlarge']").click()

    driver.find_element_by_link_text('Брошь-подвес').click()

    driver.find_element_by_xpath(
        "//a[@class='button filter-mobile-toggle']").click()

    names = ['Цвет камня', 'Камень', 'Металл']  # названия фильтров
    data = {}  # результат выборки

    for name in names:

        data[name] = {}
        elem = driver.find_element_by_xpath(
            '//span[text()="{0}"]'.format(name)).find_element_by_xpath('./../..')  # находим название категории фильтра

        elem.click()
        time.sleep(2)
        checkbox = elem.find_element_by_class_name('checkbox')  # контейнер фильтра
        container_1 = checkbox.find_elements_by_tag_name("label")  # его элементы

        # прожимаем и отжимаем каждый элемент фильтра и заносим адрес страницы во множество
        for elem_1 in container_1:
            time.sleep(1)
            ActionChains(driver).move_to_element(elem_1).click(elem_1).perform()
            time.sleep(2)
            filter_button = driver.find_element_by_xpath(
                "//a[@class='button filter-mobile-toggle']")
            filter_button.send_keys(Keys.CONTROL + Keys.HOME)
            time.sleep(1)
            filter_button = driver.find_element_by_xpath(
                "//a[@class='button filter-mobile-toggle']")
            filter_button.click()
            elem_1_text = elem_1.get_attribute("innerHTML").strip()

            if not elem_1_text in data[name].keys():
                data[name][elem_1_text] = []
            data[name][elem_1_text].append(driver.current_url)

            print(driver.current_url)
            ActionChains(driver).move_to_element(elem_1).click(elem_1).perform()
            time.sleep(2)
            filter_button = driver.find_element_by_xpath(
                "//a[@class='button filter-mobile-toggle']")
            filter_button.send_keys(Keys.CONTROL + Keys.HOME)
            filter_button = driver.find_element_by_xpath(
                "//a[@class='button filter-mobile-toggle']")
            time.sleep(1)
            filter_button.click()

        time.sleep(2)
        unclick_button = driver.find_element_by_xpath(
            '//span[text()="{0}"]'.format(name))
        unclick_button.click()
        time.sleep(2)
    print(data)

    with open('result.json', 'w', encoding="windows-1251") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)
    driver.quit()


if __name__ == '__main__':
    work("https://dinosa.ru/")
