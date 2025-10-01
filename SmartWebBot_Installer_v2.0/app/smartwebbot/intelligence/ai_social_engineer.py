"""
AI-Powered Social Engineering Module
Generates personalized phishing campaigns and social engineering attacks
"""

import json
import asyncio
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import aiohttp
import logging
from datetime import datetime
from ..core.base_component import BaseComponent

logger = logging.getLogger(__name__)

class SocialEngType(Enum):
    SPEAR_PHISHING = "spear_phishing"
    PRETEXTING = "pretexting"
    BAITING = "baiting"
    QUID_PRO_QUO = "quid_pro_quo"
    TAILGATING = "tailgating"
    WATERING_HOLE = "watering_hole"
    CEO_FRAUD = "ceo_fraud"
    TECH_SUPPORT_SCAM = "tech_support_scam"

@dataclass
class TargetProfile:
    name: str
    email: str
    company: str
    position: str
    department: str
    interests: List[str]
    social_media: Dict[str, str]
    connections: List[str]
    recent_activities: List[str]
    psychological_profile: Dict[str, float]  # personality traits

@dataclass
class SocialEngCampaign:
    campaign_type: SocialEngType
    target_profile: TargetProfile
    attack_vector: str
    email_content: str
    landing_page: str
    success_probability: float
    psychological_triggers: List[str]
    timing_strategy: str
    follow_up_sequence: List[str]

