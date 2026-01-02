#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for CyberSentinel AI Phishing Defense System
Tests all endpoints, detection engines, and integration scenarios
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, List

class CyberSentinelAPITester:
    def __init__(self, base_url="https://cybersentinel-19.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.test_results = []

    def log_test(self, name: str, success: bool, details: str = "", response_data: Dict = None):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
            self.failed_tests.append({"test": name, "error": details})
        
        self.test_results.append({
            "test_name": name,
            "success": success,
            "details": details,
            "response_data": response_data
        })

    def test_health_endpoint(self):
        """Test /api/ health check endpoint"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "CyberSentinel" in data["message"]:
                    self.log_test("Health Check Endpoint", True, f"Status: {data.get('status', 'unknown')}")
                    return True
                else:
                    self.log_test("Health Check Endpoint", False, "Invalid response format")
                    return False
            else:
                self.log_test("Health Check Endpoint", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check Endpoint", False, f"Connection error: {str(e)}")
            return False

    def test_analyze_endpoint_general(self):
        """Test /api/analyze with general mode"""
        test_content = "Congratulations! You've won $10,000 in our prize draw. Click here to claim: http://fake-prize.tk/claim"
        
        try:
            response = requests.post(
                f"{self.api_url}/analyze",
                json={
                    "content": test_content,
                    "mode": "general"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["risk_score", "verdict", "mode", "engine_results", "summary", "recommendations"]
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test("Analyze General Mode", False, f"Missing fields: {missing_fields}")
                    return False
                
                # Validate risk score
                if not (0 <= data["risk_score"] <= 100):
                    self.log_test("Analyze General Mode", False, f"Invalid risk score: {data['risk_score']}")
                    return False
                
                # Validate engine results
                if len(data["engine_results"]) < 4:  # Should have at least 4 engines for general mode
                    self.log_test("Analyze General Mode", False, f"Too few engines: {len(data['engine_results'])}")
                    return False
                
                self.log_test("Analyze General Mode", True, f"Risk: {data['risk_score']}, Verdict: {data['verdict']}")
                return True
            else:
                self.log_test("Analyze General Mode", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Analyze General Mode", False, f"Error: {str(e)}")
            return False

    def test_analyze_endpoint_email(self):
        """Test /api/analyze with email mode and headers"""
        test_content = """From: security@paypa1-support.com
Subject: Urgent: Your Account Will Be Suspended

Dear Customer,

Your PayPal account has been temporarily restricted due to unusual activity. You must verify your account within 24 hours to avoid permanent suspension.

Click here to verify: http://paypal-verify.tk/confirm

Thank you,
PayPal Security Team"""
        
        test_headers = {
            "from": "security@paypa1-support.com",
            "spf": "fail",
            "dkim": "pass",
            "dmarc": "fail"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/analyze",
                json={
                    "content": test_content,
                    "mode": "email",
                    "email_headers": test_headers
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Should have 5 engines for email mode (including email header engine)
                if len(data["engine_results"]) < 5:
                    self.log_test("Analyze Email Mode", False, f"Missing email header engine: {len(data['engine_results'])}")
                    return False
                
                # Check if email header engine is present
                engine_names = [engine["engine_name"] for engine in data["engine_results"]]
                if "Email Header Analysis" not in engine_names:
                    self.log_test("Analyze Email Mode", False, "Email Header Analysis engine missing")
                    return False
                
                self.log_test("Analyze Email Mode", True, f"Risk: {data['risk_score']}, Engines: {len(data['engine_results'])}")
                return True
            else:
                self.log_test("Analyze Email Mode", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Analyze Email Mode", False, f"Error: {str(e)}")
            return False

    def test_analyze_endpoint_url(self):
        """Test /api/analyze with URL mode"""
        test_url = "http://g00gle-security-alert.tk/verify-account?session=83749234"
        
        try:
            response = requests.post(
                f"{self.api_url}/analyze",
                json={
                    "content": test_url,
                    "mode": "url"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if URL engine detected the malicious URL
                url_engine_result = None
                for engine in data["engine_results"]:
                    if "URL" in engine["engine_name"]:
                        url_engine_result = engine
                        break
                
                if not url_engine_result:
                    self.log_test("Analyze URL Mode", False, "URL Intelligence engine not found")
                    return False
                
                if url_engine_result["risk_score"] < 10:  # Should detect suspicious TLD and lookalike domain
                    self.log_test("Analyze URL Mode", False, f"URL engine risk too low: {url_engine_result['risk_score']}")
                    return False
                
                self.log_test("Analyze URL Mode", True, f"URL Risk: {url_engine_result['risk_score']}")
                return True
            else:
                self.log_test("Analyze URL Mode", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Analyze URL Mode", False, f"Error: {str(e)}")
            return False

    def test_analyze_endpoint_sms(self):
        """Test /api/analyze with SMS mode"""
        test_sms = "URGENT: Your package delivery failed. Confirm your address here: bit.ly/pkg-confirm. Fees pending. Reply STOP to cancel."
        
        try:
            response = requests.post(
                f"{self.api_url}/analyze",
                json={
                    "content": test_sms,
                    "mode": "sms"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if behavioral engine detected mobile scam patterns
                behavioral_engine = None
                for engine in data["engine_results"]:
                    if "Behavioral" in engine["engine_name"]:
                        behavioral_engine = engine
                        break
                
                if not behavioral_engine:
                    self.log_test("Analyze SMS Mode", False, "Behavioral Analysis engine not found")
                    return False
                
                self.log_test("Analyze SMS Mode", True, f"Risk: {data['risk_score']}, Behavioral: {behavioral_engine['risk_score']}")
                return True
            else:
                self.log_test("Analyze SMS Mode", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Analyze SMS Mode", False, f"Error: {str(e)}")
            return False

    def test_analyze_endpoint_whatsapp(self):
        """Test /api/analyze with WhatsApp mode"""
        test_whatsapp = "Hi! You've been selected to receive a $500 Amazon gift card! Click this link to claim your reward before it expires: http://amazon-gift.xyz/claim?id=8374"
        
        try:
            response = requests.post(
                f"{self.api_url}/analyze",
                json={
                    "content": test_whatsapp,
                    "mode": "whatsapp"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Should detect scam patterns
                scam_engine = None
                for engine in data["engine_results"]:
                    if "Scam Pattern" in engine["engine_name"]:
                        scam_engine = engine
                        break
                
                if not scam_engine:
                    self.log_test("Analyze WhatsApp Mode", False, "Scam Pattern Recognition engine not found")
                    return False
                
                self.log_test("Analyze WhatsApp Mode", True, f"Risk: {data['risk_score']}, Scam: {scam_engine['risk_score']}")
                return True
            else:
                self.log_test("Analyze WhatsApp Mode", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Analyze WhatsApp Mode", False, f"Error: {str(e)}")
            return False

    def test_stats_endpoint(self):
        """Test /api/stats endpoint"""
        try:
            response = requests.get(f"{self.api_url}/stats", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["total_analyses", "verdicts"]
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test("Stats Endpoint", False, f"Missing fields: {missing_fields}")
                    return False
                
                # Check verdicts structure
                if "verdicts" in data:
                    verdict_fields = ["phishing", "scam", "suspicious", "safe"]
                    missing_verdicts = [field for field in verdict_fields if field not in data["verdicts"]]
                    if missing_verdicts:
                        self.log_test("Stats Endpoint", False, f"Missing verdict fields: {missing_verdicts}")
                        return False
                
                self.log_test("Stats Endpoint", True, f"Total analyses: {data['total_analyses']}")
                return True
            else:
                self.log_test("Stats Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Stats Endpoint", False, f"Error: {str(e)}")
            return False

    def test_engine_integration(self):
        """Test that all 5 engines are working properly"""
        test_content = "URGENT: Your PayPal account will be suspended! Click http://paypa1-verify.tk/login to verify your SSN and credit card details immediately!"
        
        try:
            response = requests.post(
                f"{self.api_url}/analyze",
                json={
                    "content": test_content,
                    "mode": "general"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                expected_engines = ["NLP Engine", "URL Intelligence", "Behavioral Analysis", "Scam Pattern Recognition"]
                found_engines = [engine["engine_name"] for engine in data["engine_results"]]
                
                missing_engines = [engine for engine in expected_engines if engine not in found_engines]
                if missing_engines:
                    self.log_test("Engine Integration", False, f"Missing engines: {missing_engines}")
                    return False
                
                # Check if engines are actually detecting threats
                high_risk_engines = [engine for engine in data["engine_results"] if engine["risk_score"] > 20]
                if len(high_risk_engines) < 2:
                    self.log_test("Engine Integration", False, f"Too few engines detecting threats: {len(high_risk_engines)}")
                    return False
                
                self.log_test("Engine Integration", True, f"All engines active, {len(high_risk_engines)} detecting threats")
                return True
            else:
                self.log_test("Engine Integration", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Engine Integration", False, f"Error: {str(e)}")
            return False

    def test_risk_scoring_accuracy(self):
        """Test risk scoring accuracy with known safe and malicious content"""
        
        # Test safe content
        safe_content = "Hello, this is a legitimate message from your colleague about the meeting tomorrow at 2 PM."
        
        try:
            response = requests.post(
                f"{self.api_url}/analyze",
                json={"content": safe_content, "mode": "general"},
                timeout=30
            )
            
            if response.status_code == 200:
                safe_data = response.json()
                if safe_data["risk_score"] > 30:  # Should be low risk
                    self.log_test("Risk Scoring - Safe Content", False, f"Safe content scored too high: {safe_data['risk_score']}")
                    return False
            else:
                self.log_test("Risk Scoring - Safe Content", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Risk Scoring - Safe Content", False, f"Error: {str(e)}")
            return False
        
        # Test malicious content
        malicious_content = "URGENT! Your account has been compromised! Click http://fake-bank.tk/verify and enter your password, SSN, and credit card details NOW!"
        
        try:
            response = requests.post(
                f"{self.api_url}/analyze",
                json={"content": malicious_content, "mode": "general"},
                timeout=30
            )
            
            if response.status_code == 200:
                malicious_data = response.json()
                if malicious_data["risk_score"] < 50:  # Should be high risk
                    self.log_test("Risk Scoring - Malicious Content", False, f"Malicious content scored too low: {malicious_data['risk_score']}")
                    return False
                
                self.log_test("Risk Scoring Accuracy", True, f"Safe: {safe_data['risk_score']}, Malicious: {malicious_data['risk_score']}")
                return True
            else:
                self.log_test("Risk Scoring - Malicious Content", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Risk Scoring - Malicious Content", False, f"Error: {str(e)}")
            return False

    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🔍 Starting CyberSentinel AI Backend Testing...")
        print(f"📡 Testing API at: {self.api_url}")
        print("=" * 60)
        
        # Core endpoint tests
        self.test_health_endpoint()
        
        # Analysis endpoint tests for all modes
        self.test_analyze_endpoint_general()
        self.test_analyze_endpoint_email()
        self.test_analyze_endpoint_url()
        self.test_analyze_endpoint_sms()
        self.test_analyze_endpoint_whatsapp()
        
        # Additional endpoint tests
        self.test_stats_endpoint()
        
        # Integration tests
        self.test_engine_integration()
        self.test_risk_scoring_accuracy()
        
        # Print summary
        print("=" * 60)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        
        if self.failed_tests:
            print("\n❌ Failed Tests:")
            for failure in self.failed_tests:
                print(f"  • {failure['test']}: {failure['error']}")
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"✅ Success Rate: {success_rate:.1f}%")
        
        return self.tests_passed == self.tests_run

def main():
    tester = CyberSentinelAPITester()
    success = tester.run_all_tests()
    
    # Save detailed results
    with open('/app/backend_test_results.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_tests': tester.tests_run,
            'passed_tests': tester.tests_passed,
            'success_rate': (tester.tests_passed / tester.tests_run * 100) if tester.tests_run > 0 else 0,
            'failed_tests': tester.failed_tests,
            'detailed_results': tester.test_results
        }, f, indent=2)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())