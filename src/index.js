const puppeteer = require('puppeteer');

(async () => {
  const selector = process.argv[5];

  const browser = await puppeteer.launch({
    executablePath: 'chromium-browser',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
    ],
  });

  try {
    const page = await browser.newPage();

    const path = process.argv[6];
    const headers = JSON.parse(process.argv[7]);

    page.setViewport({ width: 1920, height: 1080 });

    page.setExtraHTTPHeaders(headers);

    await page.goto(process.argv[3], { waitUntil: 'networkidle0' });

    if (process.argv[4]) {
      await page.waitFor(process.argv[4]);
    }

    const rect = await page.evaluate(selector => {
      const element = document.querySelector(selector);
      const { x, y, width, height } = element.getBoundingClientRect();
      return { left: x, top: y, width, height, id: element.id };
    }, selector);

    await page.screenshot({
      path,
      clip: {
        x: rect.left,
        y: rect.top,
        width: rect.width,
        height: rect.height,
      },
    });
  } catch (e) {
    console.log(e);
  } finally {
    await browser.close();
  }
})();
