# 使用一个适合的Django基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

RUN apt-get update && apt-get install -y libgl1-mesa-glx

# 安装 Pipenv
RUN pip install pipenv

# 将 Pipfile 和 Pipfile.lock 复制到容器中
COPY Pipfile Pipfile.lock /app/

# 使用 Pipenv 安装依赖，指定镜像源
ENV PIPENV_VENV_IN_PROJECT=1
RUN pipenv install -i https://mirrors.aliyun.com/pypi/simple/ --deploy --ignore-pipfile

# 复制应用代码到容器中
COPY . /app/

# 暴露Django应用的端口
EXPOSE 8000

# 启动Django应用
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]