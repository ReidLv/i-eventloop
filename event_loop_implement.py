# -*- encoding: utf-8 -*-
import time


def job1():
    print("do job 1")


def job2():
    print("do job 2")


class Task(object):

    def __init__(self):
        # task实际需要执行的逻辑函数
        self.callback_func = None

        # 循环的自定义条件
        self.condition_func = None

        # 时间单位：毫秒
        # 事件循环运行前的延迟时间
        self.time_delay = 0

        # 事件循环间隔时间
        # 负数: 无间隔
        # 0: 无间隔
        # 正数: 间隔时长
        self.cycle_time_interval = 0

        # 循环次数
        # 负数: 循环次数 = 无限次
        # 0: 循环次数 = 0次
        # 正数: 循环次数 = int(value)
        self.cycle_number = 0

        # 任务开始时间
        self.initialize_time = 0

        # 第一次循环开始时间
        self.cycle_initialize_time = 0

        # 已完成的循环次数
        self.cycled_number = 0

    def register(self, callback_func, condition_func=lambda: True, time_delay=0, cycle_time_interval=0, cycle_number=-1):
        self.callback_func = callback_func
        self.condition_func = condition_func
        self.time_delay = time_delay
        self.cycle_time_interval = cycle_time_interval
        self.cycle_number = cycle_number

    def initialize(self):
        self.initialize_time = time.time()

    def check(self):
        # 循环次数不满足
        if 0 < self.cycle_number <= self.cycled_number:
            return False

        now = time.time()
        # 事件循环运行前的延迟时间不满足
        if now - self.initialize_time <= self.time_delay:
            return False
        # 事件循环间隔时间不满足
        if now - self.cycle_initialize_time <= self.cycle_time_interval:
            return False
        # 循环的自定义条件不满足
        if not self.condition_func():
            return False
        # check通过，认定此次循环有效
        self.cycle_initialize_time = now
        self.cycled_number += 1

        return True

    def run(self, *args, **kwargs):
        if self.check():
            return self.callback_func(*args, **kwargs)


class EventLoop(object):
    task_list: [Task] = []

    @classmethod
    def register(cls, task):
        cls.task_list.append(task)

    @classmethod
    def run(cls):
        for task in cls.task_list:
            task.initialize()
        while True:
            for task in cls.task_list:
                task.run()


if __name__ == '__main__':
    now_ = time.time()
    task1 = Task()
    task1.register(job1, condition_func=lambda: time.time() > now_ + 10, time_delay=1, cycle_number=2, cycle_time_interval=2)

    task2 = Task()
    task2.register(job2, condition_func=lambda: False, time_delay=2, cycle_number=3, cycle_time_interval=3)

    EventLoop.register(task1)
    EventLoop.register(task2)

    EventLoop.run()
