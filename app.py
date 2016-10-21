import os
import sys
import shutil
from jinja2 import Environment, FileSystemLoader
import function
from config_provider import ConfigProvider


CONFIG = ConfigProvider()


def get_arcticles_md(filepath):
    if not function.check_file_to_read(filepath):
        return None
    return function.read_json_file(filepath)


def generate_path_to_html(file_md):
    root = os.path.splitext(file_md)[0]
    return os.path.join(CONFIG.path_to_html, root) + CONFIG.ext_html


def convert_article(article, topic, file_md, file_html, link_to_main):
    article_html = function.markdown_to_html(file_md)
    env = Environment(loader=FileSystemLoader(CONFIG.templates_dir))
    template = env.get_template('article.html')
    data = {'title': '%s | %s' % (article['title'], CONFIG.name_site),
            'page_title': CONFIG.name_site,
            'article_title': article['title'],
            'topic': topic,
            'article_text': article_html,
            'static_dir': os.path.relpath(CONFIG.static_dir,
                                          os.path.dirname(file_html)),
            'link_to_main': os.path.relpath(link_to_main,
                                            os.path.dirname(file_html))}
    html_page = template.render(data)
    function.save_html_to_file(html_page, file_html)


def create_main_html(file_html, list_articles):
    env = Environment(loader=FileSystemLoader(CONFIG.templates_dir))
    template = env.get_template('list_article.html')
    data = {'title': CONFIG.name_site,
            'page_title': CONFIG.name_site,
            'list_articles': list_articles,
            'static_dir': os.path.relpath(CONFIG.static_dir,
                                          os.path.dirname(file_html)),
            'count_col': CONFIG.count_col_on_main_page}
    html_page = template.render(data)
    function.save_html_to_file(html_page, file_html)


def delete_old_site_page():
    if function.check_dir_to_write(os.path.join(CONFIG.path_to_html,
                                                CONFIG.path_to_markdown)):
        shutil.rmtree(os.path.join(CONFIG.path_to_html,
                                   CONFIG.path_to_markdown))
    if os.path.exists(CONFIG.main_page):
        os.remove(CONFIG.main_page)


if __name__ == '__main__':
    if not function.check_dir_to_write(CONFIG.root):
        print('Denied access to  "%s"!' % CONFIG.root)
        sys.exit(1)
    if not function.check_file_to_read(CONFIG.articles_file):
        print('File "%s" not found!' % CONFIG.articles_file)
        sys.exit(1)
    delete_old_site_page()
    articles_md = get_arcticles_md(CONFIG.articles_file)
    for article in articles_md['articles']:
        file_md = os.path.join(CONFIG.path_to_markdown, article['source'])
        if not function.check_file_to_read(file_md):
            print('File "%s" not found!' % file_md)
            continue
        file_html = generate_path_to_html(file_md)
        found_topic = list(filter(lambda x: x['slug'] == article['topic'],
                                  articles_md['topics']))
        topic_title = None
        if found_topic:
            topic_title = found_topic[0]['title']
        convert_article(article, topic_title, file_md, file_html,
                        CONFIG.main_page)
        article['html_file'] = file_html
    create_main_html(CONFIG.main_page, articles_md)
