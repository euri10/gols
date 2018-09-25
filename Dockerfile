# base image
FROM alpine:3.8
# set working directory
WORKDIR /usr/src/app
COPY . /usr/src/app
COPY 99-garmin-fenix2.rules /etc/udev/rules.d/
RUN apk update --no-cache && \
apk add udev && \
apk add python3 && \
python3 -m ensurepip && \
rm -r /usr/lib/python*/ensurepip && \
pip3 install -e .

CMD ["/bin/ash"]
