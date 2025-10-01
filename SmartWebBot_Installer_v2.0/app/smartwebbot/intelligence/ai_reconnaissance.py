"""
AI-Powered Intelligent Reconnaissance Module
Analyzes targets and automatically discovers attack surfaces using AI
"""

import json
import re
import asyncio
import socket
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import aiohttp
import dns.resolver
import ssl
import logging
from datetime import datetime
from urllib.parse import urlparse, urljoin
from ..core.base_component import BaseComponent

logger = logging.getLogger(__name__)

class ReconType(Enum):
    PASSIVE = "passive"
    ACTIVE = "active"
    OSINT = "osint"
    TECHNICAL = "technical"

class AssetType(Enum):
    DOMAIN = "domain"
    SUBDOMAIN = "subdomain"
    IP_ADDRESS = "ip_address"
    PORT = "port"
    SERVICE = "service"
    TECHNOLOGY = "technology"
    ENDPOINT = "endpoint"
    PARAMETER = "parameter"
    CREDENTIAL = "credential"
    EMAIL = "email"
    SOCIAL_MEDIA = "social_media"

@dataclass
class ReconAsset:
    asset_type: AssetType
    value: str
    source: str
    confidence: float
    metadata: Dict = field(default_factory=dict)
    discovered_at: datetime = field(default_factory=datetime.now)
    verified: bool = False

@dataclass
class AttackSurface:
    target: str
    assets: List[ReconAsset]
    technologies: Dict[str, str]
    vulnerabilities: List[str]
    entry_points: List[str]
    risk_score: float
    ai_analysis: str

