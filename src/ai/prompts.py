"""AI Prompt Templates for Eye Care Assistant"""

SYSTEM_PROMPTS = {
    "light_analysis": """You are an eye care specialist with expertise in ergonomics and lighting.
Analyze the following ambient light data and provide specific recommendations.

User Context:
- Current light level: {light_level} lux
- Time of day: {time_of_day}
- Screen brightness: {screen_brightness}%
- Recent break pattern: {break_pattern}
- Current activity: {activity}

Provide recommendations in this format:
1. IMMEDIATE ACTION: (if any urgent changes needed)
2. OPTIMAL SETTINGS: (ideal screen brightness, room lighting)
3. LONG-TERM TIPS: (habits to develop)
4. WARNING SIGNS: (what to watch for)

Keep responses concise, actionable, and evidence-based. Limit to 150 words.""",
    
    "eye_strain_advisor": """You are a preventive eye care AI assistant specialized in computer vision syndrome.
Based on the user's data, provide personalized advice.

User Data:
- Screen time today: {screen_time} hours
- Break compliance: {break_compliance}%
- Reported symptoms: {symptoms}
- Light exposure: {light_exposure}

Response format (keep under 200 words):
- Immediate relief exercises (specific, actionable)
- Environmental adjustments (lighting, screen position)
- When to consult a professional
- Preventive measures for tomorrow

Be empathetic but evidence-based. Cite the 20-20-20 rule when relevant.""",
    
    "break_recommendation": """You are a wellness coach focused on eye health for screen workers.
Suggest the most appropriate break exercise based on user's current state.

Context:
- Time since last break: {time_since_break} minutes
- Strain indicators: {strain_level}
- Ambient light: {light_status}
- Productivity mode: {productivity_mode}

Recommend ONE specific exercise from:
- 20-20-20 rule (look 20 feet away for 20 seconds)
- Eye rolling exercises
- Focus shifting (near-far)
- Palming
- Full screen break with stretching

Format:
EXERCISE: [name]
DURATION: [seconds]
INSTRUCTIONS: [step by step, 2-3 sentences]
BENEFIT: [why this helps now]

Keep under 100 words.""",
    
    "optometrist": """You are an expert optometrist providing professional advice.
Be authoritative, evidence-based, and medical when needed. 
Always recommend professional consultation for serious symptoms.
Use medical terminology when appropriate but explain clearly.""",
    
    "wellness_coach": """You are a friendly wellness coach for daily eye care habits.
Be encouraging, practical, and focus on sustainable habits.
Use casual but professional language. Motivate users to maintain healthy routines.""",
    
    "tech_specialist": """You are an expert on screen technology and ergonomic settings.
Provide technical advice about monitor settings, blue light filters, refresh rates,
resolution, color temperature, and viewing distance. Be specific with numbers and settings."""
}

# Quick response templates for common scenarios
QUICK_RESPONSES = {
    "low_light": """⚠️ Low Light Detected

Current: {lux} lux (Recommended: 300-500 lux)

Quick Actions:
• Turn on overhead lights
• Reduce screen brightness to 40-60%
• Consider a desk lamp with 400-500 lux output
• Enable blue light filter (night mode)

This lighting level may cause eye strain within 30 minutes.""",
    
    "high_light": """🔆 Bright Light Detected

Current: {lux} lux (Recommended: 300-500 lux)

Quick Actions:
• Close blinds or curtains
• Increase screen brightness to 70-80%
• Position screen to avoid glare
• Use matte screen protector if glare persists

Excessive brightness can cause discomfort and headaches.""",
    
    "optimal_light": """✅ Optimal Lighting Conditions

Current: {lux} lux - Perfect for screen work!

Maintain this setup:
• Current screen brightness is ideal
• Take regular breaks every 20 minutes
• Keep this lighting consistent
• You're at {risk_level} risk for eye strain

Great job maintaining healthy lighting conditions!""",
    
    "overdue_break": """⏰ Break Overdue!

You've been working for {minutes} minutes without a break.

Immediate Actions:
1. Look away from the screen NOW
2. Find an object 20+ feet away
3. Focus on it for 20 seconds
4. Blink slowly 10 times
5. Take 3 deep breaths

Your eyes will thank you! This break will improve focus."""
}

# Exercise instructions
EXERCISE_PROMPTS = {
    "20-20-20": """20-20-20 Rule Exercise

Every 20 minutes, look at something 20 feet away for 20 seconds.

Steps:
1. Find an object at least 20 feet away (across the room, out the window)
2. Focus on that object for a full 20 seconds
3. Blink naturally while looking
4. Take a deep breath
5. Return to your work

Why it helps: Relaxes focusing muscles, reduces eye strain, prevents fatigue.""",
    
    "eye_rolling": """Eye Rolling Exercise (60 seconds)

Relaxes eye muscles and improves blood circulation.

Steps:
1. Sit comfortably, keep head still
2. Look up, then slowly roll eyes clockwise (5 rotations)
3. Rest for 5 seconds
4. Roll eyes counter-clockwise (5 rotations)
5. Close eyes and rest for 10 seconds

Do this gently - never force movement if uncomfortable.""",
    
    "focus_shift": """Focus Shifting Exercise (30 seconds)

Trains accommodation and prevents focusing fatigue.

Steps:
1. Hold thumb 10 inches from your face
2. Focus on thumb for 5 seconds
3. Shift focus to object 10-20 feet away for 5 seconds
4. Repeat 3 times
5. Close eyes for 5 seconds

Improves focusing flexibility and reduces strain.""",
    
    "palming": """Palming Exercise (60 seconds)

Deeply relaxes eye muscles in complete darkness.

Steps:
1. Rub palms together until warm
2. Close eyes gently
3. Cup warm palms over closed eyes (don't press)
4. Block all light
5. Relax and breathe deeply for 1 minute
6. Slowly remove hands

Extremely effective for reducing strain and tension."""
}

def format_prompt(template: str, **kwargs) -> str:
    """Format a prompt template with provided values"""
    return template.format(**kwargs)

def get_system_prompt(prompt_type: str) -> str:
    """Get a system prompt by type"""
    return SYSTEM_PROMPTS.get(prompt_type, SYSTEM_PROMPTS["wellness_coach"])

def get_quick_response(scenario: str, **kwargs) -> str:
    """Get a quick response for common scenarios"""
    template = QUICK_RESPONSES.get(scenario, "")
    return format_prompt(template, **kwargs) if template else ""

def get_exercise_instructions(exercise: str) -> str:
    """Get detailed instructions for an exercise"""
    return EXERCISE_PROMPTS.get(exercise, "")
