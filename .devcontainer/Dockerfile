FROM python:slim
ENV PYTHONPATH=.

# install deps
RUN apt update -y && apt install curl zsh git -y
# poetry, ohMyZsh
RUN pip install poetry
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
