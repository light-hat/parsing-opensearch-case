FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unzip \
    xvfb \
    xauth \
    fonts-ipafont-gothic \
    fonts-wqy-zenhei \
    fonts-thai-tlwg \
    fonts-kacst \
    fonts-freefont-ttf \
    libxss1 \
    wget \
    --no-install-recommends

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update -y \
    && apt-get install -y google-chrome-stable --no-install-recommends

RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1) \
    && CHROMEDRIVER_URL=$(wget -qO- https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_VERSION) \
    && wget -q -O /tmp/chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_URL/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /bin/ \
    && chmod +x /bin/chromedriver \
    && rm -rf /tmp/chromedriver*

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN groupadd -r chrome && useradd -r -g chrome -G audio,video chrome \
    && mkdir -p /home/chrome && chown -R chrome:chrome /home/chrome

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY stealth_crawler.py .

USER chrome
WORKDIR /home/chrome

RUN google-chrome --version \
    && chromedriver --version \
    && echo "Chrome and ChromeDriver versions verified"

CMD ["xvfb-run", "python", "/stealth_crawler.py"]
