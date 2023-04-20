from RPA.Browser.Selenium import Selenium
import pandas as pd
import os


class Scrapper:
    def __init__(self) -> None:
        self.browser = Selenium()

    def make_dir():
        """Make output dir if not created already.
        """
        if not os.path.exists('./output'):
            os.makedirs('./output')

    def open_browser(self):
        """Open browser.
        """
        self.browser.open_available_browser('https://www.upcollective.io/company/task-managers')
        self.browser.wait_until_element_is_visible('//div[@class="collection-list filter-complex w-dyn-items"]', 10)

    def get_each_page_link(self):
        """Get each service page link.
        """
        count = self.browser.get_element_count('xpath://div[@class="collection-list-item w-dyn-item"]')
        href_list = []

        for i in range(1, count+1):
            href = self.browser.get_element_attribute(f'xpath:(//a[@class="collection-list-content rounded-xs zoom-in w-inline-block"])[{i}]', 'href')
            href_list.append(href)

        return href_list
    
    def get_data_from_each_page(self, href_list):
        """Scrap all necessary data from each service page.
        """
        vertical_list = []
        task_list = []
        title_list = []
        description_list = []
        flow_list = []

        for href_link in href_list:
            self.browser.go_to(href_link)

            self.browser.wait_until_element_is_visible('//strong[text()="Vertical"]//../following-sibling::div', 20)
            vertical = self.browser.get_text('//strong[text()="Vertical"]//../following-sibling::div')
            vertical_list.append(vertical)

            task = self.browser.get_text('//strong[text()="Task"]//../following-sibling::div')
            task_list.append(task)

            title = self.browser.get_text('//h1[@class="title-sm-2"]')
            title_list.append(title)

            description = self.browser.get_text('//div[@class="text-xl"]')
            description_list.append(description)

            li_count = self.browser.get_element_count('//*[text()="Process Flow"]/following-sibling::ol/li')
            if li_count==0:
                print(href_link)

            flow_points= ''
            for li in range(1, (li_count//2) +1):
                li_text = self.browser.get_text(f'(//*[text()="Process Flow"]/following-sibling::ol/li)[{li}]')
                flow_points = flow_points + f'{li}) '+ li_text + '\n'
            flow_list.append(flow_points)

        return title_list, vertical_list, task_list, description_list, flow_list
    
    def make_excel_file(self, href_list):
        """Create excel file populated with all necessary data like Title, Vertical, Task, Description, Process Flow
        """
        title_list, vertical_list, task_list, description_list, flow_list = self.get_data_from_each_page(href_list)
        print(len(title_list), len(vertical_list), len(task_list), len(description_list), len(flow_list))

        data = {
            'Title' : title_list,
            'Vertical' : vertical_list,
            'Task' : task_list,
            'Description' : description_list,
            'Process Flow' : flow_list
        }

        df = pd.DataFrame(data)  
        df.to_excel('./output/upcollective_scrapping.xlsx', index=False)
