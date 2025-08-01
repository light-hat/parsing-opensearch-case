FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unzip \
    xvfb \
    fonts-ipafont-gothic \
    fonts-wqy-zenhei \
    fonts-thai-tlwg \
    fonts-kacst \
    fonts-freefont-ttf \
    libxss1 \
    wget \
    --no-install-recommends

RUN CHROME_VERSION="138.0.7204.157-1" && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable=$CHROME_VERSION --no-install-recommends

RUN CHROMEDRIVER_VERSION="138.0.7204.157" && \
    wget -q -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN groupadd -r chrome && useradd -r -g chrome -G audio,video chrome \
    && mkdir -p /home/chrome && chown -R chrome:chrome /home/chrome

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY stealth_crawler.py .

USER chrome
WORKDIR /home/chrome

CMD ["xvfb-run", "python", "/stealth_crawler.py", "https://av.ru/"]
