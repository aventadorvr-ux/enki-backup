#!/usr/bin/env node
/**
 * js-fetch.js
 * Fetch content from JavaScript-heavy websites using Puppeteer + system Chromium
 * 
 * Usage: node js-fetch.js <url> [output-file]
 * 
 * Dependencies:
 *   npm install -g puppeteer-core cheerio
 * 
 * Requires system Chromium at /usr/bin/chromium-browser (or set CHROMIUM_PATH)
 */

const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const CHROMIUM_PATH = process.env.CHROMIUM_PATH || '/usr/bin/chromium-browser';

async function fetchPage(targetUrl, outputFile = null) {
    let browser;
    try {
        console.log(`Launching browser at ${CHROMIUM_PATH}...`);
        browser = await puppeteer.launch({
            executablePath: CHROMIUM_PATH,
            headless: true,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
            ]
        });
        
        const page = await browser.newPage();
        
        // Set user agent to avoid bot detection
        await page.setUserAgent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
        );
        
        console.log(`Navigating to ${targetUrl}...`);
        await page.goto(targetUrl, {
            waitUntil: 'networkidle2',
            timeout: 60000
        });
        
        // Wait for page to stabilize
        await new Promise(r => setTimeout(r, 2000));
        
        // Extract content
        const content = await page.evaluate(() => {
            // Remove script/style tags
            const unwanted = document.querySelectorAll('script, style, noscript, iframe, svg');
            unwanted.forEach(el => el.remove());
            
            return {
                title: document.title,
                url: window.location.href,
                meta: {
                    description: document.querySelector('meta[name="description"]')?.content || '',
                    keywords: document.querySelector('meta[name="keywords"]')?.content || '',
                    ogTitle: document.querySelector('meta[property="og:title"]')?.content || '',
                    ogDescription: document.querySelector('meta[property="og:description"]')?.content || '',
                },
                text: document.body.innerText
                    .replace(/\n\s*\n/g, '\n\n')  // Compress multiple newlines
                    .replace(/\n{4,}/g, '\n\n\n')  // Max 3 newlines
                    .trim(),
                headings: Array.from(document.querySelectorAll('h1, h2, h3, h4, h5'))
                    .map(h => ({tag: h.tagName, text: h.innerText.trim()}))
                    .filter(h => h.text.length > 0)
                    .slice(0, 20)
            };
        });
        
        const result = {
            source: 'js-fetch',
            fetched_at: new Date().toISOString(),
            url: targetUrl,
            ...content
        };
        
        if (outputFile) {
            fs.writeFileSync(outputFile, JSON.stringify(result, null, 2));
            console.log(`✓ Saved to ${outputFile}`);
        } else {
            console.log('\n--- CONTENT ---\n');
            console.log(result.text.slice(0, 5000));
            if (result.text.length > 5000) {
                console.log(`\n... (${result.text.length - 5000} more characters)`);
            }
        }
        
        return result;
        
    } catch (err) {
        console.error('✗ Error:', err.message);
        process.exit(1);
    } finally {
        if (browser) await browser.close();
    }
}

// CLI usage
if (require.main === module) {
    const [, , url, output] = process.argv;
    
    if (!url) {
        console.log('Usage: node js-fetch.js <url> [output-file.json]');
        console.log('Example: node js-fetch.js "https://www.trademe.co.nz" trademe.json');
        process.exit(1);
    }
    
    fetchPage(url, output);
}

module.exports = { fetchPage };
