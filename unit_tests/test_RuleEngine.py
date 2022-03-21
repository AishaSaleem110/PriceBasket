import unittest
from basket.basket_state import BasketState, BilledState
from rule_engine.custom_operator import CustomOperator
from rule_engine.rule_inference_engine import RuleInferenceEngine
from rule_engine.condition_rule import ConditionRule


class TestRuleEngine(unittest.TestCase):

    def test_check_all_Conditions_satisfy_method(self):
        basket = BasketState("soup", 2, BilledState.Unprocessed)
        c1 = ConditionRule(CustomOperator.Equal, "3944c2df-6a87-46e6-86a4-da45b0d371d3", 2)
        self.assertEqual(True, RuleInferenceEngine.all_conditions_satisfy([c1], basket))

    def test_check_all_Conditions_satisfy_method_negative_case(self):
        basket = BasketState("soup", 2, BilledState.Unprocessed)
        c1 = ConditionRule(CustomOperator.Equal, "3944c2df-6a87-46e6-86a4-da45b0d371d3", 3)
        self.assertEqual(False, RuleInferenceEngine.all_conditions_satisfy([c1], basket))

    if __name__ == '__main__':
        # begin the unittest.main()
        unittest.main()
