from PlayDrissionPage import RemoteBrowserClient, ChromiumPagePlus


def old_test(page: ChromiumPagePlus):
    page.get(
        'https://item.taobao.com/item.htm?abbucket=6&id=742409731796&ns=1&pisk=f5DKL0bxAFY3l4sO6_OgZs7DlixMSYne-2ofEz4hNV3tVPXkYJAze4UtzyV3dyX8e03rr4nyYuaSP4UotCvmYDyzFE4JnKmF5Em6G2EQN1t7moEBpdAMADyzFUIGFIvxYqNsKlqQVltTquq5F4NQClZ75k17N4a_1oZcR8g7Fhe_VkC5F6a75PZY5w67Nzi6CoZzAw1QVhn_7uGVPUU1AzX-ap56X1fp5TWrBlTzoD3QblDTcWab1PB7jAEL9riKLI2NTlMiBSVGqF2s0f0QX-pdukhsDJZ-Un18y7HUBP3vhTrZO2H_wAxyHc2L2Sw76g6SX8GEuAeXhNEZ1DcSL2IRFkknn7U4636zZRM0Gjgd4no_dugzgYYVLyiS0xl0HpQ4vfiYBgkonxK6rZqaB6t9X_5zOl-MAxV0dz_W1lUDvLCPa5-aXrx9X_5zOlrToHpRa_Pae&priceTId=2150459817299137907746081e9f56&skuId=5117480904611&spm=a21n57.1.item.2.29cc523cMCmEd1&utparam=%7B%22aplus_abtest%22%3A%22682684831cac63037137e75692f2a34f%22%7D&xxc=taobaoSearch')

    debug_info = page.run_cdp(
        "Debugger.enable",
    )
    z = page.run_cdp(
        "Debugger.disable",
    )

    set_break_info = page.run_cdp(
        "Debugger.setBreakpointByUrl",
        lineNumber=0,
        columnNumber=1980678,
        # columnNumber=0,
        # columnNumber=1,
        urlRegex=r'https://g.alicdn.com/tbpc/pc-detail-2024/0.0.34/js/main.js',
    )

    script_id_list = [x['scriptId'] for x in set_break_info['locations']]
    location_list = set_break_info['locations']

    page.run_cdp(
        "Debugger.setBreakpointsActive",
        active=True,
    )
    page.run_cdp(
        "Debugger.getPossibleBreakpoints",
        start=location_list[1]
    )
    page.run_cdp(
        "Debugger.getPossibleBreakpoints",
    )
    page.run_cdp(
        "Debugger.pause",
    )
    page.run_cdp(
        "Debugger.resume",
    )

    args_list = []
    kwargs_list = []

    def on_paused(*args, **kwargs):
        args_list.append(args)
        kwargs_list.append(kwargs)
        print(args, kwargs)
        js = """
        eu
        """
        call_frame_id = kwargs_list[-1]['callFrames'][0]['callFrameId']

        item_info = page.run_cdp(
            "Debugger.evaluateOnCallFrame",
            callFrameId=call_frame_id,
            expression=js,
            returnByValue=True,
        )
        set_new_value_js = """
        eu.itemId = '666217341645'
        eu.pageNum = 2
        eu.orderType = 'feedbackdate'
        """
        rt = page.run_cdp(
            "Debugger.evaluateOnCallFrame",
            callFrameId=call_frame_id,
            expression=set_new_value_js,
            returnByValue=True,
        )

    page.run_js(
        """
        return 1+1
        """
    )

    page.driver.set_callback('Debugger.paused', on_paused)
    page.driver.set_callback('Debugger.paused', None)

    page.run_cdp(
        "Debugger.CallFrame",
    )

    for s_id in script_id_list:
        z = page.run_cdp(
            "Debugger.getScriptSource",
            scriptId=s_id,
        )
        src = z['scriptSource']
        if 'a.encryptSignV2' in src:
            print(s_id)
            print(src)

    js = """
    (0,
        a.encryptSignV2)({
            appKey: s.appKey,
            data: p,
            t: s.t,
            os: s.os,
            osv: s.osv,
            model: s.model,
            token: t
        })
    """
    page.run_cdp(
        "Debugger.evaluateOnCallFrame",
        callFrameId='495856556828576189.31.0',
        expression=js,
    )

    z = page.run_js(js)

    page.goto('https://www.baidu.com')
    rbc.release_page(page)
    page = rbc.get_page(page_type='p')
    page.goto('https://www.baidu.com')
    rbc.to_drission_page(page)
    r = page.xhr_request('GET', 'https://www.baidu.com', {}, {})

    page = rbc.to_playwright_page(page)
    page.goto('https://www.baidu.com')
    print(rbc.get_page())


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    rbc = RemoteBrowserClient()
    page = rbc.get_d_page()
    page.get(
        'https://item.taobao.com/item.htm?abbucket=6&id=742409731796&ns=1&pisk=f5DKL0bxAFY3l4sO6_OgZs7DlixMSYne-2ofEz4hNV3tVPXkYJAze4UtzyV3dyX8e03rr4nyYuaSP4UotCvmYDyzFE4JnKmF5Em6G2EQN1t7moEBpdAMADyzFUIGFIvxYqNsKlqQVltTquq5F4NQClZ75k17N4a_1oZcR8g7Fhe_VkC5F6a75PZY5w67Nzi6CoZzAw1QVhn_7uGVPUU1AzX-ap56X1fp5TWrBlTzoD3QblDTcWab1PB7jAEL9riKLI2NTlMiBSVGqF2s0f0QX-pdukhsDJZ-Un18y7HUBP3vhTrZO2H_wAxyHc2L2Sw76g6SX8GEuAeXhNEZ1DcSL2IRFkknn7U4636zZRM0Gjgd4no_dugzgYYVLyiS0xl0HpQ4vfiYBgkonxK6rZqaB6t9X_5zOl-MAxV0dz_W1lUDvLCPa5-aXrx9X_5zOlrToHpRa_Pae&priceTId=2150459817299137907746081e9f56&skuId=5117480904611&spm=a21n57.1.item.2.29cc523cMCmEd1&utparam=%7B%22aplus_abtest%22%3A%22682684831cac63037137e75692f2a34f%22%7D&xxc=taobaoSearch')

    kwargs_list = []
    breakpoint_id_list = []
    comments_breakpoint = {
        "line_number": 0,
        "column_number": 1980678,
        "url_regex": r'https://g.alicdn.com/tbpc/pc-detail-2024/0.0.34/js/main.js',
    }

    @page.debug.set_breakpoint_by_url(**comments_breakpoint)
    def on_paused(*args, **kwargs):
        call_frame_id = kwargs['callFrames'][0]['callFrameId']
        set_new_value_js = 'eu'
        rt = page.debug.evaluate_on_call_frame(
            call_frame_id=call_frame_id,
            expression=set_new_value_js,
        )
        print(rt)
        kwargs_list.append(kwargs)

        set_new_value_js = """
        eu.itemId = '666217341645'
        eu.pageNum = 2
        eu.orderType = 'feedbackdate'
        """
        rt = page.debug.evaluate_on_call_frame(
            call_frame_id=call_frame_id,
            expression=set_new_value_js,
        )
        print(rt)
        page.debug.resume()


    @page.debug.set_breakpoint_by_url(**comments_breakpoint)
    def on_paused(*args, **kwargs):
        print(kwargs)

    page.debug.wait(count=5, **comments_breakpoint)

    x = page.debug.remove_breakpoint(**comments_breakpoint)
    print()
