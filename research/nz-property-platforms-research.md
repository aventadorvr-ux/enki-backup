# NZ Property Platform Research
## Alternative Platforms to TradeMe

**Date:** March 12, 2026  
**Purpose:** Identify all major NZ property advertising platforms and APIs

---

## Platform Rankings (by Importance)

### 1. TradeMe Property 🥇
**Market Position:** #1 by traffic and listings
**API:** ❌ No public API
**Approach:** Web scraping required
**Why Critical:**
- 70%+ of NZ property searches start here
- Agents MUST list on TradeMe
- Largest audience reach
- Auction platform

**Integration Strategy:**
- Scrape listings (respect robots.txt)
- Parse HTML for: price, address, beds, baths, agent info
- Use puppeteer/js-fetch.js for dynamic content
- Rate limit: 1 request per 5 seconds recommended

---

### 2. Realestate.co.nz 🥈
**Market Position:** #2, Official industry platform
**API:** ✅ YES - FeedAPI
**URL:** https://feedapi.developers.realestate.co.nz/

**Why Critical:**
- Owned by Real Estate Institute of NZ (REINZ)
- Industry-standard platform
- Official API for registered agents
- Real-time listing updates
- Better agent tools than TradeMe

**API Details:**
- **Name:** FeedAPI
- **Languages:** JavaScript, Ruby SDKs
- **Auth:** API keys (requires registration)
- **Features:**
  - Publish listings in real-time
  - Update/retrieve all listings
  - Bulk upload support
  - Image handling

**Integration Strategy:**
- Register as "data provider"
- Use official API for listing management
- Lower priority than TradeMe for scraping (has API)

---

### 3. OneRoof 🥉
**Market Position:** #3, Strong in Auckland
**Owner:** NZME (NZ Media & Entertainment)
**API:** ❌ No public API
**Unique Features:**
- Property valuation estimates
- Market insights
- 240K higher estimates than competitors (per Reddit)
- Strong mobile app

**Why Useful:**
- Alternative audience to TradeMe
- Valuation data for CMAs
- Growing market share

**Integration Strategy:**
- Scrape if needed (secondary priority)
- Use for market intelligence

---

### 4. Homes.co.nz
**Market Position:** Valuation specialist
**Properties:** 1.7M NZ properties
**API:** ❌ Limited/Unofficial
**Unique Features:**
- Free estimated values
- Sales histories
- Council records
- Beautiful map interface
- No login required

**Why Useful:**
- Valuation data for AI agent
- Sales history for CMAs
- Comparable property data

**Integration Strategy:**
- Scrape valuations (respectfully)
- Use for pricing intelligence
- Cross-reference with other platforms

---

### 5. HouseHunter.nz
**Market Position:** Aggregator/Tool
**Type:** Third-party scraper
**URL:** https://www.househunter.nz/

**What It Does:**
- Tracks listings from ALL platforms (TradeMe, RealEstate, Homes, OneRoof)
- No account required
- Organizes in one place
- Private data (stays on device)

**Why It Matters:**
- Proves all platforms are scrapable
- Users want cross-platform tracking
- Our AI agent could offer similar functionality

---

## Integration Priority Matrix

| Platform | Priority | Method | Difficulty | Value |
|----------|----------|--------|------------|-------|
| **TradeMe** | 🔴 CRITICAL | Scrape | Hard | Very High |
| **Realestate.co.nz** | 🔴 CRITICAL | API | Medium | High |
| **OneRoof** | 🟡 MEDIUM | Scrape | Medium | Medium |
| **Homes.co.nz** | 🟡 MEDIUM | Scrape | Easy | Medium |
| **HouseHunter** | 🟢 LOW | Reference | N/A | Low |

---

## API vs Scraping Summary

### Official APIs Available:
1. **Realestate.co.nz FeedAPI** ✅
   - Requires registration
   - Real-time updates
   - Industry standard

### Requires Scraping:
1. **TradeMe** (No API)
   - Largest platform
   - Must use puppeteer/selenium
   - Rate limiting essential

2. **OneRoof** (No public API)
   - Valuation data
   - Secondary priority

3. **Homes.co.nz** (No public API)
   - Historical data
   - Valuation estimates

---

## Technical Implementation

### Recommended Approach:

**Phase 1: MVP**
- Scrape TradeMe (primary source)
- Use Realestate.co.nz FeedAPI if agent is registered
- Focus on listing alerts and lead capture

**Phase 2: Scale**
- Add Homes.co.nz scraping (valuations)
- Add OneRoof scraping (market insights)
- Cross-platform data enrichment

**Phase 3: Advanced**
- Historical price tracking
- Trend analysis across all platforms
- Automated CMA generation

---

## Legal/Compliance Notes

- **robots.txt:** Check each platform's robots.txt
- **Rate Limiting:** 1 req/5 sec minimum to avoid blocks
- **Terms of Service:** Review before scraping
- **Data Usage:** Don't republish scraped data publicly
- **APIs:** Follow Realestate.co.nz FeedAPI terms

---

## Competitive Advantage

**Our AI Agent Can:**
1. Monitor ALL platforms simultaneously
2. Alert on new listings across TradeMe + RE + OneRoof
3. Cross-reference valuations (OneRoof vs Homes vs QV)
4. Track price changes over time
5. Identify FSBOs and expiring listings

**No single platform offers this.**

---

## Action Items

- [ ] Test TradeMe scraping with js-fetch.js
- [ ] Register for Realestate.co.nz FeedAPI
- [ ] Evaluate Homes.co.nz scraping approach
- [ ] Document rate limiting strategy
- [ ] Create unified data schema for all platforms

---

**Conclusion:** TradeMe is #1 but not the only game. Realestate.co.nz has official API. OneRoof and Homes.co.nz offer valuable data. Our AI agent should integrate with ALL major platforms for comprehensive coverage.

*Research completed by Enki AI - March 12, 2026*
