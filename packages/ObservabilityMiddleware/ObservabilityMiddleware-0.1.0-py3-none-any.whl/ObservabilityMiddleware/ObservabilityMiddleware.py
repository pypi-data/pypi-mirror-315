import time
import logging
from logging.handlers import RotatingFileHandler
from prometheus_client import Counter,Histogram,make_wsgi_app
import os
from pythonjsonlogger import jsonlogger
import contextvars
import json
from starlette.responses import Response
from ddtrace import tracer
from ddtrace.context import Context
from ddtrace.propagation.http import HTTPPropagator
import inspect

# 创建logs目录（如果不存在）
#if not os.path.exists('logs'):
#    os.makedirs('logs')
# 创建日志格式器
class UTF8JsonFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        
    def format(self, record):
        # 从当前 span 获取 trace_id
        span = tracer.current_span()
        trace_id = str(span.trace_id) if span else "0"
        span_id = str(span.span_id) if span else "0"
        
        # 自动设置 logger_name 为模块名
        if not getattr(record, 'logger_name', None):
            # 直接使用 record 中的 module 属性
            record.logger_name = record.module  # 设置为模块名
        
        log_data = {
            'asctime': self.formatTime(record),
            'levelname': record.levelname,
            'message': record.getMessage(),
            'pathname': record.pathname,
            'lineno': record.lineno,
            'logger': record.logger_name,  # 使用自动设置的 logger_name
            'trace_id': trace_id,
            'span_id': span_id
        }
        
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        
        return json.dumps(log_data, ensure_ascii=False)

# 使用新的格式器
#formatter = UTF8JsonFormatter()

# 创建上下文变量
request_context = contextvars.ContextVar('request_context', default={})

# 创建logger
#logger = logging.getLogger("observability")
#logger.setLevel(logging.INFO)
# 创建控制台处理器
#console_handler = logging.StreamHandler()
#console_handler.setFormatter(formatter)
#logger.addHandler(console_handler)

# 创建文件处理器
#file_handler = RotatingFileHandler(
 #   'logs/observability.log',
  #  maxBytes=100*1024*1024,  # 100MB
   # backupCount=5,
    #encoding='utf-8'
#)
#file_handler.setFormatter(formatter)
#logger.addHandler(file_handler)


