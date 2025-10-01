"""
Security Results Manager - Comprehensive storage and management of security test results
Stores all vulnerability findings, test reports, and provides downloadable exports
"""

import json
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import csv
import uuid
from pathlib import Path

@dataclass
class SecurityTestSession:
    """Complete security testing session data."""
    session_id: str
    target_url: str
    start_time: datetime
    end_time: Optional[datetime]
    total_tests: int
    vulnerabilities_found: int
    elements_discovered: int
    test_results: List[Dict[str, Any]]
    discovered_elements: List[Dict[str, Any]]
    session_summary: Dict[str, Any]
    
class SecurityResultsManager:
    """Manages storage, retrieval, and export of security test results."""
    
    def __init__(self, data_dir: str = "security_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize database
        self.db_path = self.data_dir / "security_results.db"
        self.init_database()
        
        # Results storage
        self.json_dir = self.data_dir / "json_reports"
        self.csv_dir = self.data_dir / "csv_exports"
        self.json_dir.mkdir(exist_ok=True)
        self.csv_dir.mkdir(exist_ok=True)
    
    def init_database(self):
        """Initialize SQLite database for security results."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS security_sessions (
                    session_id TEXT PRIMARY KEY,
                    target_url TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    total_tests INTEGER,
                    vulnerabilities_found INTEGER,
                    elements_discovered INTEGER,
                    session_data TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vulnerability_findings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    vulnerability_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    element_type TEXT,
                    element_url TEXT,
                    payload_used TEXT,
                    evidence TEXT,
                    timestamp TEXT,
                    status TEXT DEFAULT 'open',
                    FOREIGN KEY (session_id) REFERENCES security_sessions (session_id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS discovered_elements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    element_type TEXT NOT NULL,
                    element_id TEXT,
                    element_url TEXT,
                    method TEXT,
                    parameters_count INTEGER,
                    context TEXT,
                    FOREIGN KEY (session_id) REFERENCES security_sessions (session_id)
                )
            """)
            
            conn.commit()
    
    def save_security_session(self, session_data: Dict[str, Any]) -> str:
        """Save complete security testing session."""
        session_id = str(uuid.uuid4())
        
        # Prepare session data
        session = SecurityTestSession(
            session_id=session_id,
            target_url=session_data['target_url'],
            start_time=datetime.now(),
            end_time=datetime.now(),
            total_tests=session_data.get('total_tests', 0),
            vulnerabilities_found=session_data.get('vulnerabilities_found', 0),
            elements_discovered=session_data.get('elements_discovered', 0),
            test_results=session_data.get('test_results', []),
            discovered_elements=session_data.get('discovered_elements', []),
            session_summary=self._generate_session_summary(session_data)
        )
        
        # Save to database
        with sqlite3.connect(self.db_path) as conn:
            # Save main session
            conn.execute("""
                INSERT INTO security_sessions 
                (session_id, target_url, start_time, end_time, total_tests, 
                 vulnerabilities_found, elements_discovered, session_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                session.target_url,
                session.start_time.isoformat(),
                session.end_time.isoformat() if session.end_time else None,
                session.total_tests,
                session.vulnerabilities_found,
                session.elements_discovered,
                json.dumps(asdict(session), default=str)
            ))
            
            # Save vulnerability findings
            for result in session_data.get('test_results', []):
                if result.get('success', False):
                    conn.execute("""
                        INSERT INTO vulnerability_findings
                        (session_id, vulnerability_type, severity, element_type, 
                         element_url, payload_used, evidence, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        session_id,
                        result.get('vulnerability_type', ''),
                        result.get('severity', ''),
                        result.get('element_type', ''),
                        result.get('element_url', ''),
                        result.get('payload_used', ''),
                        result.get('evidence', ''),
                        result.get('timestamp', datetime.now().isoformat())
                    ))
            
            # Save discovered elements
            for element in session_data.get('discovered_elements', []):
                conn.execute("""
                    INSERT INTO discovered_elements
                    (session_id, element_type, element_id, element_url, 
                     method, parameters_count, context)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_id,
                    element.get('type', ''),
                    element.get('id', ''),
                    element.get('url', ''),
                    element.get('method', ''),
                    element.get('parameters', 0),
                    element.get('context', '')
                ))
            
            conn.commit()
        
        # Save JSON report
        self.save_json_report(session_id, session)
        
        # Save CSV exports
        self.save_csv_reports(session_id, session)
        
        print(f"✅ Security session saved: {session_id}")
        return session_id
    
    def save_json_report(self, session_id: str, session: SecurityTestSession):
        """Save detailed JSON report."""
        report_path = self.json_dir / f"security_report_{session_id}.json"
        
        report_data = {
            "report_metadata": {
                "session_id": session_id,
                "generated_at": datetime.now().isoformat(),
                "target_url": session.target_url,
                "report_type": "comprehensive_security_test"
            },
            "executive_summary": {
                "total_tests_performed": session.total_tests,
                "vulnerabilities_discovered": session.vulnerabilities_found,
                "elements_analyzed": session.elements_discovered,
                "risk_level": self._calculate_risk_level(session.vulnerabilities_found, session.test_results),
                "test_duration": str(session.end_time - session.start_time) if session.end_time else "Unknown"
            },
            "vulnerability_details": [
                result for result in session.test_results if result.get('success', False)
            ],
            "discovered_elements": session.discovered_elements,
            "all_test_results": session.test_results,
            "recommendations": self._generate_recommendations(session.test_results)
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        return str(report_path)
    
    def save_csv_reports(self, session_id: str, session: SecurityTestSession):
        """Save CSV exports for easy analysis."""
        
        # Vulnerabilities CSV
        vuln_path = self.csv_dir / f"vulnerabilities_{session_id}.csv"
        vulnerabilities = [r for r in session.test_results if r.get('success', False)]
        
        if vulnerabilities:
            with open(vuln_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'vulnerability_type', 'severity', 'element_type', 'element_url',
                    'payload_used', 'evidence', 'timestamp'
                ])
                writer.writeheader()
                for vuln in vulnerabilities:
                    writer.writerow({
                        'vulnerability_type': vuln.get('vulnerability_type', ''),
                        'severity': vuln.get('severity', ''),
                        'element_type': vuln.get('element_type', ''),
                        'element_url': vuln.get('element_url', ''),
                        'payload_used': vuln.get('payload_used', ''),
                        'evidence': vuln.get('evidence', ''),
                        'timestamp': vuln.get('timestamp', '')
                    })
        
        # Elements CSV
        elements_path = self.csv_dir / f"elements_{session_id}.csv"
        if session.discovered_elements:
            with open(elements_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'type', 'id', 'url', 'method', 'parameters', 'context'
                ])
                writer.writeheader()
                writer.writerows(session.discovered_elements)
        
        return str(vuln_path), str(elements_path)
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Get all security testing sessions."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT session_id, target_url, start_time, end_time,
                       total_tests, vulnerabilities_found, elements_discovered
                FROM security_sessions
                ORDER BY start_time DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_session_details(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific session."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Get session info
            session = conn.execute("""
                SELECT * FROM security_sessions WHERE session_id = ?
            """, (session_id,)).fetchone()
            
            if not session:
                return None
            
            # Get vulnerabilities
            vulnerabilities = conn.execute("""
                SELECT * FROM vulnerability_findings WHERE session_id = ?
            """, (session_id,)).fetchall()
            
            # Get elements
            elements = conn.execute("""
                SELECT * FROM discovered_elements WHERE session_id = ?
            """, (session_id,)).fetchall()
            
            return {
                "session": dict(session),
                "vulnerabilities": [dict(v) for v in vulnerabilities],
                "elements": [dict(e) for e in elements]
            }
    
    def get_vulnerability_summary(self) -> Dict[str, Any]:
        """Get overall vulnerability statistics."""
        with sqlite3.connect(self.db_path) as conn:
            # Total vulnerabilities by type
            vuln_types = conn.execute("""
                SELECT vulnerability_type, COUNT(*) as count
                FROM vulnerability_findings
                GROUP BY vulnerability_type
                ORDER BY count DESC
            """).fetchall()
            
            # Vulnerabilities by severity
            severity_counts = conn.execute("""
                SELECT severity, COUNT(*) as count
                FROM vulnerability_findings
                GROUP BY severity
                ORDER BY count DESC
            """).fetchall()
            
            # Recent sessions
            recent_sessions = conn.execute("""
                SELECT COUNT(*) as total_sessions,
                       SUM(vulnerabilities_found) as total_vulns,
                       AVG(vulnerabilities_found) as avg_vulns_per_session
                FROM security_sessions
                WHERE start_time >= datetime('now', '-30 days')
            """).fetchone()
            
            return {
                "vulnerability_types": [{"type": row[0], "count": row[1]} for row in vuln_types],
                "severity_breakdown": [{"severity": row[0], "count": row[1]} for row in severity_counts],
                "recent_stats": dict(recent_sessions) if recent_sessions else {},
                "last_updated": datetime.now().isoformat()
            }
    
    def export_session_report(self, session_id: str, format: str = "json") -> Optional[str]:
        """Export session report in specified format."""
        session_details = self.get_session_details(session_id)
        if not session_details:
            return None
        
        if format.lower() == "json":
            export_path = self.json_dir / f"export_{session_id}.json"
            with open(export_path, 'w') as f:
                json.dump(session_details, f, indent=2, default=str)
            return str(export_path)
        
        elif format.lower() == "csv":
            export_path = self.csv_dir / f"export_{session_id}.csv"
            with open(export_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Session Report", session_id])
                writer.writerow([])
                
                # Session info
                writer.writerow(["Session Information"])
                for key, value in session_details["session"].items():
                    writer.writerow([key, value])
                
                writer.writerow([])
                writer.writerow(["Vulnerabilities Found"])
                if session_details["vulnerabilities"]:
                    headers = list(session_details["vulnerabilities"][0].keys())
                    writer.writerow(headers)
                    for vuln in session_details["vulnerabilities"]:
                        writer.writerow([vuln.get(h, '') for h in headers])
                
            return str(export_path)
        
        return None
    
    def _generate_session_summary(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary for session."""
        vulnerabilities = [r for r in session_data.get('test_results', []) if r.get('success', False)]
        
        # Count by severity
        severity_counts = {}
        vuln_types = {}
        
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'UNKNOWN')
            vuln_type = vuln.get('vulnerability_type', 'UNKNOWN')
            
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            vuln_types[vuln_type] = vuln_types.get(vuln_type, 0) + 1
        
        return {
            "risk_assessment": self._calculate_risk_level(len(vulnerabilities), session_data.get('test_results', [])),
            "severity_breakdown": severity_counts,
            "vulnerability_types": vuln_types,
            "coverage": {
                "elements_tested": session_data.get('elements_discovered', 0),
                "tests_performed": session_data.get('total_tests', 0),
                "success_rate": len(vulnerabilities) / max(session_data.get('total_tests', 1), 1) * 100
            }
        }
    
    def _calculate_risk_level(self, vuln_count: int, test_results: List[Dict[str, Any]]) -> str:
        """Calculate overall risk level."""
        if vuln_count == 0:
            return "LOW"
        
        # Check for critical vulnerabilities
        critical_count = sum(1 for r in test_results if r.get('severity') == 'CRITICAL' and r.get('success', False))
        high_count = sum(1 for r in test_results if r.get('severity') == 'HIGH' and r.get('success', False))
        
        if critical_count > 0:
            return "CRITICAL"
        elif high_count > 2:
            return "HIGH"
        elif vuln_count > 5:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_recommendations(self, test_results: List[Dict[str, Any]]) -> List[str]:
        """Generate security recommendations based on findings."""
        recommendations = []
        vulnerabilities = [r for r in test_results if r.get('success', False)]
        
        # Check for common vulnerability types
        vuln_types = [v.get('vulnerability_type', '') for v in vulnerabilities]
        
        if 'xss_injection' in vuln_types:
            recommendations.append("Implement input sanitization and output encoding to prevent XSS attacks")
            recommendations.append("Deploy Content Security Policy (CSP) headers")
        
        if 'sql_injection' in vuln_types:
            recommendations.append("Use parameterized queries and prepared statements")
            recommendations.append("Implement input validation and least privilege database access")
        
        if len(vulnerabilities) > 5:
            recommendations.append("Conduct regular security assessments and penetration testing")
            recommendations.append("Implement Web Application Firewall (WAF)")
        
        if not recommendations:
            recommendations.append("Continue regular security monitoring and testing")
            recommendations.append("Implement security best practices and secure coding guidelines")
        
        return recommendations
    
    def cleanup_old_data(self, days_old: int = 90):
        """Clean up old test data to save space."""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        with sqlite3.connect(self.db_path) as conn:
            # Get old session IDs
            old_sessions = conn.execute("""
                SELECT session_id FROM security_sessions 
                WHERE start_time < ?
            """, (cutoff_date.isoformat(),)).fetchall()
            
            # Delete old data
            conn.execute("""
                DELETE FROM vulnerability_findings 
                WHERE session_id IN (
                    SELECT session_id FROM security_sessions 
                    WHERE start_time < ?
                )
            """, (cutoff_date.isoformat(),))
            
            conn.execute("""
                DELETE FROM discovered_elements 
                WHERE session_id IN (
                    SELECT session_id FROM security_sessions 
                    WHERE start_time < ?
                )
            """, (cutoff_date.isoformat(),))
            
            conn.execute("""
                DELETE FROM security_sessions WHERE start_time < ?
            """, (cutoff_date.isoformat(),))
            
            conn.commit()
        
        # Clean up old files
        for session_id, in old_sessions:
            json_file = self.json_dir / f"security_report_{session_id}.json"
            csv_vuln_file = self.csv_dir / f"vulnerabilities_{session_id}.csv"
            csv_elements_file = self.csv_dir / f"elements_{session_id}.csv"
            
            for file_path in [json_file, csv_vuln_file, csv_elements_file]:
                if file_path.exists():
                    file_path.unlink()
        
        print(f"🧹 Cleaned up data older than {days_old} days")
