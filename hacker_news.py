from link_collector.link_collector import LinkCollector


class HackerNews(LinkCollector):
    def __init__(self, url, headless=True):
        super().__init__(url, headless)

    def get_links_the_page(self):
        xpath = '//td[@class="title"]/a[@class="storylink"]'
        elements = self.driver.find_elements_by_xpath(xpath)
        links = []
        for e in elements:
            links.append(e.get_attribute('href'))
            print(f'{e.text}\n{e.get_attribute("href")}\n')
        return links

    def get_next_page(self):
        try:
            xpath = '/html/body/center/table/tbody/tr/td/table/tbody/tr/td[@class="title"]/a[@class="morelink"]'
            element = self.driver.find_element_by_xpath(xpath)
            print(f'{element.text}({element.get_attribute("href")})\n')
            return element.get_attribute('href')
        except:
            return ''


if __name__ == '__main__':
    url = 'https://news.ycombinator.com/'
    obj = HackerNews(url, True)
    obj.dump()
