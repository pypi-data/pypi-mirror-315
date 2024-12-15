import unittest
from src.storybuilder.postureselector import PostureSelector
from src.storybuilder.characterpostures import CHARACTER_FIGURES

class TestPostureSelector(unittest.TestCase):
    def setUp(self):
        self.selector = PostureSelector()
        self.test_cases = {
            "happy": {
                "dialogue": "尊敬的艾莉，辛苦您帮忙查询一下明天的天气，麻烦您啦！",
                "character": "boy",
                "position": "stand",
                "expected": ["boy-stand-arms-straight-leg-straddle-smilesay-anime", "boy-stand-arms-straight-leg-straight-blinkgrin-anime"]
            },
            "question": {
                "dialogue": "正阳，你怎么一下子对艾莉这么有礼貌了呢？",
                "character": "girl",
                "position": "stand",
                "expected": ["girl-stand-arms-open-leg-straight-question-anime", "girl-stand-left-straight-right-finger1up-leg-crossing-question-anime"]
            },
            "complain": {
                "dialogue": "……",
                "character": "girl",
                "position": "stand",
                "expected": ["boy-stand-arms-straight-leg-straight-complain-anime", "boy-stand-arms-straight-leg-straight-groan-anime"]
            },
            "greeting": {
                "dialogue": "你好，很高兴认识你。",
                "character": "boy",
                "position": "stand",
                "expected": "boy-stand-arms-straight-leg-straight-smilesay-anime"
            },
            "half_body": {
                "dialogue": "你好，很高兴认识你。",
                "character": "boy",
                "position": "half",
                "expected": "boy-half-left-handonhip-right-open-smilesay-anime"
            },
            "girl_happy": {
                "dialogue": "让我们从能力的角度把人工智能分分类，拆开来仔细看看！",
                "character": "girl",
                "position": "stand",
                "expected": "girl-stand-arms-open-leg-straight-blinkgrin-anime"
            }
        }

    def test_get_best_posture(self):
        for case_name, case in self.test_cases.items():
            with self.subTest(case=case_name):
                posture = self.selector.get_best_posture(
                    case["character"], 
                    case["dialogue"], 
                    case["position"]
                )[0]
                
                if isinstance(case["expected"], list):
                    self.assertIn(posture, case["expected"],
                        f"{case_name}: 姿势 {posture} 不在预期列表 {case['expected']} 中")
                else:
                    self.assertEqual(posture, case["expected"],
                        f"{case_name}: 期望 {case['expected']}，但得到 {posture}")

    def test_posture_in_character_figures(self):
        for case_name, case in self.test_cases.items():
            with self.subTest(case=case_name):
                posture = self.selector.get_best_posture(
                    case["character"], 
                    case["dialogue"], 
                    case["position"]
                )[0]
                self.assertIn(posture, CHARACTER_FIGURES[case["character"]], 
                              f"{case_name}: 姿势 {posture} 不在 CHARACTER_FIGURES 中")

    def test_fallback_for_missing_position(self):
        dialogue = "你好，很高兴认识你。"
        result = self.selector.get_best_posture("boy", dialogue, "nonexistent_position")
        self.assertIsNotNone(result, "当指定位置不存在时，应该返回一个回退姿势")
        self.assertIn(result[0], CHARACTER_FIGURES["boy"], "回退姿势应该在CHARACTER_FIGURES中")

    def test_no_matching_character(self):
        dialogue = "你好，很高兴认识你。"
        result = self.selector.get_best_posture("nonexistent_character", dialogue, "stand")
        self.assertIsNone(result, "当角色不存在时，应该返回None")

if __name__ == '__main__':
    unittest.main()
