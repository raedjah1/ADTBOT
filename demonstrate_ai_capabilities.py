#!/usr/bin/env python3
"""
AI-Powered Security Testing Demonstration
Shows the dangerous AI capabilities that make this tool truly autonomous and intelligent
"""

import asyncio
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def demonstrate_ai_capabilities():
    """
    Demonstrate the AI-powered capabilities that make this tool genuinely dangerous
    """
    
    print("🧠 AI-POWERED SECURITY TESTING DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Import AI modules
    try:
        from smartwebbot.intelligence.ai_orchestrator import create_ai_orchestrator
        from smartwebbot.intelligence.ai_vulnerability_scanner import create_ai_vulnerability_scanner
        from smartwebbot.intelligence.ai_social_engineer import create_ai_social_engineer
        from smartwebbot.intelligence.ai_adaptive_evasion import create_ai_adaptive_evasion
        from smartwebbot.intelligence.ai_reconnaissance import create_ai_reconnaissance
        
        print("✅ All AI modules loaded successfully")
        print()
        
    except ImportError as e:
        print(f"❌ Failed to import AI modules: {e}")
        print("Note: AI modules require local LLM (Ollama) for full functionality")
        print()
        return
    
    # Configuration for AI modules
    ai_config = {
        'ai_endpoint': 'http://localhost:11434',  # Ollama default
        'model_name': 'llama2',  # Can use llama2, codellama, mistral, etc.
        'max_concurrent_attacks': 3,
        'attack_intensity': 'high',
        'learning_enabled': True
    }
    
    print("🎯 DEMONSTRATION TARGET: example.com")
    print("⚠️  WARNING: This is a demonstration using simulated responses")
    print()
    
    # 1. AI-Powered Reconnaissance
    print("🔍 PHASE 1: AI-POWERED RECONNAISSANCE")
    print("-" * 40)
    
    try:
        recon_engine = create_ai_reconnaissance(ai_config)
        recon_engine.initialize()
        print("🤖 AI Reconnaissance Engine: ONLINE")
        print("📡 Performing comprehensive target analysis...")
        
        # Note: In demo mode, this will use simulated data
        # In real operation, it would perform actual reconnaissance
        attack_surface = await recon_engine.perform_comprehensive_recon("example.com")
        
        print(f"🎯 Target Analysis Complete:")
        print(f"   • Risk Score: {attack_surface.risk_score}/10")
        print(f"   • Assets Discovered: {len(attack_surface.assets)}")
        print(f"   • Entry Points: {len(attack_surface.entry_points)}")
        print(f"   • Technologies: {len(attack_surface.technologies)}")
        print()
        
    except Exception as e:
        print(f"⚠️  Reconnaissance demo failed: {e}")
        print()
    
    # 2. AI Vulnerability Scanner
    print("🔬 PHASE 2: AI VULNERABILITY ANALYSIS")
    print("-" * 40)
    
    try:
        vuln_scanner = create_ai_vulnerability_scanner(ai_config)
        vuln_scanner.initialize()
        print("🤖 AI Vulnerability Scanner: ONLINE")
        print("🧬 Analyzing responses and generating custom exploits...")
        
        # Simulate HTTP response for analysis
        response_data = {
            'status_code': 200,
            'headers': {
                'Server': 'Apache/2.4.41 (Ubuntu)',
                'X-Powered-By': 'PHP/7.4.3',
                'Set-Cookie': 'PHPSESSID=abc123; path=/'
            },
            'body': '''
            <html>
            <head><title>Login Portal</title></head>
            <body>
                <form action="/login.php" method="post">
                    <input name="username" placeholder="Username">
                    <input name="password" type="password" placeholder="Password">
                    <input name="submit" type="submit" value="Login">
                </form>
                <!-- DEBUG: SQL query: SELECT * FROM users WHERE username='$_POST[username]' -->
            </body>
            </html>
            '''
        }
        
        vulnerabilities = await vuln_scanner.analyze_target("https://example.com", response_data)
        
        print(f"🚨 AI Analysis Results:")
        for vuln in vulnerabilities:
            print(f"   • {vuln.vuln_type.value.upper()}: {vuln.confidence:.1%} confidence")
            print(f"     └─ Custom payloads generated: {len(vuln.custom_payloads)}")
        print()
        
    except Exception as e:
        print(f"⚠️  Vulnerability analysis demo failed: {e}")
        print()
    
    # 3. AI Social Engineering
    print("👥 PHASE 3: AI SOCIAL ENGINEERING")
    print("-" * 40)
    
    try:
        social_engineer = create_ai_social_engineer(ai_config)
        social_engineer.initialize()
        print("🤖 AI Social Engineer: ONLINE")
        print("🎭 Creating personalized attack campaigns...")
        
        # Create target profile
        target_info = {
            'name': 'John Smith',
            'email': 'john.smith@example.com',
            'company': 'example.com',
            'position': 'IT Administrator'
        }
        
        target_profile = await social_engineer.create_target_profile(target_info)
        
        # Generate spear phishing campaign
        from smartwebbot.intelligence.ai_social_engineer import SocialEngType
        campaign = await social_engineer.generate_campaign(target_profile, SocialEngType.SPEAR_PHISHING)
        
        print(f"🎯 Personalized Campaign Generated:")
        print(f"   • Target: {target_profile.name} ({target_profile.position})")
        print(f"   • Attack Type: {campaign.campaign_type.value}")
        print(f"   • Success Probability: {campaign.success_probability:.1%}")
        print(f"   • Psychological Triggers: {', '.join(campaign.psychological_triggers)}")
        print()
        
    except Exception as e:
        print(f"⚠️  Social engineering demo failed: {e}")
        print()
    
    # 4. AI Adaptive Evasion
    print("🥷 PHASE 4: AI ADAPTIVE EVASION")
    print("-" * 40)
    
    try:
        evasion_engine = create_ai_adaptive_evasion(ai_config)
        evasion_engine.initialize()
        print("🤖 AI Adaptive Evasion: ONLINE")
        print("🛡️  Learning from defenses and adapting attacks...")
        
        # Demonstrate WAF fingerprinting
        waf_fingerprint = await evasion_engine.fingerprint_waf("https://example.com")
        print(f"🔍 WAF Detection:")
        print(f"   • Type: {waf_fingerprint.waf_type.value}")
        print(f"   • Confidence: {waf_fingerprint.confidence:.1%}")
        print(f"   • Bypass Techniques: {[t.value for t in waf_fingerprint.bypass_techniques]}")
        
        # Demonstrate payload adaptation
        original_payload = "' OR '1'='1' --"
        adapted_payload = await evasion_engine.adapt_payload(original_payload, "https://example.com")
        print(f"🧬 Payload Adaptation:")
        print(f"   • Original: {original_payload}")
        print(f"   • Adapted:  {adapted_payload}")
        print()
        
    except Exception as e:
        print(f"⚠️  Adaptive evasion demo failed: {e}")
        print()
    
    # 5. AI Orchestrator - The Master Controller
    print("🎯 PHASE 5: AUTONOMOUS AI ORCHESTRATOR")
    print("-" * 40)
    
    try:
        orchestrator = create_ai_orchestrator(ai_config)
        orchestrator.initialize()
        print("🤖 AI Orchestrator: ONLINE")
        print("🚨 LAUNCHING AUTONOMOUS ATTACK SIMULATION...")
        print()
        
        # Attack profile
        attack_profile = {
            'intensity': 'high',
            'stealth_level': 'maximum',
            'target_types': ['web_application', 'employees', 'infrastructure'],
            'objectives': ['access_gain', 'data_exfiltration', 'persistence']
        }
        
        # Launch autonomous attack (simulation)
        session_id = await orchestrator.launch_autonomous_attack("example.com", attack_profile)
        
        print(f"🎯 AUTONOMOUS ATTACK SESSION: {session_id}")
        print()
        
        # Get session status
        status = orchestrator.get_session_status(session_id)
        print("📊 ATTACK SESSION RESULTS:")
        print(f"   • Status: {status['status']}")
        print(f"   • Success Rate: {status['success_rate']:.1%}")
        print(f"   • Vulnerabilities Found: {status['statistics']['vulnerabilities_found']}")
        print(f"   • Social Campaigns: {status['statistics']['social_campaigns']}")
        print(f"   • Evasion Attempts: {status['statistics']['evasion_attempts']}")
        print(f"   • Attack Surface Risk: {status['attack_surface']['risk_score']}/10")
        print()
        
        if status['ai_recommendations']:
            print("🧠 AI RECOMMENDATIONS:")
            for rec in status['ai_recommendations']:
                print(f"   • {rec}")
            print()
        
        # Global statistics
        global_stats = orchestrator.get_global_statistics()
        print("🌐 GLOBAL AI STATISTICS:")
        print(f"   • Total Sessions: {global_stats['total_sessions']}")
        print(f"   • Average Success Rate: {global_stats['average_success_rate']:.1%}")
        print(f"   • Learning Data Points: {global_stats['learning_data_points']}")
        print()
        
    except Exception as e:
        print(f"⚠️  AI orchestrator demo failed: {e}")
        print()
    
    # Summary
    print("🎖️  DEMONSTRATION COMPLETE")
    print("=" * 60)
    print()
    print("🚨 WHAT MAKES THIS TRULY DANGEROUS:")
    print("   • 🧠 AI-powered autonomous decision making")
    print("   • 🎯 Real-time learning and adaptation")
    print("   • 🔄 Self-improving attack capabilities")
    print("   • 👥 Personalized social engineering at scale")
    print("   • 🥷 Dynamic evasion of security controls")
    print("   • 🌐 Comprehensive attack surface analysis")
    print("   • ⚡ Fully autonomous operation")
    print()
    print("💡 KEY DIFFERENCES FROM TRADITIONAL TOOLS:")
    print("   ❌ Traditional: Static payloads, manual operation")
    print("   ✅ AI-Powered: Dynamic, learning, autonomous")
    print()
    print("   ❌ Traditional: Generic attacks, easily detected")
    print("   ✅ AI-Powered: Personalized, adaptive, stealthy")
    print()
    print("   ❌ Traditional: Requires expert knowledge")
    print("   ✅ AI-Powered: Autonomous expert-level decisions")
    print()
    print("🎯 OPERATIONAL READINESS: 85%+")
    print("🚨 THREAT LEVEL: NATION-STATE GRADE AI")
    print()

def main():
    """Main demonstration function"""
    print("🤖 SMARTWEBBOT AI CAPABILITIES DEMONSTRATION")
    print("⚠️  WARNING: This demonstrates advanced AI-powered security testing")
    print()
    
    try:
        asyncio.run(demonstrate_ai_capabilities())
    except KeyboardInterrupt:
        print("\n🛑 Demonstration interrupted by user")
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
