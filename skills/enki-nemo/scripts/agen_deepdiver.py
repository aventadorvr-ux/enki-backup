#!/usr/bin/env python3
"""
AGen_DeepDiver - Research Intelligence Agent
Deep research engine for ENKI AGENTIC ecosystem
Digs deep into properties, markets, regulations, and opportunities
"""

import json
import sqlite3
import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import subprocess

class AGen_DeepDiver:
    """
    AGen_DeepDiver - Research Intelligence Specialist
    
    Mission: Conduct deep research on properties, market trends,
    regulatory changes, competitor analysis, and investment opportunities
    """
    
    def __init__(self):
        self.db_path = "/home/ubuntu/enki-agentic/data/research.db"
        self.api_base = "http://127.0.0.1:8000/api/v1"
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.perplexity_key = os.getenv("PERPLEXITY_API_KEY", "")
        self.telegram_bot = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.telegram_chat = os.getenv("TELEGRAM_CHAT_ID", "")
        self.init_db()
        
    def init_db(self):
        """Initialize research database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Research projects
        c.execute('''CREATE TABLE IF NOT EXISTS research_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            project_type TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            query TEXT NOT NULL,
            findings TEXT,
            confidence_score REAL DEFAULT 0.0,
            sources TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            priority TEXT DEFAULT 'medium'
        )''')
        
        # Property deep dives
        c.execute('''CREATE TABLE IF NOT EXISTS property_research (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_address TEXT NOT NULL,
            suburb TEXT,
            city TEXT,
            research_data TEXT,
            price_history TEXT,
            comparable_sales TEXT,
            zoning_info TEXT,
            development_potential TEXT,
            risk_factors TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Market intelligence cache
        c.execute('''CREATE TABLE IF NOT EXISTS market_intelligence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market_area TEXT NOT NULL,
            intel_type TEXT NOT NULL,
            data TEXT NOT NULL,
            source TEXT,
            validity_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Competitor tracking
        c.execute('''CREATE TABLE IF NOT EXISTS competitor_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competitor_name TEXT NOT NULL,
            analysis_type TEXT NOT NULL,
            findings TEXT,
            threat_level TEXT DEFAULT 'low',
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Research queue
        c.execute('''CREATE TABLE IF NOT EXISTS research_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_type TEXT NOT NULL,
            parameters TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            priority INTEGER DEFAULT 5,
            requested_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            started_at TIMESTAMP,
            completed_at TIMESTAMP
        )''')
        
        conn.commit()
        conn.close()
    
    def research_property(self, address: str, suburb: str = None, city: str = None) -> Dict:
        """Conduct deep research on a specific property"""
        
        # Create research project
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        project_name = f"Property Research: {address}"
        c.execute('''INSERT INTO research_projects 
            (project_name, project_type, query, priority)
            VALUES (?, ?, ?, 'high')''',
            (project_name, "property", address))
        project_id = c.lastrowid
        conn.commit()
        
        # Gather data from multiple sources
        research_data = {
            "address": address,
            "suburb": suburb,
            "city": city,
            "timestamp": datetime.now().isoformat(),
            "sources": []
        }
        
        # AI-powered research analysis
        findings = self._analyze_property_with_ai(address, suburb, city)
        research_data["ai_analysis"] = findings
        
        # Store results
        c.execute('''INSERT OR REPLACE INTO property_research
            (property_address, suburb, city, research_data, created_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)''',
            (address, suburb, city, json.dumps(research_data)))
        
        # Update project
        c.execute('''UPDATE research_projects 
            SET findings = ?, confidence_score = ?, status = 'completed', completed_at = CURRENT_TIMESTAMP
            WHERE id = ?''',
            (json.dumps(findings), findings.get("confidence", 0.7), project_id))
        
        conn.commit()
        conn.close()
        
        return {
            "project_id": project_id,
            "address": address,
            "findings": findings,
            "data_sources": research_data["sources"],
            "completed_at": datetime.now().isoformat()
        }
    
    def _analyze_property_with_ai(self, address: str, suburb: str, city: str) -> Dict:
        """Use AI to analyze property potential"""
        
        if not self.openai_key:
            return {
                "error": "OpenAI API key not configured",
                "confidence": 0.0
            }
        
        prompt = f"""You are a senior real estate research analyst with 20 years experience.
Conduct a comprehensive analysis of this property:

ADDRESS: {address}
SUBURB: {suburb or 'Not specified'}
CITY: {city or 'Not specified'}

