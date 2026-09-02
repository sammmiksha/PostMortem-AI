from typing import Dict, Any

class PreventionValidator:
    def validate_test_code(self, test_code: str) -> bool:
        """Validates that generated test code contains assertion checks."""
        if not test_code:
            return False
        return "def test_" in test_code and "assert" in test_code

    def validate_alert_rule(self, rule_text: str) -> bool:
        """Validates that monitoring rule text contains alert definitions and metrics."""
        if not rule_text:
            return False
        return "alert:" in rule_text and "expr:" in rule_text

    def validate_runbook(self, runbook_text: str) -> bool:
        """Validates that runbook contains required SRE sections."""
        if not runbook_text:
            return False
        required_headers = ["Symptoms", "Diagnosis", "Resolution"]
        return all(h in runbook_text for h in required_headers)

    def validate_package(self, package: Dict[str, Any]) -> Dict[str, bool]:
        return {
            "test_valid": self.validate_test_code(package.get("test_code", "")),
            "alert_valid": self.validate_alert_rule(package.get("alert_rules", "")),
            "runbook_valid": self.validate_runbook(package.get("runbook", ""))
        }
