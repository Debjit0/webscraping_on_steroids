const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    const productUrl = 'https://2717recovery.com/products/recovery-cream';
    
    await page.goto(productUrl, { waitUntil: 'networkidle' });

    // Get the page source
    const pageSource = await page.content();

    // Output the page source to a file
    const fs = require('fs');
    fs.writeFileSync('pageSource.html', pageSource);

    await browser.close();
})();