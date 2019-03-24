const puppeteer = require('puppeteer');
const minimist = require('minimist');

const args = minimist(process.argv);
const { url, path, selector, waitseconds } = args;
const headers = JSON.parse(args.headers);
const viewportWidth = parseInt(args.vwidth, 10);
const viewportHeight = parseInt(args.vheight, 10);
const waitSelectors = JSON.parse(args.waitselectors);

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'chromium-browser',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
    ],
  });

  const page = await browser.newPage();

  try {
    page.setViewport({
      width: viewportWidth,
      height: viewportHeight,
    });

    page.setExtraHTTPHeaders(headers);

    await page.goto(url, { waitUntil: 'networkidle0' });

    if (waitSelectors.length > 0) {
      waitSelectors.forEach(async wait => {
        await page.waitForSelector(wait);
      });
    }
    await page.waitFor(waitseconds);
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
    console.error(e);
  } finally {
    await page.close();
    await browser.close();
  }
})();
