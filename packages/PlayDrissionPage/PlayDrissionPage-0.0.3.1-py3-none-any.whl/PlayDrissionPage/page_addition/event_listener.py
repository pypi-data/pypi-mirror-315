import base64
import fnmatch
import logging
from collections.abc import Callable

from DrissionPage import ChromiumPage

logger = logging.getLogger('main')


class BaseEventListener(object):
    pass


class RequestEventListener(BaseEventListener):

    def __init__(self, page: ChromiumPage):
        super().__init__()
        self.page = page
        self._request_patterns = []
        self._request_fun_dict = {}
        # todo: 加入wait 逻辑
        self._request_wait_dict = {}

    def event(self, **kwargs):
        pass

    def request(self, url):
        """
        Wildcards ('*' -> zero or more, '?' -> exactly one) are allowed. Escape character is backslash. Omitting is equivalent to "*".
        :param url:
        :return:
        :example:
        @page.over.request('https://www.baidu.com/s?wd=*')
        def modify(**kwargs):
            requestId = kwargs['requestId']
            request = kwargs['request']
            url = request['url']
            if 'https://www.baidu.com/s?wd=' in url:
                request['url'] = url.replace('https://www.baidu.com/s?wd=', 'https://www.baidu.com/s?wd=hello')

            page.over.continue_request(requestId=requestId, **request)
        """
        self._request_patterns.append({'urlPattern': url, 'requestStage': 'Request'})
        self.page.run_cdp('Fetch.enable', patterns=self._request_patterns)

        def wrapper(func):
            if not self._request_fun_dict:
                self.page._driver.set_callback('Fetch.requestPaused', self._request_event_fun)
            self._request_fun_dict[url] = func
            return func

        return wrapper

    def _request_event_fun(self, **kwargs):
        real_url = kwargs['request']['url']
        for url_pattern, func in self._request_fun_dict.items():
            if fnmatch.fnmatch(real_url, url_pattern):
                func(**kwargs)
                break

    def continue_request(self, **kwargs):
        """
        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#method-continueRequest
        RequestId
        An id the client received in requestPaused event.
        url
        string
        If set, the request url will be modified in a way that's not observable by page.
        method
        string
        If set, the request method is overridden.
        postData
        string
        If set, overrides the post data in the request. (Encoded as a base64 string when passed over JSON)
        headers
        array[ HeaderEntry ]
        If set, overrides the request headers. Note that the overrides do not extend to subsequent redirect hops, if a redirect happens. Another override may be applied to a different request produced by a redirect.
        interceptResponse
        boolean
        If set, overrides response interception behavior for this request. Experimental
        :param kwargs:
        :return:
        """
        _kwargs = {}
        if 'requestId' in kwargs:
            _kwargs['requestId'] = kwargs['requestId']
        if 'url' in kwargs:
            _kwargs['url'] = kwargs['url']
        if 'method' in kwargs:
            _kwargs['method'] = kwargs['method']
        if 'postData' in kwargs:
            post_data = kwargs['postData']
            _kwargs['postData'] = base64.b64encode(post_data.encode()).decode()
        if 'headers' in kwargs:
            headers = kwargs['headers']
            _kwargs['headers'] = [{"name": key, "value": value} for key, value in headers.items()]
        if 'interceptResponse' in kwargs:
            _kwargs['interceptResponse'] = kwargs['interceptResponse']

        self.page.run_cdp('Fetch.continueRequest', **_kwargs)

    def fail_request(self, requestId, errorReason='ConnectionClosed'):
        """
        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#method-failRequest
        RequestId
        An id the client received in requestPaused event.
        errorReason
        string
        Causes the request to fail with the given reason.
        Network level fetch failure reason.
        Allowed Values: Failed, Aborted, TimedOut, AccessDenied, ConnectionClosed, ConnectionReset, ConnectionRefused, ConnectionAborted, ConnectionFailed, NameNotResolved, InternetDisconnected, AddressUnreachable, BlockedByClient, BlockedByResponse
        :param kwargs:
        :return:
        """
        _kwargs = {'requestId': requestId, 'errorReason': errorReason}
        self.page.run_cdp('Fetch.failRequest', **_kwargs)

    def disable_request(self, url: [Callable, str, None] = None):
        if isinstance(url, Callable):
            self._request_patterns = [x for x in self._request_patterns if url(x['urlPattern'])]
        elif isinstance(url, str):
            self._request_patterns = [x for x in self._request_patterns if x['urlPattern'] != url]
        elif url is None:
            self._request_patterns = []
        else:
            raise TypeError
        if not self._request_patterns or not url:
            self.page.run_cdp('Fetch.disable')
        else:
            self.page.run_cdp('Fetch.enable', patterns=self._request_patterns)
        return True

    def response(self, **kwargs):
        pass


