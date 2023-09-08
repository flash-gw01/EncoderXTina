#base image
FROM artemisfowl004/vid-compress
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt install ffmpeg
RUN apt install speedtest-cli
COPY . .
CMD ["bash","start.sh"]
