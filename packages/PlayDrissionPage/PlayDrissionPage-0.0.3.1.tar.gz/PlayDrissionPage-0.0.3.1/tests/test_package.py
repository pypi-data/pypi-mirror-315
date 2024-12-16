from PlayDrissionPage import RemoteBrowserClient, ChromiumPagePlus

if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()

    rbc = RemoteBrowserClient()
    page = rbc.get_d_page()

    page.get('https://www.baidu.com')
    x = page.xhr_request('GET', 'https://www.baidu.com', {}, {})