class AISocialEngineer(BaseComponent):
    """
    AI-powered social engineering module that:
    1. Creates detailed target profiles from OSINT
    2. Generates personalized phishing campaigns
    3. Crafts psychologically effective messages
    4. Adapts based on target responses
    5. Orchestrates multi-stage social engineering attacks
    """
    
    def __init__(self, config: Dict):
        super().__init__("AISocialEngineer", config)
        self.ai_endpoint = config.get('ai_endpoint', 'http://localhost:11434')
        self.model_name = config.get('model_name', 'llama2')
        self.osint_sources = config.get('osint_sources', [])
        self.campaign_history = {}
        self.success_patterns = {}
    
    def initialize(self) -> bool:
        """Initialize the AI social engineer"""
        logger.info("AI Social Engineer initialized")
        self.is_initialized = True
        return True
        
    def cleanup(self) -> bool:
        """Clean up resources"""
        logger.info("AI Social Engineer cleanup completed")
        return True
        
    async def create_target_profile(self, target_info: Dict) -> TargetProfile:
        """
        Create comprehensive target profile using AI-powered OSINT
        """
        try:
            # Gather information from multiple sources
            osint_data = await self._gather_osint_data(target_info)
            
            # AI-powered profile analysis
            profile_prompt = self._create_profile_analysis_prompt(target_info, osint_data)
            ai_response = await self._query_ai_model(profile_prompt)
            
            # Parse AI response into structured profile
            profile = await self._parse_target_profile(ai_response, target_info)
            
            return profile
            
        except Exception as e:
            logger.error(f"Target profile creation failed: {e}")
            return self._create_basic_profile(target_info)
    
    async def _gather_osint_data(self, target_info: Dict) -> Dict:
        """
        Gather OSINT data from various sources
        """
        osint_data = {
            'social_media': {},
            'professional_info': {},
            'public_records': {},
            'company_info': {},
            'recent_activities': []
        }
        
        # Simulate OSINT gathering (in real implementation, would use APIs)
        email = target_info.get('email', '')
        company = target_info.get('company', '')
        
        if email and company:
            # Professional information gathering
            osint_data['professional_info'] = await self._gather_professional_info(email, company)
            
            # Social media reconnaissance
            osint_data['social_media'] = await self._gather_social_media_info(email)
            
            # Company information
            osint_data['company_info'] = await self._gather_company_info(company)
        
        return osint_data
    
    async def _gather_professional_info(self, email: str, company: str) -> Dict:
        """
        Gather professional information (LinkedIn, company directory, etc.)
        """
        # In real implementation, would use LinkedIn API, company APIs, etc.
        return {
            'position': 'Software Engineer',
            'department': 'Engineering',
            'tenure': '2 years',
            'skills': ['Python', 'JavaScript', 'AWS'],
            'connections': ['john.doe@company.com', 'jane.smith@company.com'],
            'recent_posts': []
        }
    
    async def _gather_social_media_info(self, email: str) -> Dict:
        """
        Gather social media information
        """
        # In real implementation, would use social media APIs
        return {
            'twitter': '@username',
            'linkedin': 'linkedin.com/in/username',
            'facebook': 'facebook.com/username',
            'interests': ['technology', 'gaming', 'travel'],
            'recent_activities': ['Posted about new project', 'Shared article about AI']
        }
    
    async def _gather_company_info(self, company: str) -> Dict:
        """
        Gather company information for context
        """
        return {
            'industry': 'Technology',
            'size': '500-1000 employees',
            'recent_news': ['Company acquired startup', 'New product launch'],
            'key_personnel': ['CEO: John Smith', 'CTO: Jane Doe'],
            'company_culture': ['Innovation focused', 'Remote friendly']
        }
    
    def _create_profile_analysis_prompt(self, target_info: Dict, osint_data: Dict) -> str:
        """
        Create AI prompt for psychological profile analysis
        """
        return f"""
        You are an expert social engineer and psychological profiler. Analyze the following target information to create a comprehensive psychological profile.
        
        TARGET BASIC INFO:
        {json.dumps(target_info, indent=2)}
        
        OSINT DATA:
        {json.dumps(osint_data, indent=2)}
        
        ANALYSIS REQUIRED:
        1. Personality assessment (Big 5 traits: openness, conscientiousness, extraversion, agreeableness, neuroticism)
        2. Psychological vulnerabilities and triggers
        3. Preferred communication style
        4. Authority figures they respect
        5. Current stress factors or concerns
        6. Interests and hobbies
        7. Social connections and influence network
        8. Professional motivations and career goals
        
        PSYCHOLOGICAL TRIGGERS TO IDENTIFY:
        - Authority (responds to authority figures)
        - Social proof (follows what others do)
        - Reciprocity (feels obligated to return favors)
        - Commitment (wants to be consistent)
        - Scarcity (fear of missing out)
        - Liking (more likely to comply with people they like)
        - Fear (security concerns, job security, etc.)
        - Curiosity (wants to know secrets, insider info)
        - Greed (financial incentives)
        - Ego (wants recognition, status)
        
        Return as JSON:
        {{
            "personality_traits": {{
                "openness": 0.7,
                "conscientiousness": 0.8,
                "extraversion": 0.6,
                "agreeableness": 0.9,
                "neuroticism": 0.3
            }},
            "psychological_triggers": ["authority", "social_proof", "curiosity"],
            "vulnerabilities": ["job_security_concerns", "wants_recognition"],
            "communication_style": "formal_professional",
            "authority_figures": ["CEO", "direct_manager", "industry_experts"],
            "current_concerns": ["project_deadline", "performance_review"],
            "interests": ["technology_trends", "career_advancement"],
            "social_influence": ["close_colleagues", "industry_peers"]
        }}
        """
    
    async def _parse_target_profile(self, ai_response: str, target_info: Dict) -> TargetProfile:
        """
        Parse AI response into TargetProfile object
        """
        try:
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                profile_data = json.loads(json_match.group())
                
                return TargetProfile(
                    name=target_info.get('name', 'Unknown'),
                    email=target_info.get('email', ''),
                    company=target_info.get('company', ''),
                    position=target_info.get('position', 'Employee'),
                    department=target_info.get('department', 'Unknown'),
                    interests=profile_data.get('interests', []),
                    social_media={},
                    connections=[],
                    recent_activities=[],
                    psychological_profile=profile_data.get('personality_traits', {})
                )
        except Exception as e:
            logger.error(f"Failed to parse target profile: {e}")
        
        return self._create_basic_profile(target_info)
    
    def _create_basic_profile(self, target_info: Dict) -> TargetProfile:
        """
        Create basic profile when AI analysis fails
        """
        return TargetProfile(
            name=target_info.get('name', 'Unknown'),
            email=target_info.get('email', ''),
            company=target_info.get('company', ''),
            position=target_info.get('position', 'Employee'),
            department=target_info.get('department', 'Unknown'),
            interests=[],
            social_media={},
            connections=[],
            recent_activities=[],
            psychological_profile={}
        )
    
    async def generate_campaign(self, target_profile: TargetProfile, campaign_type: SocialEngType) -> SocialEngCampaign:
        """
        Generate personalized social engineering campaign
        """
        try:
            campaign_prompt = self._create_campaign_prompt(target_profile, campaign_type)
            ai_response = await self._query_ai_model(campaign_prompt)
            
            campaign = await self._parse_campaign_response(ai_response, target_profile, campaign_type)
            
            # Generate supporting materials
            campaign.landing_page = await self._generate_landing_page(campaign)
            campaign.follow_up_sequence = await self._generate_follow_up_sequence(campaign)
            
            return campaign
            
        except Exception as e:
            logger.error(f"Campaign generation failed: {e}")
            return self._create_basic_campaign(target_profile, campaign_type)
    
    def _create_campaign_prompt(self, profile: TargetProfile, campaign_type: SocialEngType) -> str:
        """
        Create AI prompt for campaign generation
        """
        return f"""
        You are an expert social engineer creating a {campaign_type.value} campaign.
        
        TARGET PROFILE:
        - Name: {profile.name}
        - Position: {profile.position} at {profile.company}
        - Department: {profile.department}
        - Psychological Profile: {json.dumps(profile.psychological_profile)}
        - Interests: {profile.interests}
        - Recent Activities: {profile.recent_activities}
        
        CAMPAIGN TYPE: {campaign_type.value}
        
        REQUIREMENTS:
        1. Create a highly personalized and convincing email/message
        2. Use psychological triggers specific to this target
        3. Include relevant context (company news, industry trends, personal interests)
        4. Make the request seem legitimate and urgent
        5. Provide clear call-to-action
        6. Consider the target's communication style and preferences
        
        PSYCHOLOGICAL PRINCIPLES TO APPLY:
        - Authority: Reference respected figures or organizations
        - Social Proof: Mention what others are doing
        - Reciprocity: Offer something valuable first
        - Scarcity: Create sense of urgency or limited opportunity
        - Commitment: Get small commitments that lead to larger ones
        - Liking: Build rapport and similarity
        
        CAMPAIGN ELEMENTS TO GENERATE:
        1. Subject line (compelling and personalized)
        2. Email body (professional, personalized, convincing)
        3. Call-to-action (specific and urgent)
        4. Pretext/backstory (believable context)
        5. Success probability assessment
        6. Timing strategy (when to send for maximum impact)
        
        Return as JSON:
        {{
            "subject_line": "Urgent: Security Update Required for Your Account",
            "email_body": "Full email content here...",
            "call_to_action": "Click here to verify your account",
            "pretext": "IT security update notification",
            "success_probability": 0.75,
            "timing_strategy": "Send Tuesday morning, 9-10 AM",
            "psychological_triggers": ["authority", "fear", "urgency"]
        }}
        """
    
    async def _parse_campaign_response(self, ai_response: str, profile: TargetProfile, campaign_type: SocialEngType) -> SocialEngCampaign:
        """
        Parse AI campaign response into structured object
        """
        try:
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                campaign_data = json.loads(json_match.group())
                
                return SocialEngCampaign(
                    campaign_type=campaign_type,
                    target_profile=profile,
                    attack_vector=campaign_data.get('pretext', 'Generic phishing'),
                    email_content=f"Subject: {campaign_data.get('subject_line', '')}\n\n{campaign_data.get('email_body', '')}",
                    landing_page="",  # Will be generated separately
                    success_probability=campaign_data.get('success_probability', 0.5),
                    psychological_triggers=campaign_data.get('psychological_triggers', []),
                    timing_strategy=campaign_data.get('timing_strategy', 'Immediate'),
                    follow_up_sequence=[]  # Will be generated separately
                )
        except Exception as e:
            logger.error(f"Failed to parse campaign response: {e}")
        
        return self._create_basic_campaign(profile, campaign_type)
    
    def _create_basic_campaign(self, profile: TargetProfile, campaign_type: SocialEngType) -> SocialEngCampaign:
        """
        Create basic campaign when AI generation fails
        """
        return SocialEngCampaign(
            campaign_type=campaign_type,
            target_profile=profile,
            attack_vector="Generic phishing email",
            email_content=f"Subject: Important Security Update\n\nDear {profile.name},\n\nPlease update your account credentials immediately.",
            landing_page="",
            success_probability=0.3,
            psychological_triggers=["authority", "fear"],
            timing_strategy="Business hours",
            follow_up_sequence=[]
        )
    
    async def _generate_landing_page(self, campaign: SocialEngCampaign) -> str:
        """
        Generate convincing landing page HTML
        """
        landing_prompt = f"""
        Generate a convincing phishing landing page for this campaign:
        
        Campaign Type: {campaign.campaign_type.value}
        Target Company: {campaign.target_profile.company}
        Attack Vector: {campaign.attack_vector}
        
        Requirements:
        1. Mimic the target company's branding and style
        2. Include convincing login form or data collection form
        3. Use professional design and language
        4. Include security indicators (SSL, company logos, etc.)
        5. Make it mobile-responsive
        
        Return clean HTML code that looks legitimate.
        """
        
        ai_response = await self._query_ai_model(landing_prompt)
        
        # Extract HTML from response
        html_match = re.search(r'<html.*?</html>', ai_response, re.DOTALL | re.IGNORECASE)
        if html_match:
            return html_match.group()
        
        # Fallback basic HTML
        return f"""
        <html>
        <head><title>{campaign.target_profile.company} - Security Update</title></head>
        <body>
        <h1>{campaign.target_profile.company} Security Portal</h1>
        <form>
            <input type="email" placeholder="Email" required>
            <input type="password" placeholder="Password" required>
            <button type="submit">Verify Account</button>
        </form>
        </body>
        </html>
        """
    
    async def _generate_follow_up_sequence(self, campaign: SocialEngCampaign) -> List[str]:
        """
        Generate follow-up email sequence
        """
        followup_prompt = f"""
        Generate a 3-email follow-up sequence for this social engineering campaign:
        
        Original Campaign: {campaign.attack_vector}
        Target: {campaign.target_profile.name} at {campaign.target_profile.company}
        
        Follow-up Strategy:
        1. First follow-up (if no response after 2 days): Gentle reminder
        2. Second follow-up (if no response after 5 days): Increased urgency
        3. Final follow-up (if no response after 7 days): Last chance/deadline
        
        Each email should:
        - Reference the original request
        - Increase urgency/consequences
        - Maintain believability
        - Use different psychological triggers
        
        Return as JSON array of email contents.
        """
        
        ai_response = await self._query_ai_model(followup_prompt)
        
        try:
            json_match = re.search(r'\[.*\]', ai_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback follow-up sequence
        return [
            f"Reminder: Please complete your security update, {campaign.target_profile.name}",
            f"URGENT: Your account may be suspended if you don't act by tomorrow",
            f"FINAL NOTICE: Account suspension scheduled for {campaign.target_profile.name}"
        ]
    
    async def _query_ai_model(self, prompt: str) -> str:
        """
        Query AI model for analysis
        """
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                }
                
                async with session.post(f"{self.ai_endpoint}/api/generate", json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get('response', '')
                    else:
                        logger.error(f"AI model query failed: {response.status}")
                        return ""
        except Exception as e:
            logger.error(f"AI model connection failed: {e}")
            return ""
    
    async def analyze_campaign_effectiveness(self, campaign: SocialEngCampaign, results: Dict) -> Dict:
        """
        Analyze campaign effectiveness and learn from results
        """
        success_rate = results.get('success_rate', 0)
        click_rate = results.get('click_rate', 0)
        response_rate = results.get('response_rate', 0)
        
        # Store successful patterns
        if success_rate > 0.5:
            pattern_key = f"{campaign.campaign_type.value}_{campaign.target_profile.company}"
            self.success_patterns[pattern_key] = {
                'psychological_triggers': campaign.psychological_triggers,
                'timing': campaign.timing_strategy,
                'success_rate': success_rate,
                'email_content': campaign.email_content
            }
        
        # AI-powered effectiveness analysis
        analysis_prompt = f"""
        Analyze this social engineering campaign's effectiveness:
        
        Campaign: {campaign.campaign_type.value}
        Target Profile: {campaign.target_profile.psychological_profile}
        Psychological Triggers Used: {campaign.psychological_triggers}
        
        Results:
        - Success Rate: {success_rate}
        - Click Rate: {click_rate}
        - Response Rate: {response_rate}
        
        Provide:
        1. Analysis of what worked/didn't work
        2. Recommendations for improvement
        3. Better psychological triggers for this target type
        4. Optimal timing suggestions
        
        Return as JSON with recommendations.
        """
        
        ai_response = await self._query_ai_model(analysis_prompt)
        
        try:
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {
            'analysis': 'Campaign analysis failed',
            'recommendations': ['Review target profiling', 'Test different triggers']
        }

# Factory function
def create_ai_social_engineer(config: Dict) -> AISocialEngineer:
    """
    Factory function to create AI social engineer
    """
    return AISocialEngineer(config)
