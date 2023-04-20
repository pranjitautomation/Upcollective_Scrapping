from scrapper import Scrapper


class Process:
    def __init__(self) -> None:
        self.scrapper_obj = Scrapper()

    def all_steps(self):

        self.scrapper_obj.open_browser()
        href_list = self.scrapper_obj.get_each_page_link()
        self.scrapper_obj.make_excel_file(href_list)
