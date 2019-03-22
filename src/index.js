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

  const page = await browser.newPage();

  try {
    const path = process.argv[6];
    const headers = JSON.parse(process.argv[7]);
    const viewport_width = process.argv[8];
    const viewport_height = process.argv[9];
    const waitSelectors = JSON.parse(process.argv[4]);

    page.setViewport({ width: viewport_width, height: viewport_height });

    page.setExtraHTTPHeaders(headers);

    await page.goto(process.argv[3], { waitUntil: 'networkidle0' });

    if (waitSelectors.length > 0) {
      waitSelectors.each(async wait => {
        await page.waitFor(wait);
      });
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
