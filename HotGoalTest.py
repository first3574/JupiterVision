from getting2rectanglesandcomparing import isHotGoal
import cv2
import unittest

class TestHotGoal (unittest.TestCase):
    def test_Hot_1 (self):
        testHot_1 = cv2.imread(r"Hot Goals\HotGoal_Real.png")
        self.assertTrue(isHotGoal(testHot_1))

if __name__ == "__main__":
    unittest.main()
