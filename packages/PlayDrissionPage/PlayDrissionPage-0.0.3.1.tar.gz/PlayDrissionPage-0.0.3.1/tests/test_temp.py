from PlayDrissionPage import RemoteBrowserClient, ChromiumPagePlus

if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()

    import subprocess
    z = subprocess.run(
        'powershell.exe -Command "Get-NetTCPConnection -LocalPort 22200"'
    )

    rbc = RemoteBrowserClient()
    page = rbc.get_d_page()
    page1 = rbc.get_d_page()
    page2 = rbc.get_d_page()
    rbc2 = RemoteBrowserClient()
    page3 = rbc2.get_d_page()
    page_ = page.browser.new_tab()
    page_2 = page.browser.new_tab()
    page_4 = page.browser.new_tab()
    rt = page.run_cdp(
        "ServiceWorker.enable"
    )
    rt = page.browser.run_cdp(
        "SystemInfo.getInfo"
    )
    import requests
    z = requests.get('http://127.0.0.1:22211/json/protocol').json()
    for _z in z['domains']:
        for cmd in _z.get('commands', []):
            print(cmd.get('description', None))


    page.browser._driver._websocket_url
