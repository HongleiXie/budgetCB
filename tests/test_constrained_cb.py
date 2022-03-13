import unittest

import numpy as np

from budgetcb.constrained_cb import LinUCB
from budgetcb.replay import ReplayEvaluator


class LinUCBTest(unittest.TestCase):
    def setUp(self):
        np.random.seed(2020)
        self.config = {
            "narms": 3,
            "ndims": 3,
            "alpha": 0.1,
            "T": 10,
            "B": 3,
            "dummy_arm": 0,
        }
        self.policy = LinUCB(**self.config)
        self.state = np.random.random(30).reshape(10, 3)
        self.action = np.random.randint(0, 2, 10)
        self.reward = np.random.random(10)

    def test_no_contexts_exception(self):
        with self.assertRaises(ValueError):
            self.policy.update(arm=0, reward=1.0)

    def test_sherman_morrison_update(self):
        context = np.array([1, 0.8, 0.5]).reshape(3, 1)
        old_Aa = np.eye(self.config["ndims"])
        np.testing.assert_equal(self.policy.AaI[0], old_Aa)  # arm 0
        new_Aa = old_Aa + np.dot(context, context.T)
        expected_AaI = np.linalg.inv(new_Aa)
        self.policy.update(arm=0, reward=0.5, context=context, tround=0)
        actual_AaI = self.policy.AaI[0]  # arm 0
        np.testing.assert_almost_equal(expected_AaI, actual_AaI, 15)

    def test_replay_payoffs(self):
        evaluator = ReplayEvaluator(
            policy=self.policy,
            arms=self.action,
            rewards=self.reward,
            contexts=self.state,
        )
        actual_output = evaluator.evaluate()
        expected_output = {"avg_payoff": 0.5719}
        details = evaluator.get_details()
        self.assertAlmostEqual(
            actual_output["avg_payoff"], expected_output["avg_payoff"], places=3
        )
        self.assertEqual(details["match_num"], 6)
        self.assertEqual(details["match_arms"], [0] * 6)
        self.assertEqual(
            ["match_num", "payoff_records", "match_arms"], [x for x in details.keys()]
        )
