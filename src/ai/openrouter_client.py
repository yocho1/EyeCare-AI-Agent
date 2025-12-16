"""OpenRouter API Client for AI Integration"""
import os
import json
import logging
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import asyncio

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

from .prompts import SYSTEM_PROMPTS, get_quick_response


class AIModel(Enum):
    """Available AI models"""
    LLAMA_3_1 = "meta-llama/llama-3.1-8b-instruct"
    CLAUDE_3_5 = "anthropic/claude-3.5-sonnet"
    GPT_4_O = "openai/gpt-4o"
    MIXTRAL = "mistralai/mixtral-8x7b-instruct"
    GPT_4_O_MINI = "openai/gpt-4o-mini"


@dataclass
class AIResponse:
    """Structured AI response"""
    recommendation: str
    confidence: float
    action_items: List[str]
    warning_level: str  # "low", "medium", "high"
    timestamp: datetime
    cached: bool = False


class OpenRouterClient:
    """Professional OpenRouter API client with error handling and caching"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = None):
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = model or os.getenv("OPENROUTER_MODEL", AIModel.LLAMA_3_1.value)
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://eyecare-agent.com",
            "X-Title": "EyeCare AI Agent",
            "Content-Type": "application/json"
        }
        
        # Cache for responses
        self.cache: Dict[str, tuple[AIResponse, datetime]] = {}
        self.cache_duration = timedelta(minutes=30)
        
        # Check if API is available
        self.enabled = bool(self.api_key) and HTTPX_AVAILABLE
        
        if not self.enabled:
            if not self.api_key:
                self.logger.warning("OpenRouter API key not found. AI features will use fallback responses.")
            if not HTTPX_AVAILABLE:
                self.logger.warning("httpx not available. Install with: pip install httpx")
        else:
            self.logger.info(f"OpenRouter client initialized with model: {self.model}")
    
    async def get_light_recommendation(self, 
                                      light_data: Dict,
                                      user_context: Dict) -> AIResponse:
        """Get AI-powered lighting recommendations"""
        
        # Create cache key
        lux = light_data.get('lux', 0)
        cache_key = f"light_{int(lux/50)*50}"  # Round to nearest 50 lux
        
        # Check cache
        if cache_key in self.cache:
            cached_response, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_duration:
                self.logger.debug(f"Using cached response for {cache_key}")
                cached_response.cached = True
                return cached_response
        
        # If AI not available, use rule-based fallback
        if not self.enabled:
            return self._get_fallback_recommendation(light_data, user_context)
        
        # Build prompt
        prompt = self._build_light_prompt(light_data, user_context)
        
        try:
            response = await self._make_request(
                system_prompt=SYSTEM_PROMPTS["light_analysis"],
                user_prompt=prompt,
                temperature=0.3,
                max_tokens=500
            )
            
            if response:
                ai_response = self._parse_ai_response(response, light_data)
                self.cache[cache_key] = (ai_response, datetime.now())
                return ai_response
            else:
                return self._get_fallback_recommendation(light_data, user_context)
                
        except Exception as e:
            self.logger.error(f"Error getting AI recommendation: {e}")
            return self._get_fallback_recommendation(light_data, user_context)
    
    async def get_eye_strain_advice(self,
                                   screen_time: float,
                                   break_compliance: float,
                                   symptoms: List[str]) -> AIResponse:
        """Get personalized eye strain advice"""
        
        cache_key = f"strain_{int(screen_time)}_{int(break_compliance)}"
        
        if cache_key in self.cache:
            cached_response, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_duration:
                cached_response.cached = True
                return cached_response
        
        if not self.enabled:
            return self._get_fallback_strain_advice(screen_time, break_compliance, symptoms)
        
        prompt = f"""
User Status:
- Screen time today: {screen_time:.1f} hours
- Break compliance: {break_compliance:.0f}%
- Symptoms: {', '.join(symptoms) if symptoms else 'None reported'}
- Light exposure: Varying throughout day

Please provide concise, actionable advice.
"""
        
        try:
            response = await self._make_request(
                system_prompt=SYSTEM_PROMPTS["eye_strain_advisor"],
                user_prompt=prompt,
                temperature=0.4,
                max_tokens=400
            )
            
            if response:
                ai_response = self._parse_strain_response(response, screen_time, break_compliance)
                self.cache[cache_key] = (ai_response, datetime.now())
                return ai_response
            else:
                return self._get_fallback_strain_advice(screen_time, break_compliance, symptoms)
                
        except Exception as e:
            self.logger.error(f"Error getting strain advice: {e}")
            return self._get_fallback_strain_advice(screen_time, break_compliance, symptoms)
    
    async def get_break_recommendation(self,
                                      time_since_break: int,
                                      strain_level: str,
                                      light_status: str) -> str:
        """Get recommended break exercise"""
        
        if not self.enabled:
            return self._get_fallback_exercise(time_since_break, strain_level)
        
        prompt = f"""
Current state:
- Minutes since last break: {time_since_break}
- Strain level: {strain_level}
- Light conditions: {light_status}

