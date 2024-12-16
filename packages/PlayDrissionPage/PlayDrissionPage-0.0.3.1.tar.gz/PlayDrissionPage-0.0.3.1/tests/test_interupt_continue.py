from dotenv import load_dotenv
load_dotenv()
if __name__ == '__main__':
    from PlayDrissionPage.client.remote_browser_client import RemoteBrowserClient

    rbc = RemoteBrowserClient()
    page = rbc.get_d_page(user_id='Default')
    page.get('https://www.baidu.com/s?wd=')

    modify_running = False

    @page.over.request('https://www.baidu.com/s?wd=*')
    def modify(**kwargs):
        requestId = kwargs['requestId']
        request = kwargs['request']
        url = request['url']
        if 'https://www.baidu.com/s?wd=' in url:
            request['url'] = url.replace('https://www.baidu.com/s?wd=', 'https://www.baidu.com/s?wd=hello')
        modify_running = True
        page.over.continue_request(requestId=requestId, **request)


    @page.over.request('*.png')
    def fail(**kwargs):
        requestId = kwargs['requestId']
        page.over.fail_request(requestId=requestId)


    page.get('https://www.baidu.com/s?wd=%E4%BD%A0%E5%A5%BD')
    while not modify_running:
        page.wait(1)
    page.over.disable_request('*.png')
    page.get('https://www.baidu.com/s?wd=%E4%BD%A0%E5%A5%BD')

    print(page.title)
