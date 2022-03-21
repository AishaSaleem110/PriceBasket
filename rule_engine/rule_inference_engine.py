from typing import List
from basket.basket_state import BasketState
from logs.logging import CustomLogging
from rule_engine.condition_rule import ConditionRule
from rule_engine.custom_operator import CustomOperator


class RuleInferenceEngine:
    """
    This class represents an inference engine which checks if rules/conditions are met
    Created a separate entity as it can be extended and following responsibility driven design pattern, responsibility to
    check conditions should be separate.

    Interpretations of CustomOperators are defined in this class
    """

    @staticmethod
    def equal(value, required_value) -> bool:
        return value == required_value

    @staticmethod
    def equal_or_greater(value, required_value) -> bool:
        return value >= required_value

    @staticmethod
    def all_conditions_satisfy(conditions: List[ConditionRule], basket: BasketState) -> bool:
        assessment = []
        for condition in conditions:
            try:
                match condition.operator:
                    case CustomOperator.Equal:
                        result: bool = RuleInferenceEngine.equal(condition.quantity, basket.purchased_quantity)
                        assessment.append(result)

                    case CustomOperator.EqualOrGreater:
                        result: bool = RuleInferenceEngine.equal_or_greater(condition.quantity, basket.purchased_quantity)
                        assessment.append(result)
            except Exception as e:
                CustomLogging.log_error(e)
        return all(assessment)
