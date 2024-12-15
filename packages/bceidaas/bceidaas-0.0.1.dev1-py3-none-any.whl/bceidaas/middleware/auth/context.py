from threading import RLock
from contextvars import ContextVar


class SingletonContext(object):
    """
    单例模式，用于保存全局变量。
    """
    single_lock = RLock()

    def __init__(self, name):
        """
        初始化
        """
        self.context = ContextVar(name, default={})

    @classmethod
    def instance(cls, *args, **kwargs):
        """
        get instance
        """
        with SingletonContext.single_lock:
            if not hasattr(SingletonContext, "_instance"):
                SingletonContext._instance = SingletonContext(*args, **kwargs)
        return SingletonContext._instance

    @staticmethod
    def set_var_value(key: str, value: str):
        """
        set context value。
        :param key: 变量名
        :param value: 变量值
        """
        var = SingletonContext.instance().context.get()
        if var is None:
            return False

        var[key] = value
        SingletonContext.instance().context.set(var)



    @staticmethod
    def get_context():
        """
        get context
        """
        var = SingletonContext.instance().context.get()
        return var

    @staticmethod
    def get_var_value(key: str):
        """
        get context value
        """
        var = SingletonContext.instance().context.get()
        if var is None:
            return None
        return var.get(key)