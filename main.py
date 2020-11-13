from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from json2xml import json2xml
import time


def work(url: str):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    driver.implicitly_wait(10)  # ожидание по возможному безействию

    driver.find_element_by_xpath(
        "//a[@class='header-mobile-toggle inline-block-item vertical-middle hide-for-xlarge']").click()
    cats = driver.find_element_by_xpath("//ul[@class='vertical menu mobile-menu-main']").find_elements_by_tag_name('li')
    categories = [i.text for i in cats]

    driver.find_element_by_link_text(categories[0]).click()
    driver.find_element_by_xpath(
        "//a[@class='button filter-mobile-toggle']").click()
    filters = driver.find_elements_by_xpath("//div[contains(@style,'z-index')]")
    filters.pop(0)
    filters.pop(len(filters) - 1)

    names = [i.text for i in filters]  # названия фильтров
    driver.find_element_by_xpath(
        "//div[@class='header-logo--mobile-fixed']").click()

    time.sleep(2)
    data = {}  # результат выборки
    for category in categories:
        data[category] = {}

        driver.find_element_by_xpath(
            "//a[@class='header-mobile-toggle inline-block-item vertical-middle hide-for-xlarge']").click()
        time.sleep(2)

        driver.find_element_by_link_text(category).click()

        driver.find_element_by_xpath(
            "//a[@class='button filter-mobile-toggle']").click()

        for name in names:

            data[category][name] = {}
            elem = driver.find_element_by_xpath(
                '//span[text()="{0}"]'.format(name)).find_element_by_xpath(
                './../..')  # находим название категории фильтра
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="{0}"]'.format(name))))
            elem.click()
            time.sleep(2)
            checkbox = elem.find_element_by_class_name('checkbox')  # контейнер фильтра
            container_1 = checkbox.find_elements_by_tag_name("label")  # его элементы

            # прожимаем и отжимаем каждый элемент фильтра и заносим адрес страницы во множество
            for elem_1 in container_1:
                time.sleep(3)
                ActionChains(driver).move_to_element(elem_1).click(elem_1).perform()
                time.sleep(2)
                filter_button = driver.find_element_by_xpath(
                    "//a[@class='button filter-mobile-toggle']")
                filter_button.send_keys(Keys.CONTROL + Keys.HOME)
                time.sleep(2)

                WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@class='button filter-mobile-toggle']")))
                time.sleep(2)
                filter_button = driver.find_element_by_xpath(
                    "//a[@class='button filter-mobile-toggle']").click()
                elem_1_text = elem_1.get_attribute("innerHTML").strip()

                if not elem_1_text in data[category][name].keys():
                    data[category][name][elem_1_text] = set()
                data[category][name][elem_1_text].add(driver.current_url)

                print(driver.current_url)
                ActionChains(driver).move_to_element(elem_1).click(elem_1).perform()
                time.sleep(3)
                filter_button = driver.find_element_by_xpath(
                    "//a[@class='button filter-mobile-toggle']")
                time.sleep(3)
                filter_button = driver.find_element_by_xpath(
                    "//a[@class='button filter-mobile-toggle']")
                filter_button.send_keys(Keys.CONTROL + Keys.HOME)
                time.sleep(1)
                filter_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@class='button filter-mobile-toggle']")))
                time.sleep(4)
                filter_button = driver.find_element_by_xpath(
                    "//a[@class='button filter-mobile-toggle']").click()

            time.sleep(2)
            unclick_button = driver.find_element_by_xpath(
                '//span[text()="{0}"]'.format(name))
            unclick_button.click()
            time.sleep(2)

    data_for_xml = []

    # запись данных в xml формат
    for value in data.values():
        for value_1 in value.values():
            for value_2 in value_1.values():
                lst = list(value_2)
                for url in lst:
                    data_for_xml.append({'url': {'loc': url}})

    xml_data = json2xml.Json2xml(data_for_xml, wrapper='urlset', pretty=True, attr_type=False).to_xml()
    print(data_for_xml)
    xml_str = xml_data.__str__().replace('<item>', "").replace('</item>', "")
    print(xml_str)
    with open('result.xml', 'w', encoding="utf-8") as fp:
        fp.write(xml_str)
    driver.quit()


if __name__ == '__main__':
    work("https://dinosa.ru/")
