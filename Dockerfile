FROM python:3.11.3-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY . .

# Install dependencies
RUN pip3 install -r requirements.txt 

EXPOSE 5000
ENTRYPOINT ["python3"] 
CMD ["http_server.py"]