class DebugEventListener(BaseEventListener):

    def __init__(self, page: ChromiumPage):
        super().__init__()
        self.page = page
        self._debug_info = {}
        self._debug_patterns_dict = {}
        self._debug_fun_dict = {}

    def set_breakpoint_by_url(self, line_number,
                              url=None,
                              url_regex=None,
                              script_hash=None,
                              column_number=None,
                              condition=None
                              ):
        """
        https://chromedevtools.github.io/devtools-protocol/tot/Debugger/#method-setBreakpointByUrl
        def on_paused(*args, **kwargs):
            call_frame_id = kwargs['callFrames'][0]['callFrameId']
            set_new_value_js = 'eu'
            rt = page.debug.evaluate_on_call_frame(
                call_frame_id=call_frame_id,
                expression=set_new_value_js,
            )
            page.debug.resume()
        """
        if not self._debug_info:
            self._debug_info = self.page.run_cdp('Debugger.enable')

        if not self._debug_fun_dict:
            self.page._driver.set_callback('Debugger.paused', self._debug_event_fun)

        set_breakpoint_rq = dict()
        set_breakpoint_rq['lineNumber'] = line_number
        if url:
            set_breakpoint_rq['url'] = url
        if url_regex:
            set_breakpoint_rq['urlRegex'] = url_regex
        if script_hash:
            set_breakpoint_rq['scriptHash'] = script_hash
        if column_number:
            set_breakpoint_rq['columnNumber'] = column_number
        if condition:
            set_breakpoint_rq['condition'] = condition

        # 是否在该位置已经设置断点
        breakpoint_id = None
        for _breakpoint_id, debug_info in self._debug_patterns_dict.items():
            if debug_info['set_breakpoint_rq'] == set_breakpoint_rq:
                breakpoint_id = _breakpoint_id

        if breakpoint_id is None:
            breakpoint_info = self.page.run_cdp(
                "Debugger.setBreakpointByUrl",
                **set_breakpoint_rq)

            breakpoint_id = breakpoint_info['breakpointId']
            location_list = breakpoint_info['locations']
            if not location_list:
                logger.warning(
                    f"set breakpoint maybe failed, because locations is empty, set_breakpoint_rq: {set_breakpoint_rq}")

            breakpoint_info['set_breakpoint_rq'] = set_breakpoint_rq
            self._debug_patterns_dict[breakpoint_id] = breakpoint_info

        def wrapper(func):
            # 用户等待Debug执行需要
            self._debug_patterns_dict[breakpoint_id]['wait'] = 0
            self._debug_patterns_dict[breakpoint_id]['running_count'] = 0
            if breakpoint_id not in self._debug_fun_dict:
                self._debug_fun_dict[breakpoint_id] = [func]
            else:
                self._debug_fun_dict[breakpoint_id].append(func)
            return func

        return wrapper

    def _debug_event_fun(self, **kwargs):
        breakpoint_id_list = kwargs['hitBreakpoints']
        for breakpoint_id, func_list in self._debug_fun_dict.items():
            if breakpoint_id in breakpoint_id_list:
                for func in func_list:
                    func(**kwargs)
                self._debug_patterns_dict[breakpoint_id]['wait'] = 1
                self._debug_patterns_dict[breakpoint_id]['running_count'] += 1
                logger.info(f"breakpoint_id: {breakpoint_id}, running_count: {self._debug_patterns_dict[breakpoint_id]['running_count']}")

    def wait(self, count, **breakpoint):
        breakpoint_id = self._find_breakpoint(**breakpoint)

        while self._debug_patterns_dict[breakpoint_id]['wait'] == 0:
            self.page.wait(0.5)

        while self._debug_patterns_dict[breakpoint_id]['running_count'] < count:
            self.page.wait(0.5)

        running_count = self._debug_patterns_dict[breakpoint_id]['running_count']
        return running_count

    def evaluate_on_call_frame(self,
                               call_frame_id,
                               expression,
                               object_group=None,
                               include_command_line_api=None,
                               silent=None,
                               return_by_value=True,
                               generate_preview=None,
                               throw_on_side_effect=None,
                               timeout=None,
                               ):
        """
        https://chromedevtools.github.io/devtools-protocol/tot/Debugger/#method-evaluateOnCallFrame
        :return:
        """
        evaluate_on_call_frame_rq = dict()
        evaluate_on_call_frame_rq['callFrameId'] = call_frame_id
        evaluate_on_call_frame_rq['expression'] = expression
        if object_group:
            evaluate_on_call_frame_rq['objectGroup'] = object_group
        if include_command_line_api:
            evaluate_on_call_frame_rq['includeCommandLineAPI'] = include_command_line_api
        if silent:
            evaluate_on_call_frame_rq['silent'] = silent
        if return_by_value:
            evaluate_on_call_frame_rq['returnByValue'] = return_by_value
        if generate_preview:
            evaluate_on_call_frame_rq['generatePreview'] = generate_preview
        if throw_on_side_effect:
            evaluate_on_call_frame_rq['throwOnSideEffect'] = throw_on_side_effect
        if timeout:
            evaluate_on_call_frame_rq['timeout'] = timeout

        rt = self.page.run_cdp(
            "Debugger.evaluateOnCallFrame",
            **evaluate_on_call_frame_rq
        )
        return rt

    def _remove_breakpoint(self, breakpoint_id):
        """
        https://chromedevtools.github.io/devtools-protocol/tot/Debugger/#method-removeBreakpoint
        :param breakpoint_id:
        :return:
        """
        remove_breakpoint_rq = dict()
        remove_breakpoint_rq['breakpointId'] = breakpoint_id
        rt = self.page.run_cdp(
            "Debugger.removeBreakpoint",
            **remove_breakpoint_rq
        )
        assert rt == {}
        del self._debug_patterns_dict[breakpoint_id]
        del self._debug_fun_dict[breakpoint_id]
        return rt

    def remove_breakpoint(self, **breakpoint):
        breakpoint_id = self._find_breakpoint(**breakpoint)
        if breakpoint_id:
            return self._remove_breakpoint(breakpoint_id)

    def _find_breakpoint(self, line_number,
                         url=None,
                         url_regex=None,
                         script_hash=None,
                         column_number=None,
                         condition=None):

        set_breakpoint_rq = dict()
        set_breakpoint_rq['lineNumber'] = line_number
        if url:
            set_breakpoint_rq['url'] = url
        if url_regex:
            set_breakpoint_rq['urlRegex'] = url_regex
        if script_hash:
            set_breakpoint_rq['scriptHash'] = script_hash
        if column_number:
            set_breakpoint_rq['columnNumber'] = column_number
        if condition:
            set_breakpoint_rq['condition'] = condition

        for breakpoint_id, debug_info in self._debug_patterns_dict.items():
            if debug_info['set_breakpoint_rq'] == set_breakpoint_rq:
                return breakpoint_id
            else:
                return None

    def resume(self):
        """
        """
        rt = self.page.run_cdp("Debugger.resume")
        return rt

    def disable(self):
        rt = self.page.run_cdp('Debugger.disable')
        return rt
