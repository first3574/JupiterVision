import sys

sys.path.insert(0,'/usr/lib/pyshared/python2.7')

from getting2rectanglesandcomparing import isHotGoal
import cv2
import unittest
import os

class TestHotGoal (unittest.TestCase):
    """
    def test_HotGoals_1 (self):
        for i in os.listdir("Hot Goals"):
            testHotGoals_1 = cv2.imread("Hot Goals/" + i)
            result = isHotGoal(testHotGoals_1)
            if (result == False):
                print i
            self.assertTrue(result)
    """
             
    def test_Hot_1 (self):
        testHot_1 = cv2.imread(r"Hot Goals/HotGoal_Real1.png")
        self.assertTrue(isHotGoal(testHot_1))

    def test_Hot_2 (self):
        testHot_2 = cv2.imread(r"Hot Goals/HotGoal_Real2.png")
        self.assertTrue(isHotGoal(testHot_2))

    def test_HotLeft_1 (self):
        testHotLeft_1 = cv2.imread(r"Hot Goals/HotGoal_Left2.png")
        self.assertTrue(isHotGoal(testHotLeft_1))

    def test_HotLeft_2 (self):
        testHotLeft_2 = cv2.imread(r"Hot Goals/HotGoal_Left3.png")
        self.assertTrue(isHotGoal(testHotLeft_2))

    # NOT HOT GOES HERE
    
    def test_NotHot_1 (self):
        testNotHot_1 = cv2.imread(r"Not Hot Goals/NotHotGoal_Real1.png")
        self.assertFalse(isHotGoal(testNotHot_1))

    def test_NotHot_2 (self):
        testNotHot_2 = cv2.imread(r"Not Hot Goals/NotHotGoal_Real2.png")
        self.assertFalse(isHotGoal(testNotHot_2))
        
    def test_NotHot_3 (self):
        testNotHot_3 = cv2.imread(r"Not Hot Goals/NotHotGoal_Fake1.png")
        self.assertFalse(isHotGoal(testNotHot_3))

    def test_NotHot_4 (self):
        testNotHot_4 = cv2.imread(r"Not Hot Goals/NotHotGoal_Fake2.png")
        self.assertFalse(isHotGoal(testNotHot_4))

    def test_Noise_1 (self):
        testNoise_1 = cv2.imread(r"Not Hot Goals/Noise_1.png")
        self.assertFalse(isHotGoal(testNoise_1))

    def test_Noise_2 (self):
        testNoise_2 = cv2.imread(r"Not Hot Goals/Noise_2.png")
        self.assertFalse(isHotGoal(testNoise_2))

if __name__ == '__main__':
    unittest.main()

# :D
