
if __name__ == '__main__':
    import sys, os.path
    sys.path.insert(0, os.path.dirname((os.path.dirname(os.path.abspath(__file__)))))

    import unittest, ModelsTest 

    suite = unittest.TestLoader().loadTestsFromTestCase(ModelsTest.BlogTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
