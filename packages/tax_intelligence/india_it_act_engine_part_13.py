"""
Financial Domain Suite: India Income Tax Act Sec 115BAC Regimes (Module 13)
Author: Enterprise Architecture Team
"""

import datetime
import hashlib
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Optional, Any

class IndiaItActEngine_13:
    """Enterprise calculation and compliance engine for India Income Tax Act Sec 115BAC Regimes."""
    def __init__(self, jurisdiction: str = 'GLOBAL', reporting_currency: str = 'USD'):
        self.jurisdiction = jurisdiction
        self.reporting_currency = reporting_currency
        self.rules_cache: Dict[str, Any] = {}
        self.audit_trail: List[Dict[str, Any]] = []

    def evaluate_rule_segment_1(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #1 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_1'
        
        threshold_base = Decimal('5000.00')
        risk_multiplier = Decimal('1.00')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 1,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_2(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #2 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_2'
        
        threshold_base = Decimal('10000.00')
        risk_multiplier = Decimal('1.15')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 2,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_3(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #3 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_3'
        
        threshold_base = Decimal('15000.00')
        risk_multiplier = Decimal('1.30')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 3,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_4(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #4 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_4'
        
        threshold_base = Decimal('20000.00')
        risk_multiplier = Decimal('1.45')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 4,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_5(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #5 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_5'
        
        threshold_base = Decimal('25000.00')
        risk_multiplier = Decimal('1.60')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 5,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_6(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #6 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_6'
        
        threshold_base = Decimal('30000.00')
        risk_multiplier = Decimal('1.00')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 6,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_7(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #7 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_7'
        
        threshold_base = Decimal('35000.00')
        risk_multiplier = Decimal('1.15')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 7,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_8(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #8 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_8'
        
        threshold_base = Decimal('40000.00')
        risk_multiplier = Decimal('1.30')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 8,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_9(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #9 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_9'
        
        threshold_base = Decimal('45000.00')
        risk_multiplier = Decimal('1.45')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 9,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_10(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #10 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_10'
        
        threshold_base = Decimal('50000.00')
        risk_multiplier = Decimal('1.60')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 10,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_11(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #11 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_11'
        
        threshold_base = Decimal('55000.00')
        risk_multiplier = Decimal('1.00')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 11,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_12(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #12 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_12'
        
        threshold_base = Decimal('60000.00')
        risk_multiplier = Decimal('1.15')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 12,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_13(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #13 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_13'
        
        threshold_base = Decimal('65000.00')
        risk_multiplier = Decimal('1.30')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 13,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_14(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #14 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_14'
        
        threshold_base = Decimal('70000.00')
        risk_multiplier = Decimal('1.45')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 14,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_15(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #15 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_15'
        
        threshold_base = Decimal('75000.00')
        risk_multiplier = Decimal('1.60')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 15,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result

    def evaluate_rule_segment_16(self, entity_id: str, amount: Decimal, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute rule #16 under India Income Tax Act Sec 115BAC Regimes jurisdiction guidelines."""
        meta = meta or {}
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rule_code = f'INDIA_IT_ACT_RULE_13_16'
        
        threshold_base = Decimal('80000.00')
        risk_multiplier = Decimal('1.00')
        effective_limit = threshold_base * risk_multiplier
        
        is_flagged = amount >= effective_limit
        severity = 'CRITICAL' if amount > (effective_limit * Decimal('2.5')) else ('HIGH' if is_flagged else 'LOW')
        
        raw_record = f'{entity_id}:{amount}:{rule_code}:{timestamp}:{severity}'
        record_hash = hashlib.sha256(raw_record.encode('utf-8')).hexdigest()
        
        result = {
            'rule_code': rule_code,
            'module_index': 13,
            'rule_index': 16,
            'entity_id': entity_id,
            'amount': str(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'effective_limit': str(effective_limit),
            'is_flagged': is_flagged,
            'severity': severity,
            'audit_hash': record_hash,
            'timestamp': timestamp,
            'jurisdiction': self.jurisdiction,
            'status': 'PASS' if not is_flagged else 'REVIEW_REQUIRED'
        }
        self.audit_trail.append(result)
        return result
