import configparser as ConfigParser
import function
import os


class ConfigProvider:
    config_file_name = 'config.ini'
    root = os.path.abspath(os.path.dirname(__file__))
    path_to_markdown = 'articles'
    path_to_html = 'static'
    templates_dir = os.path.join(root, 'templates')
    static_dir = os.path.join(root, 'static')
    main_page = os.path.join(root, 'index.html')
    ext_html = '.html'
    articles_file = 'config.json'
    name_site = 'Энциклопедия'
    count_col_on_main_page = 3

    def __init__(self):
        if function.check_file_to_read(self.config_file_name):
            config = ConfigParser.RawConfigParser()
            config.read(self.config_file_name, encoding='utf-8')
            self.path_to_markdown = config.get('app_setting',
                                               'path_to_markdown')
            self.path_to_html = config.get('app_setting', 'path_to_html')
            self.templates_dir \
                = os.path.join(self.root,
                               config.get('app_setting', 'templates_dir'))
            self.static_dir \
                = os.path.join(self.root,
                               config.get('app_setting', 'static_dir'))
            self.main_page \
                = os.path.join(self.root,
                               config.get('app_setting', 'main_page'))
            self.ext_html = config.get('app_setting', 'ext_html')
            self.articles_file = config.get('app_setting', 'articles_file')
            self.name_site = config.get('app_setting', 'name_site')
            self.count_col_on_main_page \
                = config.getint('app_setting', 'count_col_on_main_page')