#Prometheus指标
REQUEST_COUNT = Counter('http_requests_total','Total HTTP Requests',
                        ['method','endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 
                            'HTTP Request Duration', ['method', 'endpoint'])
class ObservabilityMiddleware:
    def __init__(self, app, log_config=None):
        self.app = app
        self.common_extra = {
            "appName": "observability",
            "appVersion": "1.0.0",
            "appEnv": "dev"
        }
        self.tracer = tracer
        self.propagator = HTTPPropagator()
        
        # 默认日志配置
        default_log_config = {
            'log_dir': 'logs',
            'log_file': 'observability.log',  # 确保使用统一的日志文件名
            'max_bytes': 10 * 1024 * 1024,  # 10MB
            'backup_count': 5,
            'level': logging.INFO
        }

        # 更新配置
        self.log_config = default_log_config
        if log_config:
            self.log_config.update(log_config)

        # 确保日志目录存在
        os.makedirs(self.log_config['log_dir'], exist_ok=True)

        # 设置日志处理器
        formatter = UTF8JsonFormatter()

        # 文件处理器
        log_path = os.path.join(self.log_config['log_dir'], self.log_config['log_file'])
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=self.log_config['max_bytes'],
            backupCount=self.log_config['backup_count'],
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # 配置根日志器
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_config['level'])

        # 移除所有已存在的处理器
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # 添加处理器到根日志器
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

    # FastAPI 处理
    async def __call__(self, request, call_next):
        start_time = time.time()
        
        # 提取链路上下文
        headers = dict(request.headers)
        context = self.propagator.extract(headers)
        if context:
            self.tracer.context_provider.activate(context)

        # 创建 span
        with self.tracer.trace(
            "http.request",
            service=self.common_extra["appName"],
            resource=f"{request.method} {request.url.path}",
            span_type="web"
        ) as span:
            span.set_tag("http.method", request.method)
            span.set_tag("http.url", str(request.url))
            
            context = {
                **self.common_extra,
                "requestMethod": request.method,
                "requestPath": request.url.path,
                "trace_id": str(span.trace_id),
                "span_id": str(span.span_id)
            }
            request_context.set(context)

            if request.url.path == "/metrics":
                return Response(
                    content=make_wsgi_app()(
                        {"PATH_INFO": "/metrics", "REQUEST_METHOD": "GET"},
                        lambda *args: None
                    )[0],
                    media_type="text/plain"
                )

            try:
                response = await call_next(request)
                span.set_tag("http.status_code", response.status_code)
                
                duration = time.time() - start_time
                context["responseTime"] = f"{duration:.4f}"
                request_context.set(context)
                
                REQUEST_COUNT.labels(
                    method=request.method,
                    endpoint=request.url.path
                ).inc()
                REQUEST_LATENCY.labels(
                    method=request.method,
                    endpoint=request.url.path
                ).observe(duration)

                return response
            except Exception as e:
                span.set_tag("error", str(e))
                span.set_tag("error.type", type(e).__name__)
                raise

    # Flask 处理
    def __call_wsgi__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        method = environ.get('REQUEST_METHOD', '')
        
        if path == '/metrics':
            return make_wsgi_app()(environ, start_response)

        # 提取链路上下文
        headers = {k[5:].lower(): v for k, v in environ.items() 
                  if k.startswith('HTTP_')}
        context = self.propagator.extract(headers)
        if context:
            self.tracer.context_provider.activate(context)

        start_time = time.time()
        
        # 创建 span
        with self.tracer.trace(
            "http.request",
            service=self.common_extra["appName"],
            resource=f"{method} {path}",
            span_type="web"
        ) as span:
            span.set_tag("http.method", method)
            span.set_tag("http.url", path)
            
            context = {
                **self.common_extra,
                "requestMethod": method,
                "requestPath": path,
                "trace_id": str(span.trace_id),
                "span_id": str(span.span_id)
            }
            request_context.set(context)

            status_code = None
            def custom_start_response(status, headers, exc_info=None):
                nonlocal status_code
                status_code = int(status.split()[0])
                span.set_tag("http.status_code", status_code)
                
                duration = time.time() - start_time
                context["responseTime"] = f"{duration:.4f}"
                request_context.set(context)
                
                REQUEST_COUNT.labels(
                    method=method,
                    endpoint=path
                ).inc()
                REQUEST_LATENCY.labels(
                    method=method,
                    endpoint=path
                ).observe(duration)
                
                return start_response(status, headers, exc_info)

            try:
                return self.app(environ, custom_start_response)
            except Exception as e:
                span.set_tag("error", str(e))
                span.set_tag("error.type", type(e).__name__)
                raise

    # _convert_wsgi_to_asgi 方法保持不变

# 创建一个包装器函数来自动添加上下文信息
def log_with_context(func):
    def wrapper(self, message, *args, **kwargs):
        context = request_context.get()
        if 'extra' in kwargs:
            if kwargs['extra'] is None:
                kwargs['extra'] = {}
            if isinstance(kwargs['extra'], dict):
                kwargs['extra'] = {**context, **kwargs['extra']}
        else:
            kwargs['extra'] = context
        return func(self, message, *args, **kwargs)
    return wrapper

# 扩展 Logger 类
class ContextLogger(logging.Logger):
    @log_with_context
    def info(self, message, *args, **kwargs):
        super().info(message, *args, **kwargs)

    @log_with_context
    def error(self, message, *args, **kwargs):
        super().error(message, *args, **kwargs)

    @log_with_context
    def warning(self, message, *args, **kwargs):
        super().warning(message, *args, **kwargs)

    @log_with_context
    def debug(self, message, *args, **kwargs):
        super().debug(message, *args, **kwargs)

# 注册自定义 Logger 类
logging.setLoggerClass(ContextLogger)
logger = logging.getLogger("observability")