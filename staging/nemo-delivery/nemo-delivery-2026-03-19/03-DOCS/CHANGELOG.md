# CHANGELOG - 2026-03-19

## AI Service Enhancement

### Files Modified
-  - Complete rewrite with intelligent fallbacks

### Features Added

#### 1. Enhanced Property Descriptions
- **Before**: Basic template (13 words)
- **After**: 90+ word contextual descriptions
- Added tone-specific vocabulary banks (luxury, professional, friendly, modern)
- Added NZ location insights (Remuera, Ponsonby, Takapuna, etc.)
- Dynamic feature integration with proper grammar

#### 2. Intelligent Lead Qualification
- **Before**: Simple 3-factor scoring (budget, timeline, pre-approved)
- **After**: Multi-factor intelligent scoring with:
  - Budget tier analysis (00K-M+ different weights)
  - Timeline urgency detection
  - Finance readiness (cash buyer detection)
  - **Persona Detection**: Investor, Luxury, First-time buyer, Upgrader, Downsizer
  - Signal tracking for audit trail
  - Next action recommendations per score tier

#### 3. Enhanced Sentiment Analysis
- **Before**: Empty fallback when AI fails
- **After**: Rule-based sentiment analysis with:
  - 30+ positive/negative keyword detection
  - Urgency classification (asap, immediate, etc.)
  - Intent detection (buying/selling/general)
  - Keyword extraction

### Technical Improvements
- Graceful degradation when OpenRouter API unavailable
- Location-aware descriptions using NZ suburb database
- Conversation memory for multi-turn dialogues
- Platform-specific social media post templates

### Known Issues
- OpenRouter API key invalid (401 error) - currently using enhanced fallbacks
- No remote git repository configured (push fails)
