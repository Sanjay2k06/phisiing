# backend/engines/intent_engine.py

class IntentEngine:
    """
    Detects the primary malicious intent behind a message.
    Focuses on WHAT the attacker wants, not just keywords.
    """

    def analyze(self, content: str):
        text = content.lower()

        intent = {
            "primary_goal": "Unknown",
            "malicious_intent": False,
            "confidence": 0.0,
            "signals": []
        }

        # Money extraction intent
        if any(word in text for word in ["fee", "payment", "pay", "processing fee", "transfer"]):
            intent["primary_goal"] = "Extract Money"
            intent["malicious_intent"] = True
            intent["confidence"] = 0.90
            intent["signals"].append("Requests direct or indirect payment")

        # Credential theft intent
        elif any(word in text for word in ["verify", "login", "password", "otp", "account access"]):
            intent["primary_goal"] = "Steal Credentials"
            intent["malicious_intent"] = True
            intent["confidence"] = 0.85
            intent["signals"].append("Requests account verification or credentials")

        # Personal data harvesting
        elif any(word in text for word in ["ssn", "aadhar", "pan", "id proof"]):
            intent["primary_goal"] = "Harvest Personal Data"
            intent["malicious_intent"] = True
            intent["confidence"] = 0.80
            intent["signals"].append("Requests sensitive personal information")

        return intent
