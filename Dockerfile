


FROM python:3.11

EXPOSE 8000 

WORKDIR /app/Amazon_Webcrawler
ADD . /app

ADD requirements.txt .

RUN python -m pip install -r /app/requirements.txt

RUN playwright install

RUN playwright install-deps 


CMD ["scrapy", "crawl","Amazon_Webcrawler"] 