class AIReconnaissance(BaseComponent):
    """
    AI-powered reconnaissance engine that:
    1. Performs comprehensive target analysis
    2. Discovers hidden assets and endpoints
    3. Identifies technologies and vulnerabilities
    4. Maps attack surfaces intelligently
    5. Prioritizes targets based on AI risk assessment
    """
    
    def __init__(self, config: Dict):
        super().__init__("AIReconnaissance", config)
        self.ai_endpoint = config.get('ai_endpoint', 'http://localhost:11434')
        self.model_name = config.get('model_name', 'llama2')
        
        # Discovery databases
        self.discovered_assets: Dict[str, List[ReconAsset]] = {}
        self.attack_surfaces: Dict[str, AttackSurface] = {}
        
        # Common wordlists for discovery
        self.subdomain_wordlist = self._load_subdomain_wordlist()
        self.directory_wordlist = self._load_directory_wordlist()
        self.parameter_wordlist = self._load_parameter_wordlist()
        
        # Rate limiting
        self.request_semaphore = asyncio.Semaphore(10)
        self.request_delay = 0.1
    
    def initialize(self) -> bool:
        """Initialize the AI reconnaissance engine"""
        logger.info("AI Reconnaissance Engine initialized")
        self.is_initialized = True
        return True
        
    def cleanup(self) -> bool:
        """Clean up resources"""
        logger.info("AI Reconnaissance Engine cleanup completed")
        return True
        
    def _load_subdomain_wordlist(self) -> List[str]:
        """Load common subdomain names"""
        return [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
            'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'mx', 'test', 'dev',
            'staging', 'admin', 'api', 'cdn', 'blog', 'shop', 'store', 'mobile', 'app',
            'portal', 'secure', 'vpn', 'remote', 'support', 'help', 'docs', 'wiki',
            'beta', 'demo', 'preview', 'git', 'svn', 'jenkins', 'ci', 'build'
        ]
    
    def _load_directory_wordlist(self) -> List[str]:
        """Load common directory names"""
        return [
            'admin', 'administrator', 'login', 'panel', 'control', 'cp', 'wp-admin',
            'phpmyadmin', 'mysql', 'sql', 'database', 'db', 'backup', 'backups',
            'api', 'v1', 'v2', 'rest', 'graphql', 'swagger', 'docs', 'documentation',
            'test', 'testing', 'dev', 'development', 'staging', 'prod', 'production',
            'config', 'configuration', 'settings', 'uploads', 'files', 'assets',
            'static', 'public', 'private', 'secure', 'protected', 'hidden'
        ]
    
    def _load_parameter_wordlist(self) -> List[str]:
        """Load common parameter names"""
        return [
            'id', 'user', 'username', 'email', 'password', 'pass', 'token', 'key',
            'api_key', 'access_token', 'session', 'cookie', 'auth', 'login',
            'page', 'file', 'path', 'url', 'redirect', 'return', 'callback',
            'search', 'query', 'q', 'term', 'keyword', 'filter', 'sort', 'order',
            'limit', 'offset', 'page_size', 'count', 'format', 'type', 'action'
        ]
    
    async def perform_comprehensive_recon(self, target: str) -> AttackSurface:
        """
        Perform comprehensive AI-powered reconnaissance
        """
        try:
            logger.info(f"Starting comprehensive reconnaissance for: {target}")
            
            # Initialize asset collection
            assets = []
            
            # Phase 1: Passive reconnaissance
            passive_assets = await self._passive_reconnaissance(target)
            assets.extend(passive_assets)
            
            # Phase 2: Active reconnaissance
            active_assets = await self._active_reconnaissance(target)
            assets.extend(active_assets)
            
            # Phase 3: Technology fingerprinting
            tech_assets = await self._technology_fingerprinting(target)
            assets.extend(tech_assets)
            
            # Phase 4: Endpoint discovery
            endpoint_assets = await self._endpoint_discovery(target)
            assets.extend(endpoint_assets)
            
            # Phase 5: AI-powered analysis
            attack_surface = await self._ai_attack_surface_analysis(target, assets)
            
            # Store results
            self.discovered_assets[target] = assets
            self.attack_surfaces[target] = attack_surface
            
            logger.info(f"Reconnaissance complete. Discovered {len(assets)} assets.")
            return attack_surface
            
        except Exception as e:
            logger.error(f"Comprehensive reconnaissance failed: {e}")
            return AttackSurface(target, [], {}, [], [], 0.0, "Analysis failed")
    
    async def _passive_reconnaissance(self, target: str) -> List[ReconAsset]:
        """
        Passive reconnaissance using DNS, WHOIS, certificates, etc.
        """
        assets = []
        
        try:
            # DNS enumeration
            dns_assets = await self._dns_enumeration(target)
            assets.extend(dns_assets)
            
            # Certificate transparency logs
            cert_assets = await self._certificate_transparency_search(target)
            assets.extend(cert_assets)
            
            # Search engine reconnaissance
            search_assets = await self._search_engine_recon(target)
            assets.extend(search_assets)
            
            # Social media and OSINT
            osint_assets = await self._osint_gathering(target)
            assets.extend(osint_assets)
            
        except Exception as e:
            logger.error(f"Passive reconnaissance failed: {e}")
        
        return assets
    
    async def _dns_enumeration(self, target: str) -> List[ReconAsset]:
        """
        Comprehensive DNS enumeration
        """
        assets = []
        
        try:
            # Basic DNS records
            record_types = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS', 'SOA']
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(target, record_type)
                    for answer in answers:
                        assets.append(ReconAsset(
                            asset_type=AssetType.DOMAIN,
                            value=str(answer),
                            source=f"DNS_{record_type}",
                            confidence=0.95,
                            metadata={'record_type': record_type}
                        ))
                except:
                    continue
            
            # Subdomain enumeration
            subdomain_assets = await self._subdomain_enumeration(target)
            assets.extend(subdomain_assets)
            
        except Exception as e:
            logger.error(f"DNS enumeration failed: {e}")
        
        return assets
    
    async def _subdomain_enumeration(self, target: str) -> List[ReconAsset]:
        """
        AI-enhanced subdomain discovery
        """
        assets = []
        
        # Brute force common subdomains
        for subdomain in self.subdomain_wordlist:
            try:
                full_domain = f"{subdomain}.{target}"
                
                # Try to resolve
                try:
                    answers = dns.resolver.resolve(full_domain, 'A')
                    for answer in answers:
                        assets.append(ReconAsset(
                            asset_type=AssetType.SUBDOMAIN,
                            value=full_domain,
                            source="Subdomain_Brute_Force",
                            confidence=0.9,
                            metadata={'ip': str(answer)}
                        ))
                except:
                    continue
                    
            except Exception as e:
                continue
        
        # AI-powered subdomain prediction
        ai_subdomains = await self._ai_subdomain_prediction(target, assets)
        assets.extend(ai_subdomains)
        
        return assets
    
    async def _ai_subdomain_prediction(self, target: str, discovered_subdomains: List[ReconAsset]) -> List[ReconAsset]:
        """
        Use AI to predict additional subdomains based on discovered patterns
        """
        if not discovered_subdomains:
            return []
        
        discovered_names = [asset.value.replace(f'.{target}', '') for asset in discovered_subdomains]
        
        prediction_prompt = f"""
        Analyze these discovered subdomains for {target} and predict additional likely subdomains:
        
        DISCOVERED SUBDOMAINS: {discovered_names}
        
        Based on the patterns, naming conventions, and common subdomain practices, predict 10 additional subdomains that are likely to exist.
        
        Consider:
        1. Naming patterns (dev/staging/prod, v1/v2/v3, etc.)
        2. Technology-specific subdomains (api, cdn, mail, etc.)
        3. Department/function-based names (hr, finance, support, etc.)
        4. Environment variations (test, beta, demo, etc.)
        5. Geographic variations (us, eu, asia, etc.)
        
        Return as JSON array of subdomain names (without the domain):
        ["predicted1", "predicted2", "predicted3", ...]
        """
        
        ai_response = await self._query_ai_model(prediction_prompt)
        
        try:
            json_match = re.search(r'\[.*\]', ai_response, re.DOTALL)
            if json_match:
                predicted_subdomains = json.loads(json_match.group())
                
                assets = []
                for subdomain in predicted_subdomains:
                    if isinstance(subdomain, str) and subdomain not in discovered_names:
                        assets.append(ReconAsset(
                            asset_type=AssetType.SUBDOMAIN,
                            value=f"{subdomain}.{target}",
                            source="AI_Prediction",
                            confidence=0.6,
                            metadata={'predicted': True}
                        ))
                
                return assets
        except Exception as e:
            logger.error(f"AI subdomain prediction failed: {e}")
        
        return []
    
    async def _certificate_transparency_search(self, target: str) -> List[ReconAsset]:
        """
        Search certificate transparency logs for subdomains
        """
        assets = []
        
        try:
            # Simulate CT log search (in real implementation, would use CT APIs)
            ct_url = f"https://crt.sh/?q=%.{target}&output=json"
            
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(ct_url) as response:
                        if response.status == 200:
                            ct_data = await response.json()
                            
                            for entry in ct_data[:50]:  # Limit results
                                name_value = entry.get('name_value', '')
                                for domain in name_value.split('\n'):
                                    domain = domain.strip()
                                    if domain and target in domain:
                                        assets.append(ReconAsset(
                                            asset_type=AssetType.SUBDOMAIN,
                                            value=domain,
                                            source="Certificate_Transparency",
                                            confidence=0.85,
                                            metadata={'cert_id': entry.get('id')}
                                        ))
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"Certificate transparency search failed: {e}")
        
        return assets
    
    async def _search_engine_recon(self, target: str) -> List[ReconAsset]:
        """
        AI-powered search engine reconnaissance
        """
        assets = []
        
        # Search queries for different types of information
        search_queries = [
            f'site:{target}',
            f'site:{target} filetype:pdf',
            f'site:{target} filetype:doc',
            f'site:{target} filetype:xls',
            f'site:{target} inurl:admin',
            f'site:{target} inurl:login',
            f'site:{target} inurl:api',
            f'"{target}" email',
            f'"{target}" contact',
        ]
        
        # AI analysis of search results
        search_analysis_prompt = f"""
        Analyze potential search engine results for reconnaissance of {target}.
        
        Based on common patterns, what types of sensitive information might be found through search engines?
        
        Consider:
        1. Exposed documents (PDF, DOC, XLS)
        2. Login pages and admin interfaces
        3. API endpoints and documentation
        4. Employee email addresses
        5. Configuration files
        6. Error pages revealing information
        7. Cached pages with sensitive data
        8. Social media profiles and mentions
        
        Return potential findings as JSON:
        {{
            "likely_findings": [
                {{"type": "email", "pattern": "firstname.lastname@{target}", "confidence": 0.8}},
                {{"type": "admin_panel", "pattern": "{target}/admin", "confidence": 0.7}}
            ]
        }}
        """
        
        ai_response = await self._query_ai_model(search_analysis_prompt)
        
        try:
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                
                for finding in analysis.get('likely_findings', []):
                    finding_type = finding.get('type', 'unknown')
                    pattern = finding.get('pattern', '')
                    confidence = finding.get('confidence', 0.5)
                    
                    if finding_type == 'email':
                        asset_type = AssetType.EMAIL
                    elif finding_type == 'admin_panel':
                        asset_type = AssetType.ENDPOINT
                    else:
                        asset_type = AssetType.ENDPOINT
                    
                    assets.append(ReconAsset(
                        asset_type=asset_type,
                        value=pattern,
                        source="Search_Engine_AI_Analysis",
                        confidence=confidence,
                        metadata={'search_type': finding_type}
                    ))
        except Exception as e:
            logger.error(f"Search engine analysis failed: {e}")
        
        return assets
    
    async def _osint_gathering(self, target: str) -> List[ReconAsset]:
        """
        AI-powered OSINT gathering
        """
        assets = []
        
        osint_prompt = f"""
        Perform OSINT analysis for {target}. Based on common patterns and public information sources, identify likely:
        
        1. Social media accounts and profiles
        2. Employee information and email patterns
        3. Technology stack indicators
        4. Business relationships and partnerships
        5. News and press releases
        6. Job postings revealing internal technologies
        7. Conference presentations and technical talks
        8. GitHub repositories and code
        9. Third-party services and integrations
        10. Contact information and office locations
        
        Return findings as JSON:
        {{
            "social_media": [
                {{"platform": "twitter", "handle": "@{target}", "confidence": 0.7}}
            ],
            "employees": [
                {{"name": "John Doe", "role": "CTO", "email": "john.doe@{target}", "confidence": 0.6}}
            ],
            "technologies": [
                {{"tech": "AWS", "evidence": "Job posting mentions AWS experience", "confidence": 0.8}}
            ],
            "integrations": [
                {{"service": "Salesforce", "evidence": "Privacy policy mentions Salesforce", "confidence": 0.7}}
            ]
        }}
        """
        
        ai_response = await self._query_ai_model(osint_prompt)
        
        try:
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                osint_data = json.loads(json_match.group())
                
                # Process social media findings
                for social in osint_data.get('social_media', []):
                    assets.append(ReconAsset(
                        asset_type=AssetType.SOCIAL_MEDIA,
                        value=f"{social['platform']}:{social['handle']}",
                        source="OSINT_AI_Analysis",
                        confidence=social.get('confidence', 0.5),
                        metadata={'platform': social['platform']}
                    ))
                
                # Process employee findings
                for employee in osint_data.get('employees', []):
                    assets.append(ReconAsset(
                        asset_type=AssetType.EMAIL,
                        value=employee['email'],
                        source="OSINT_AI_Analysis",
                        confidence=employee.get('confidence', 0.5),
                        metadata={'name': employee['name'], 'role': employee['role']}
                    ))
                
                # Process technology findings
                for tech in osint_data.get('technologies', []):
                    assets.append(ReconAsset(
                        asset_type=AssetType.TECHNOLOGY,
                        value=tech['tech'],
                        source="OSINT_AI_Analysis",
                        confidence=tech.get('confidence', 0.5),
                        metadata={'evidence': tech['evidence']}
                    ))
                
        except Exception as e:
            logger.error(f"OSINT analysis failed: {e}")
        
        return assets
    
    async def _active_reconnaissance(self, target: str) -> List[ReconAsset]:
        """
        Active reconnaissance with port scanning and service detection
        """
        assets = []
        
        try:
            # Port scanning
            port_assets = await self._port_scanning(target)
            assets.extend(port_assets)
            
            # Service detection
            service_assets = await self._service_detection(target)
            assets.extend(service_assets)
            
            # HTTP reconnaissance
            http_assets = await self._http_reconnaissance(target)
            assets.extend(http_assets)
            
        except Exception as e:
            logger.error(f"Active reconnaissance failed: {e}")
        
        return assets
    
    async def _port_scanning(self, target: str) -> List[ReconAsset]:
        """
        Intelligent port scanning
        """
        assets = []
        
        # Common ports to scan
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080, 8443]
        
        try:
            # Resolve target to IP
            ip = socket.gethostbyname(target)
            
            assets.append(ReconAsset(
                asset_type=AssetType.IP_ADDRESS,
                value=ip,
                source="DNS_Resolution",
                confidence=0.95,
                metadata={'hostname': target}
            ))
            
            # Scan common ports
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    result = sock.connect_ex((ip, port))
                    sock.close()
                    
                    if result == 0:
                        assets.append(ReconAsset(
                            asset_type=AssetType.PORT,
                            value=f"{ip}:{port}",
                            source="Port_Scan",
                            confidence=0.9,
                            metadata={'ip': ip, 'port': port, 'state': 'open'}
                        ))
                except:
                    continue
                    
        except Exception as e:
            logger.error(f"Port scanning failed: {e}")
        
        return assets
    
    async def _service_detection(self, target: str) -> List[ReconAsset]:
        """
        AI-powered service detection
        """
        assets = []
        
        # Service detection on common ports
        service_ports = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            993: 'IMAPS',
            995: 'POP3S',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            8080: 'HTTP-Alt',
            8443: 'HTTPS-Alt'
        }
        
        try:
            ip = socket.gethostbyname(target)
            
            for port, service in service_ports.items():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    result = sock.connect_ex((ip, port))
                    
                    if result == 0:
                        # Try to grab banner
                        banner = ""
                        try:
                            sock.send(b'\r\n')
                            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                        except:
                            pass
                        
                        assets.append(ReconAsset(
                            asset_type=AssetType.SERVICE,
                            value=f"{service}:{port}",
                            source="Service_Detection",
                            confidence=0.85,
                            metadata={'ip': ip, 'port': port, 'service': service, 'banner': banner}
                        ))
                    
                    sock.close()
                except:
                    continue
                    
        except Exception as e:
            logger.error(f"Service detection failed: {e}")
        
        return assets
    
    async def _http_reconnaissance(self, target: str) -> List[ReconAsset]:
        """
        HTTP-specific reconnaissance
        """
        assets = []
        
        try:
            # Test both HTTP and HTTPS
            protocols = ['http', 'https']
            
            for protocol in protocols:
                url = f"{protocol}://{target}"
                
                async with self.request_semaphore:
                    async with aiohttp.ClientSession() as session:
                        try:
                            async with session.get(url, timeout=10) as response:
                                # Analyze response headers
                                server = response.headers.get('Server', '')
                                if server:
                                    assets.append(ReconAsset(
                                        asset_type=AssetType.TECHNOLOGY,
                                        value=server,
                                        source="HTTP_Headers",
                                        confidence=0.9,
                                        metadata={'header': 'Server', 'url': url}
                                    ))
                                
                                # Check for common technologies in headers
                                tech_headers = {
                                    'X-Powered-By': 'Technology',
                                    'X-AspNet-Version': 'ASP.NET',
                                    'X-Generator': 'CMS'
                                }
                                
                                for header, tech_type in tech_headers.items():
                                    if header in response.headers:
                                        assets.append(ReconAsset(
                                            asset_type=AssetType.TECHNOLOGY,
                                            value=f"{tech_type}:{response.headers[header]}",
                                            source="HTTP_Headers",
                                            confidence=0.85,
                                            metadata={'header': header, 'url': url}
                                        ))
                                
                                # Analyze response body for technologies
                                body = await response.text()
                                tech_assets = await self._analyze_http_body(body, url)
                                assets.extend(tech_assets)
                                
                        except:
                            continue
                
                await asyncio.sleep(self.request_delay)
                
        except Exception as e:
            logger.error(f"HTTP reconnaissance failed: {e}")
        
        return assets
    
    async def _analyze_http_body(self, body: str, url: str) -> List[ReconAsset]:
        """
        AI-powered analysis of HTTP response body
        """
        assets = []
        
        # Truncate body for AI analysis
        body_sample = body[:2000] if len(body) > 2000 else body
        
        analysis_prompt = f"""
        Analyze this HTTP response body to identify technologies, frameworks, and potential security issues:
        
        URL: {url}
        RESPONSE BODY SAMPLE:
        {body_sample}
        
        Identify:
        1. Web frameworks (React, Angular, Vue, Django, Laravel, etc.)
        2. CMS platforms (WordPress, Drupal, Joomla, etc.)
        3. JavaScript libraries (jQuery, Bootstrap, etc.)
        4. Server technologies (Apache, Nginx, IIS, etc.)
        5. Database hints (MySQL, PostgreSQL, MongoDB, etc.)
        6. Third-party services (Google Analytics, CDNs, etc.)
        7. Potential security issues (error messages, debug info, etc.)
        8. API endpoints or AJAX calls
        9. Hidden form fields or parameters
        10. Comments with sensitive information
        
        Return findings as JSON:
        {{
            "technologies": [
                {{"name": "React", "evidence": "React DOM render", "confidence": 0.9}}
            ],
            "endpoints": [
                {{"path": "/api/users", "method": "GET", "confidence": 0.7}}
            ],
            "parameters": [
                {{"name": "user_id", "context": "form field", "confidence": 0.8}}
            ],
            "security_issues": [
                {{"issue": "Debug mode enabled", "evidence": "Django debug page", "severity": "medium"}}
            ]
        }}
        """
        
        ai_response = await self._query_ai_model(analysis_prompt)
        
        try:
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                
                # Process technology findings
                for tech in analysis.get('technologies', []):
                    assets.append(ReconAsset(
                        asset_type=AssetType.TECHNOLOGY,
                        value=tech['name'],
                        source="HTTP_Body_Analysis",
                        confidence=tech.get('confidence', 0.5),
                        metadata={'evidence': tech['evidence'], 'url': url}
                    ))
                
                # Process endpoint findings
                for endpoint in analysis.get('endpoints', []):
                    full_url = urljoin(url, endpoint['path'])
                    assets.append(ReconAsset(
                        asset_type=AssetType.ENDPOINT,
                        value=full_url,
                        source="HTTP_Body_Analysis",
                        confidence=endpoint.get('confidence', 0.5),
                        metadata={'method': endpoint.get('method', 'GET')}
                    ))
                
                # Process parameter findings
                for param in analysis.get('parameters', []):
                    assets.append(ReconAsset(
                        asset_type=AssetType.PARAMETER,
                        value=param['name'],
                        source="HTTP_Body_Analysis",
                        confidence=param.get('confidence', 0.5),
                        metadata={'context': param['context'], 'url': url}
                    ))
                
        except Exception as e:
            logger.error(f"HTTP body analysis failed: {e}")
        
        return assets
    
    async def _technology_fingerprinting(self, target: str) -> List[ReconAsset]:
        """
        Advanced technology fingerprinting
        """
        assets = []
        
        try:
            # SSL/TLS analysis
            ssl_assets = await self._ssl_analysis(target)
            assets.extend(ssl_assets)
            
            # Application fingerprinting
            app_assets = await self._application_fingerprinting(target)
            assets.extend(app_assets)
            
        except Exception as e:
            logger.error(f"Technology fingerprinting failed: {e}")
        
        return assets
    
    async def _ssl_analysis(self, target: str) -> List[ReconAsset]:
        """
        SSL/TLS certificate analysis
        """
        assets = []
        
        try:
            # Get SSL certificate info
            context = ssl.create_default_context()
            with socket.create_connection((target, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Extract certificate information
                    if cert:
                        # Subject alternative names
                        for ext in cert.get('subjectAltName', []):
                            if ext[0] == 'DNS':
                                assets.append(ReconAsset(
                                    asset_type=AssetType.SUBDOMAIN,
                                    value=ext[1],
                                    source="SSL_Certificate",
                                    confidence=0.95,
                                    metadata={'cert_source': 'SAN'}
                                ))
                        
                        # Certificate issuer
                        issuer = dict(cert.get('issuer', []))
                        if 'organizationName' in issuer:
                            assets.append(ReconAsset(
                                asset_type=AssetType.TECHNOLOGY,
                                value=f"SSL_Issuer:{issuer['organizationName']}",
                                source="SSL_Certificate",
                                confidence=0.8,
                                metadata={'cert_issuer': issuer['organizationName']}
                            ))
                            
        except Exception as e:
            logger.error(f"SSL analysis failed: {e}")
        
        return assets
    
    async def _application_fingerprinting(self, target: str) -> List[ReconAsset]:
        """
        Application-specific fingerprinting
        """
        assets = []
        
        # WordPress detection
        wp_paths = ['/wp-admin/', '/wp-content/', '/wp-includes/', '/wp-login.php']
        
        for path in wp_paths:
            url = f"https://{target}{path}"
            
            async with self.request_semaphore:
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.get(url, timeout=5) as response:
                            if response.status == 200:
                                assets.append(ReconAsset(
                                    asset_type=AssetType.TECHNOLOGY,
                                    value="WordPress",
                                    source="Application_Fingerprinting",
                                    confidence=0.9,
                                    metadata={'detected_path': path}
                                ))
                                break
                    except:
                        continue
            
            await asyncio.sleep(self.request_delay)
        
        return assets
    
    async def _endpoint_discovery(self, target: str) -> List[ReconAsset]:
        """
        AI-enhanced endpoint discovery
        """
        assets = []
        
        try:
            # Directory brute forcing
            directory_assets = await self._directory_bruteforce(target)
            assets.extend(directory_assets)
            
            # Parameter discovery
            param_assets = await self._parameter_discovery(target)
            assets.extend(param_assets)
            
            # AI-powered endpoint prediction
            ai_endpoints = await self._ai_endpoint_prediction(target, assets)
            assets.extend(ai_endpoints)
            
        except Exception as e:
            logger.error(f"Endpoint discovery failed: {e}")
        
        return assets
    
    async def _directory_bruteforce(self, target: str) -> List[ReconAsset]:
        """
        Intelligent directory brute forcing
        """
        assets = []
        
        base_url = f"https://{target}"
        
        for directory in self.directory_wordlist[:20]:  # Limit for demo
            url = f"{base_url}/{directory}"
            
            async with self.request_semaphore:
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.get(url, timeout=5) as response:
                            if response.status in [200, 301, 302, 403]:
                                assets.append(ReconAsset(
                                    asset_type=AssetType.ENDPOINT,
                                    value=url,
                                    source="Directory_Bruteforce",
                                    confidence=0.8,
                                    metadata={'status_code': response.status}
                                ))
                    except:
                        continue
            
            await asyncio.sleep(self.request_delay)
        
        return assets
    
    async def _parameter_discovery(self, target: str) -> List[ReconAsset]:
        """
        Parameter discovery and analysis
        """
        assets = []
        
        base_url = f"https://{target}"
        
        # Test common parameters
        for param in self.parameter_wordlist[:10]:  # Limit for demo
            test_url = f"{base_url}/?{param}=test"
            
            async with self.request_semaphore:
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.get(test_url, timeout=5) as response:
                            body = await response.text()
                            
                            # Look for parameter reflection or different behavior
                            if 'test' in body or response.status != 404:
                                assets.append(ReconAsset(
                                    asset_type=AssetType.PARAMETER,
                                    value=param,
                                    source="Parameter_Discovery",
                                    confidence=0.6,
                                    metadata={'test_url': test_url, 'reflected': 'test' in body}
                                ))
                    except:
                        continue
            
            await asyncio.sleep(self.request_delay)
        
        return assets
    
    async def _ai_endpoint_prediction(self, target: str, discovered_assets: List[ReconAsset]) -> List[ReconAsset]:
        """
        AI-powered endpoint prediction based on discovered assets
        """
        # Get discovered endpoints and technologies
        endpoints = [asset.value for asset in discovered_assets if asset.asset_type == AssetType.ENDPOINT]
        technologies = [asset.value for asset in discovered_assets if asset.asset_type == AssetType.TECHNOLOGY]
        
        if not endpoints and not technologies:
            return []
        
        prediction_prompt = f"""
        Based on the discovered assets for {target}, predict additional likely endpoints and URLs:
        
        DISCOVERED ENDPOINTS: {endpoints}
        DETECTED TECHNOLOGIES: {technologies}
        
        Analyze patterns and predict:
        1. API endpoints (REST, GraphQL, etc.)
        2. Admin interfaces and control panels
        3. Configuration and settings pages
        4. Upload and file management endpoints
        5. Authentication and user management URLs
        6. Development and testing endpoints
        7. Documentation and help pages
        8. Backup and archive locations
        9. Database management interfaces
        10. Monitoring and status pages
        
        Consider:
        - Technology-specific patterns (WordPress, Django, etc.)
        - Common naming conventions
        - Version-based paths (v1, v2, etc.)
        - Environment indicators (dev, staging, prod)
        
        Return as JSON array of predicted URLs:
        ["https://{target}/api/v1/users", "https://{target}/admin/dashboard", ...]
        """
        
        ai_response = await self._query_ai_model(prediction_prompt)
        
        try:
            json_match = re.search(r'\[.*\]', ai_response, re.DOTALL)
            if json_match:
                predicted_endpoints = json.loads(json_match.group())
                
                assets = []
                for endpoint in predicted_endpoints:
                    if isinstance(endpoint, str) and target in endpoint:
                        assets.append(ReconAsset(
                            asset_type=AssetType.ENDPOINT,
                            value=endpoint,
                            source="AI_Endpoint_Prediction",
                            confidence=0.4,
                            metadata={'predicted': True}
                        ))
                
                return assets
        except Exception as e:
            logger.error(f"AI endpoint prediction failed: {e}")
        
        return []
    
    async def _ai_attack_surface_analysis(self, target: str, assets: List[ReconAsset]) -> AttackSurface:
        """
        AI-powered attack surface analysis and risk assessment
        """
        # Categorize assets
        asset_summary = {}
        for asset_type in AssetType:
            asset_summary[asset_type.value] = [
                asset.value for asset in assets if asset.asset_type == asset_type
            ]
        
        analysis_prompt = f"""
        Perform comprehensive attack surface analysis for {target}:
        
        DISCOVERED ASSETS:
        {json.dumps(asset_summary, indent=2)}
        
        ANALYSIS REQUIRED:
        1. Risk assessment (0-10 scale)
        2. Primary attack vectors
        3. High-value targets
        4. Potential vulnerabilities
        5. Entry points for attackers
        6. Technology-specific risks
        7. OSINT exposure level
        8. Overall security posture
        
        CONSIDER:
        - Exposed services and ports
        - Outdated technologies
        - Misconfigurations
        - Information disclosure
        - Attack chain possibilities
        - Social engineering opportunities
        
        Provide detailed analysis and actionable recommendations:
        {{
            "risk_score": 7.5,
            "primary_attack_vectors": ["Web application attacks", "Social engineering"],
            "high_value_targets": ["admin.{target}", "api.{target}"],
            "vulnerabilities": ["Exposed admin interface", "Information disclosure"],
            "entry_points": ["/admin/login", "/api/v1/"],
            "technology_risks": ["WordPress vulnerabilities", "Outdated SSL"],
            "recommendations": ["Secure admin interface", "Update SSL certificate"],
            "analysis": "Detailed analysis text here..."
        }}
        """
        
        ai_response = await self._query_ai_model(analysis_prompt)
        
        try:
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                
                return AttackSurface(
                    target=target,
                    assets=assets,
                    technologies={asset.value: asset.metadata.get('evidence', '') 
                                for asset in assets if asset.asset_type == AssetType.TECHNOLOGY},
                    vulnerabilities=analysis.get('vulnerabilities', []),
                    entry_points=analysis.get('entry_points', []),
                    risk_score=analysis.get('risk_score', 5.0),
                    ai_analysis=analysis.get('analysis', 'Analysis completed')
                )
        except Exception as e:
            logger.error(f"Attack surface analysis failed: {e}")
        
        # Fallback basic analysis
        return AttackSurface(
            target=target,
            assets=assets,
            technologies={},
            vulnerabilities=[],
            entry_points=[],
            risk_score=5.0,
            ai_analysis="Basic analysis - AI analysis failed"
        )
    
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
    
    def get_reconnaissance_report(self, target: str) -> Dict:
        """
        Generate comprehensive reconnaissance report
        """
        attack_surface = self.attack_surfaces.get(target)
        assets = self.discovered_assets.get(target, [])
        
        if not attack_surface:
            return {"error": "No reconnaissance data available for target"}
        
        # Categorize assets by type
        asset_counts = {}
        for asset_type in AssetType:
            count = len([a for a in assets if a.asset_type == asset_type])
            if count > 0:
                asset_counts[asset_type.value] = count
        
        # Get high-confidence assets
        high_confidence_assets = [a for a in assets if a.confidence > 0.8]
        
        return {
            "target": target,
            "reconnaissance_summary": {
                "total_assets": len(assets),
                "asset_breakdown": asset_counts,
                "high_confidence_findings": len(high_confidence_assets),
                "risk_score": attack_surface.risk_score
            },
            "attack_surface": {
                "entry_points": attack_surface.entry_points,
                "vulnerabilities": attack_surface.vulnerabilities,
                "technologies": attack_surface.technologies,
                "ai_analysis": attack_surface.ai_analysis
            },
            "key_findings": [
                {
                    "type": asset.asset_type.value,
                    "value": asset.value,
                    "confidence": asset.confidence,
                    "source": asset.source
                } for asset in high_confidence_assets
            ]
        }

# Factory function
def create_ai_reconnaissance(config: Dict) -> AIReconnaissance:
    """
    Factory function to create AI reconnaissance engine
    """
    return AIReconnaissance(config)