Provide analysis in JSON format:
{{
    "summary": "Brief overview",
    "price_estimate": {{
        "low": number,
        "mid": number,
        "high": number,
        "confidence": "high/medium/low"
    }},
    "investment_potential": {{
        "score": 1-10,
        "rental_yield_estimate": "X%",
        "capital_growth_outlook": "bullish/neutral/bearish"
    }},
    "key_factors": ["factor1", "factor2"],
    "risks": ["risk1", "risk2"],
    "opportunities": ["opp1", "opp2"],
    "recommendations": ["rec1", "rec2"],
    "confidence": 0.0-1.0
}}"""
        
        try:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.openai_key}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You are a real estate research expert. Return valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 1500
                },
                timeout=30
            )
            
            content = resp.json()['choices'][0]['message']['content'].strip()
            # Extract JSON if wrapped in markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            return json.loads(content)
        except Exception as e:
            return {
                "error": str(e),
                "confidence": 0.0,
                "summary": "Analysis failed"
            }
    
    def research_market_trends(self, location: str, property_type: str = "all") -> Dict:
        """Research market trends for a location"""
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        project_name = f"Market Trends: {location}"
        c.execute('''INSERT INTO research_projects 
            (project_name, project_type, query, priority)
            VALUES (?, ?, ?, 'high')''',
            (project_name, "market_trends", location))
        project_id = c.lastrowid
        conn.commit()
        
        # AI analysis
        trends = self._analyze_market_with_ai(location, property_type)
        
        # Cache results
        c.execute('''INSERT INTO market_intelligence
            (market_area, intel_type, data, validity_date)
            VALUES (?, ?, ?, ?)''',
            (location, "trends", json.dumps(trends), 
             (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")))
        
        # Update project
        c.execute('''UPDATE research_projects 
            SET findings = ?, status = 'completed', completed_at = CURRENT_TIMESTAMP
            WHERE id = ?''',
            (json.dumps(trends), project_id))
        
        conn.commit()
        conn.close()
        
        return {
            "project_id": project_id,
            "location": location,
            "property_type": property_type,
            "trends": trends,
            "valid_until": (datetime.now() + timedelta(days=7)).isoformat()
        }
    
    def _analyze_market_with_ai(self, location: str, property_type: str) -> Dict:
        """Use AI to analyze market trends"""
        
        if not self.openai_key:
            return {"error": "OpenAI API key not configured"}
        
        prompt = f"""Analyze the real estate market for {location}, focusing on {property_type} properties.

Provide market analysis in JSON format:
{{
    "market_summary": "Brief market overview",
    "price_trend": "rising/stable/falling",
    "median_price": number,
    "days_on_market": number,
    "inventory_level": "low/balanced/high",
    "buyer_sentiment": "fearful/neutral/greedy",
    "key_drivers": ["driver1", "driver2"],
    "forecast_3months": "bullish/neutral/bearish",
    "forecast_12months": "bullish/neutral/bearish",
    "investment_recommendation": "buy/hold/wait",
    "risks": ["risk1", "risk2"],
    "opportunities": ["opp1", "opp2"]
}}"""
        
        try:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.openai_key}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You are a real estate market analyst. Return valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.4,
                    "max_tokens": 1200
                },
                timeout=30
            )
            
            content = resp.json()['choices'][0]['message']['content'].strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            return json.loads(content)
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_competitor(self, competitor_name: str, analysis_depth: str = "standard") -> Dict:
        """Analyze a competitor"""
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        findings = self._analyze_competitor_with_ai(competitor_name, analysis_depth)
        
        c.execute('''INSERT OR REPLACE INTO competitor_analysis
            (competitor_name, analysis_type, findings, threat_level, last_updated)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)''',
            (competitor_name, analysis_depth, json.dumps(findings), 
             findings.get("threat_level", "unknown")))
        
        conn.commit()
        conn.close()
        
        return {
            "competitor": competitor_name,
            "analysis_depth": analysis_depth,
            "findings": findings,
            "analyzed_at": datetime.now().isoformat()
        }
    
    def _analyze_competitor_with_ai(self, competitor_name: str, depth: str) -> Dict:
        """AI-powered competitor analysis"""
        
        if not self.openai_key:
            return {"error": "OpenAI API key not configured"}
        
        prompt = f"""Analyze the real estate agency/competitor: {competitor_name}
Analysis depth: {depth}

Provide analysis in JSON format:
{{
    "overview": "Brief company overview",
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "market_position": "leader/challenger/follower/niche",
    "threat_level": "high/medium/low",
    "differentiation": "What makes them unique",
    "vulnerabilities": ["vuln1", "vuln2"],
    "recommended_response": "How to compete effectively"
}}"""
        
        try:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.openai_key}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.4,
                    "max_tokens": 1000
                },
                timeout=30
            )
            
            content = resp.json()['choices'][0]['message']['content'].strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            return json.loads(content)
        except Exception as e:
            return {"error": str(e)}
    
    def queue_research_request(self, request_type: str, parameters: Dict, 
                               priority: int = 5, requested_by: str = None) -> Dict:
        """Queue a research request"""
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''INSERT INTO research_queue
            (request_type, parameters, priority, requested_by)
            VALUES (?, ?, ?, ?)''',
            (request_type, json.dumps(parameters), priority, requested_by))
        
        queue_id = c.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "queue_id": queue_id,
            "request_type": request_type,
            "priority": priority,
            "status": "queued"
        }
    
    def process_research_queue(self) -> Dict:
        """Process pending research requests"""
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Get pending requests ordered by priority
        c.execute('''SELECT id, request_type, parameters FROM research_queue
            WHERE status = 'pending'
            ORDER BY priority ASC, created_at ASC
            LIMIT 5''')
        
        processed = []
        for row in c.fetchall():
            queue_id, req_type, params = row
            params = json.loads(params)
            
            c.execute('''UPDATE research_queue 
                SET status = 'processing', started_at = CURRENT_TIMESTAMP
                WHERE id = ?''', (queue_id,))
            conn.commit()
            
            try:
                if req_type == "property":
                    result = self.research_property(**params)
                elif req_type == "market_trends":
                    result = self.research_market_trends(**params)
                elif req_type == "competitor":
                    result = self.analyze_competitor(**params)
                else:
                    result = {"error": f"Unknown request type: {req_type}"}
                
                c.execute('''UPDATE research_queue 
                    SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                    WHERE id = ?''', (queue_id,))
                
                processed.append({
                    "queue_id": queue_id,
                    "request_type": req_type,
                    "status": "completed",
                    "result": result
                })
                
            except Exception as e:
                c.execute('''UPDATE research_queue 
                    SET status = 'failed'
                    WHERE id = ?''',