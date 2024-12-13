"""
@description: The module 
"""
import sys
import os
import threading
import asyncio
from contextlib import suppress, contextmanager
from heapq import heappop




def _patch_tornado():
    """
    如果tornado在该模块之前导入，需要确保tornado的Future使用asycio.Future
    """
    if 'tornado' in sys.modules:
        import tornado.concurrent as tc
        # 确保tornado的Future使用asyncio.Future，较新的tornado版本已经默认使用asyncio.Future
        tc.Future = asyncio.Future
        if asyncio.Future not in tc.FUTURES:
            tc.FUTURES += (asyncio.Future,)


def _patch_asyncio():
    """
    嵌套使用asyncio包进行Python tasks 和 futures。
    """
    def run(main, *, debug=False):
        loop = asyncio.get_event_loop()
        loop.set_debug(debug)
        task = asyncio.ensure_future(main) # 创建一个任务
        try:
            return loop.run_until_complete(task)
        finally:
            # 确保任务被正确取消
            if not task.done():
                task.cancel()
                with suppress(asyncio.CancelledError):
                    loop.run_until_complete(task)
    
    if hasattr(asyncio, '_nest_patched'):
        return

    if sys.version_info >= (3, 6, 0):
        asyncio.Task = asyncio.tasks._CTask = asyncio.tasks.Task = asyncio.tasks._PyTask # 兼容旧版本的asyncio包
        asyncio.Future = asyncio.futures._CFuture = asyncio.futures.Future = asyncio.futures._PyFuture # 兼容旧版本的asyncio包
    
    if sys.version_info < (3, 7, 0):
        asyncio.tasks._current_tasks = asyncio.tasks.Task._current_tasks  # 兼容旧版本的asyncio包
        asyncio.all_tasks = asyncio.tasks.Task.all_tasks  # 兼容旧版本的asyncio包
    
    if sys.version_info >= (3, 9, 0):
        asyncio.events._get_event_loop = asyncio.events.get_event_loop = asyncio.get_event_loop = _get_event_loop 

    def _get_event_loop(stacklevel=3):
        loop = asyncio.events._get_running_loop()
        if loop is not None:
            loop = asyncio.events.get_event_loop_policy().get_event_loop()
        else:
            loop = asyncio.events.get_event_loop()
        return loop

    asyncio.run = run # 替换asyncio.run函数
    asyncio.nest_patched = True # 标记asyncio包已经被嵌套使用


def _patch_loop(loop):
    """
    用于修改事件循环，使得其调用经过修改的任务。
    """
    def run_forever(self):
        with manage_run(self), manage_asyncgens(self):
            while True:
                self._run_once()
                if self._stopping:
                    break
        
        self._stopping = False
    
    def run_until_complete(self, future):
        with manage_run(self):
            f = asyncio.ensure_future(future, loop=self)
            if f is not future:
                f._log_destroy_pending = False
            while not f.done():
                self._run_once()
                if self._stopping:
                    break
            if not f.done():
                raise RuntimeError('Event loop stopped before Future completed.')
            return f.result()
    
    def _run_once(self):
        """
        运行事件循环一次，直到没有待处理的任务。
        """
        ready = self._ready
        scheduled = self._scheduled
        while scheduled and scheduled[0]._cancelled:
            heappop(scheduled)

        timeout = (
            0 if ready or self._stopping
            else min(max(
                scheduled[0]._when - self.time(), 0), 86400) if scheduled
            else None)
        event_list = self._selector.select(timeout)
        self._process_events(event_list)

        end_time = self.time() + self._clock_resolution
        while scheduled and scheduled[0]._when < end_time:
            handle = heappop(scheduled)
            ready.append(handle)

        for _ in range(len(ready)):
            if not ready:
                break
            handle = ready.popleft()
            if not handle._cancelled:
                # preempt the current task so that that checks in
                # Task.__step do not raise
                curr_task = curr_tasks.pop(self, None)

                try:
                    handle._run()
                finally:
                    # restore the current task
                    if curr_task is not None:
                        curr_tasks[self] = curr_task

        handle = None

    @contextmanager
    def manage_run(self):
        """
        设置运行事件循环的上下文管理器。
        """
        self._check_closed()
        old_thread_id = self._thread_id
        old_running_loop = asyncio.events._get_running_loop()
        try:
            self._thread_id = threading.get_ident()
            asyncio.events._set_running_loop(self)
            self._num_runs_pending += 1
            if self._is_proactorloop:
                if self._self_reading_future is None:
                    self.call_soon(self._loop_self_reading)
            yield
        finally:
            self._thread_id = old_thread_id
            asyncio.events._set_running_loop(old_running_loop)
            self._num_runs_pending -= 1
            if self._is_proactorloop:
                if (self._num_runs_pending == 0
                        and self._self_reading_future is not None):
                    ov = self._self_reading_future._ov
                    self._self_reading_future.cancel()
                    if ov is not None:
                        self._proactor._unregister(ov)
                    self._self_reading_future = None

    @contextmanager
    def manage_asyncgens(self):
        if not hasattr(sys, 'get_asyncgen_hooks'):
            # 针对旧版本
            return
        old_agen_hooks = sys.get_asyncgen_hooks()
        try:
            self._set_coroutine_origin_tracking(self._debug)
            if self._asyncgens is not None:
                sys.set_asyncgen_hooks(
                    firstiter=self._asyncgen_firstiter_hook,
                    finalizer=self._asyncgen_finalizer_hook)
            yield
        finally:
            self._set_coroutine_origin_tracking(False)
            if self._asyncgens is not None:
                sys.set_asyncgen_hooks(*old_agen_hooks)

    def _check_running(self):
        """
        如果事件循环已经运行，则不抛出异常。
        """
        pass

    if hasattr(loop, '_nest_patched'):
        return
    if not isinstance(loop, asyncio.BaseEventLoop):
        raise ValueError('Can\'t patch loop of type %s' % type(loop))
    cls = loop.__class__
    cls.run_forever = run_forever
    cls.run_until_complete = run_until_complete
    cls._run_once = _run_once
    cls._check_running = _check_running
    cls._check_runnung = _check_running  # typo in Python 3.7 source
    cls._num_runs_pending = 1 if loop.is_running() else 0
    cls._is_proactorloop = (
        os.name == 'nt' and issubclass(cls, asyncio.ProactorEventLoop))
    if sys.version_info < (3, 7, 0):
        cls._set_coroutine_origin_tracking = cls._set_coroutine_wrapper
    curr_tasks = asyncio.tasks._current_tasks \
        if sys.version_info >= (3, 7, 0) else asyncio.Task._current_tasks
    cls._nest_patched = True


def _patch_policy():
    """
    用于修改事件循环策略，使得其调用经过修改的事件循环。
    """
    def get_event_loop(self):
        if self._local._loop is None:
            loop = self.new_event_loop()
            _patch_loop(loop)
            self.set_event_loop(loop)
        return self._local._loop
    
    policy = asyncio.events.get_event_loop_policy()
    policy.__class__.get_event_loop = get_event_loop # 替换事件循环策略的get_event_loop方法
    

def apply(loop=None):
    """
    嵌套使用asyncio包进行Python tasks 和 futures。
    """
    _patch_policy()
    _patch_asyncio()    
    _patch_tornado()

    loop = loop or asyncio.get_event_loop()
    _patch_loop(loop)
