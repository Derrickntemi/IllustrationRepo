import unittest
import employee  # import employee.py


class TestEmployee(unittest.TestCase):
    # #executed before every test, for isntance used when testing persistence of an object
    # def setUpClass(cls):
    #     return super().setUpClass()
    # #decorator @classmethod
    # setUpClass = classmethod(setUpClass)
    # #executed after every test
    # def tearDownClass(cls):
    #     return super().tearDownClass()
    # #decorator @classmethod
    # tearDownClass = classmethod(tearDownClass)

    # executed before every test method
    def setUp(self):
        self.employee_1 = employee.Employee('Derrick', 'kimathi')
        self.employee_2 = employee.Employee('austin', 'mutuma')

        # test object creation
        self.assertIsInstance(self.employee_1, employee.Employee)
        self.assertIsInstance(self.employee_2, employee.Employee)

    # exceuted after every test method

    def tearDown(self):
        pass

    # test email method
    def test_email(self):
        self.assertEqual(self.employee_1.email, 'Derrick.kimathi@email.com')
        self.assertEqual(self.employee_2.email, 'austin.mutuma@email.com')

    # test fullname method
    def test_fullname(self):
        self.assertEqual(self.employee_1.fullname, 'Derrick kimathi')
        self.assertEqual(self.employee_2.fullname, 'austin mutuma')


if __name__ == '__main__':
    unittest.main()
