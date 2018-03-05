import json


from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


results = []


def parse(response):
#    global results
    for comment in response.css('div.comment-list-item'):
        name = comment.xpath('.//div[2]/div[1]/a/text()').re_first('(\S+)')
#        print(name)
        content = comment.xpath(".//div[contains(@class, 'comment-item-content')]/p/text()").re_first('(\S+)')
#        print(content)
        result = {"username":name, "content":content}
#        print(result)
        results.append(result)
#    print(results)


def has_next_page(response):
    res = response.xpath('//*[@id="comments"]/div/div[4]/ul/li[5]/@class').extract_first()
#    print(res)
    return 'disabled' not in res


def goto_next_page(driver):
    driver.find_element_by_xpath('//*[@id="comments"]/div/div[4]/ul/li[5]/a').click()


def wait_page_return(driver, page):
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, '//ul[@class="pagination"]/li[@class="active"]'),
            str(page)
        )
    )


def spider():

    driver = webdriver.PhantomJS()

    url = 'https://www.shiyanlou.com/courses/427'
    driver.get(url)
    page = 1
    while True:

        wait_page_return(driver, page)

        html = driver.page_source

        response = HtmlResponse(url=url, body=html.encode('utf8'))

        parse(response)

        if not has_next_page(response):
            break

        page += 1
        goto_next_page(driver)

    with open('/home/shiyanlou/comments.json', 'w') as f:
        f.write(json.dumps(results))


if __name__ == '__main__':
    spider()

