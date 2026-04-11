# API ENDPOINTS - All Working

## Base URL
http://3.25.170.226:8000

## Health Check
GET /health
Response: {"status": "healthy", "timestamp": "..."}

## List Agents
GET /api/v1/agents
Response: List of 5 agents with descriptions

## Agent Processing
POST /api/v1/agents/{agent_name}/process
Content-Type: application/json

### Available Agents

#### 1. Lead Agent (lead)
Actions:
- "qualify" - Basic rule-based qualification
- "qualify_ai" - AI-enhanced qualification with persona detection
- "respond" - Generate contextual response
- "chat" - Conversational interaction with memory
- "analyze_sentiment" - Sentiment analysis
- "analyze_conversation" - Full conversation intent analysis
- "get_follow_up_recommendations" - AI follow-up recommendations
- "get_conversation_history" - Retrieve chat history
- "route" - Smart lead routing

#### 2. Content Agent (content)
Actions:
- "description" - Basic template description
- "description_ai" - AI-enhanced property description (90+ words)
- "social" - Basic social post
- "social_ai" - AI-optimized social post
- "social_multi_platform" - Generate for multiple platforms
- "email" - Email template
- "email_campaign" - AI-powered email campaign
- "seo_optimize" - SEO optimization for descriptions
- "generate_campaign" - Full marketing campaign
- "get_content_calendar" - Content calendar generation

#### 3. Scheduling Agent (scheduling)
Actions:
- "check_availability" - Check calendar availability
- "book_viewing" - Schedule property viewing
- "book_valuation" - Schedule property valuation
- "get_agent_schedule" - Get agent calendar
- "reschedule" - Reschedule existing booking
- "cancel" - Cancel booking
- "send_reminder" - Send reminder notification
- "optimize_schedule" - AI-optimized scheduling

#### 4. Market Intelligence Agent (market_intel)
Actions:
- "cma" - Comparative Market Analysis
- "cma_enhanced" - AI-enhanced CMA with insights
- "price_trends" - Market price trend analysis
- "neighborhood_report" - Neighborhood analytics
- "investment_analysis" - ROI calculations
- "demand_forecast" - Demand forecasting

#### 5. Transaction Coordinator (transaction)
Actions:
- "checklist" - Generate transaction checklist
- "compliance_check" - Compliance verification
- "document_status" - Track document status
- "timeline" - Transaction timeline
- "deadline_alerts" - Upcoming deadline alerts
- "coordinate_inspection" - Schedule inspections
- "track_conditions" - Track contract conditions

## Example Requests

### Property Description
POST /api/v1/agents/content/process
{"action": "description_ai", "data": {"bedrooms": 4, "bathrooms": 2, "location": "Remuera, Auckland", "features": ["pool", "views"], "tone": "luxury"}}

### Lead Qualification
POST /api/v1/agents/lead/process
{"action": "qualify_ai", "data": {"budget": 1200000, "timeline": "immediate", "pre_approved": true, "notes": "Cash buyer"}}

## Test Results
All 4 API tests PASSING
- test_root ✓
- test_health ✓
- test_list_agents ✓
- test_lead_agent_qualify ✓