Recommend the BEST exercise for this moment.
"""
        
        try:
            response = await self._make_request(
                system_prompt=SYSTEM_PROMPTS["break_recommendation"],
                user_prompt=prompt,
                temperature=0.5,
                max_tokens=200
            )
            
            return response if response else self._get_fallback_exercise(time_since_break, strain_level)
            
        except Exception as e:
            self.logger.error(f"Error getting break recommendation: {e}")
            return self._get_fallback_exercise(time_since_break, strain_level)
    
    async def _make_request(self,
                           system_prompt: str,
                           user_prompt: str,
                           temperature: float = 0.3,
                           max_tokens: int = 500) -> Optional[str]:
        """Make request to OpenRouter API"""
        
        if not HTTPX_AVAILABLE:
            return None
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data['choices'][0]['message']['content']
                else:
                    self.logger.error(f"API error: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Request failed: {e}")
            return None
    
    def _build_light_prompt(self, light_data: Dict, user_context: Dict) -> str:
        """Build prompt for light analysis"""
        return f"""
Current Conditions:
- Light level: {light_data.get('lux', 0):.0f} lux
- Status: {light_data.get('status', 'unknown')}
- Time: {datetime.now().strftime('%I:%M %p')}
- Screen brightness: {user_context.get('screen_brightness', 'auto')}%
- Recent breaks: {user_context.get('recent_breaks', 0)} in last hour
- Current activity: {user_context.get('activity', 'general computer work')}

Please analyze and provide specific recommendations.
"""
    
    def _parse_ai_response(self, text: str, light_data: Dict) -> AIResponse:
        """Parse AI response into structured format"""
        
        # Extract action items (lines starting with bullet points or numbers)
        action_items = []
        for line in text.split('\n'):
            line = line.strip()
            if line and (line[0] in ['•', '-', '*'] or (line[0].isdigit() and line[1] in ['.', ')'])):
                action_items.append(line.lstrip('•-*0123456789.) '))
        
        # Determine warning level based on light data
        lux = light_data.get('lux', 300)
        if lux < 100 or lux > 1000:
            warning_level = "high"
        elif lux < 200 or lux > 700:
            warning_level = "medium"
        else:
            warning_level = "low"
        
        return AIResponse(
            recommendation=text,
            confidence=0.85,
            action_items=action_items[:5],  # Top 5 actions
            warning_level=warning_level,
            timestamp=datetime.now()
        )
    
    def _parse_strain_response(self, text: str, screen_time: float, break_compliance: float) -> AIResponse:
        """Parse eye strain advice response"""
        
        action_items = []
        for line in text.split('\n'):
            line = line.strip()
            if line and (line[0] in ['•', '-', '*'] or (line[0].isdigit() and line[1] in ['.', ')'])):
                action_items.append(line.lstrip('•-*0123456789.) '))
        
        # Determine warning level
        if screen_time > 8 or break_compliance < 50:
            warning_level = "high"
        elif screen_time > 6 or break_compliance < 70:
            warning_level = "medium"
        else:
            warning_level = "low"
        
        return AIResponse(
            recommendation=text,
            confidence=0.80,
            action_items=action_items[:5],
            warning_level=warning_level,
            timestamp=datetime.now()
        )
    
    def _get_fallback_recommendation(self, light_data: Dict, user_context: Dict) -> AIResponse:
        """Rule-based fallback recommendations"""
        
        lux = light_data.get('lux', 300)
        status = light_data.get('status', 'optimal')
        
        if status == 'very_low':
            text = get_quick_response('low_light', lux=lux)
            warning = "high"
        elif status == 'low':
            text = get_quick_response('low_light', lux=lux)
            warning = "medium"
        elif status == 'high':
            text = get_quick_response('high_light', lux=lux)
            warning = "medium"
        else:
            text = get_quick_response('optimal_light', lux=lux, risk_level="low")
            warning = "low"
        
        action_items = [
            line.strip().lstrip('•-* ') 
            for line in text.split('\n') 
            if line.strip() and line.strip()[0] in ['•', '-', '*']
        ]
        
        return AIResponse(
            recommendation=text,
            confidence=0.70,
            action_items=action_items,
            warning_level=warning,
            timestamp=datetime.now(),
            cached=False
        )
    
    def _get_fallback_strain_advice(self, screen_time: float, break_compliance: float, symptoms: List[str]) -> AIResponse:
        """Fallback eye strain advice"""
        
        advice = []
        warning = "low"
        
        if screen_time > 8:
            advice.append("Your screen time is very high (>8 hours). Consider taking longer breaks.")
            warning = "high"
        elif screen_time > 6:
            advice.append("Screen time is above recommended levels. Increase break frequency.")
            warning = "medium"
        
        if break_compliance < 50:
            advice.append("Break compliance is low. Try setting more frequent reminders.")
            warning = "high"
        elif break_compliance < 70:
            advice.append("Improve break compliance to reduce eye strain risk.")
        
        if symptoms:
            advice.append(f"You reported: {', '.join(symptoms)}. Consider consulting an eye care professional.")
            warning = "high"
        
        if not advice:
            advice.append("You're maintaining good eye care habits. Keep it up!")
        
        text = "\n\n".join(advice)
        
        return AIResponse(
            recommendation=text,
            confidence=0.75,
            action_items=advice,
            warning_level=warning,
            timestamp=datetime.now()
        )
    
    def _get_fallback_exercise(self, time_since_break: int, strain_level: str) -> str:
        """Fallback exercise recommendation"""
        
        from .prompts import get_exercise_instructions
        
        if time_since_break > 30 or strain_level == "high":
            return get_exercise_instructions("20-20-20")
        elif strain_level == "medium":
            return get_exercise_instructions("focus_shift")
        else:
            return get_exercise_instructions("eye_rolling")
    
    def clear_cache(self):
        """Clear response cache"""
        self.cache.clear()
        self.logger.info("AI response cache cleared")
