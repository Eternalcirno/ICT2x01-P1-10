import unittest
import auth
import time

class authTest(unittest.TestCase):
    def setUp(self):
        self.auth = auth.Auth('admin','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918')
    
    def testEmptyPass(self):
        self.assertRaisesRegex(NameError, "^Password cannot be empty$" , self.auth.login, "admin", "")

    def testEmptyUser(self):
        self.assertRaisesRegex(NameError, "^Username cannot be empty$" , self.auth.login, "", "admin")

    def testBan(self):
        for i in range(5):
            try:
                self.auth.login("admin", "admin1")
            except:
                continue
        self.assertRaisesRegex(NameError, "^5 invalid tries detected, account locked out. Try again in 5 minutes$" , self.auth.login, "admin", "admin1")

    def testBadCreds(self):
        self.assertRaisesRegex(NameError, "^Invalid username or password$" , self.auth.login, "admin", "admin1")

    def testUnBan(self):
        for i in range(6):
            try:
                self.auth.login("admin", "admin1")
            except:
                continue
        time.sleep(300)
        self.testBadCreds()

    def testLogin(self):
        self.assertEqual(self.auth.login("admin", "admin"), 0)

    def testEmptyNewPass(self):
        self.assertRaisesRegex(NameError, "^New password cannot be empty$" , self.auth.change, "admin", "", "a", "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb")

    def testEmptyConfNewPass(self):
        self.assertRaisesRegex(NameError, "^Confirm new password cannot be empty$" , self.auth.change, "admin", "a", "", "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb")

    def testEmptyOldPass(self):
        self.assertRaisesRegex(NameError, "^Old password cannot be empty$" , self.auth.change, "", "a", "a", "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb")

    def testWrongOldPass(self):
        self.assertRaisesRegex(NameError, "^Incorrect old password$" , self.auth.change, "a", "admin", "admin", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918")

    def testDiffPass(self):
        self.assertRaisesRegex(NameError, "^Passwords do not match$" , self.auth.change, "admin", "ad", "a", "70ba33708cbfb103f1a8e34afef333ba7dc021022b2d9aaa583aabb8058d8d67")

    def testPol(self):
        self.assertRaisesRegex(NameError, "^Password should be 6-20 chars long with upper and lower case characters and special characters$" , self.auth.change, "admin", "ad", "ad", "70ba33708cbfb103f1a8e34afef333ba7dc021022b2d9aaa583aabb8058d8d67")

    def testChange(self):
        self.assertEqual(self.auth.change("admin", "Aaa12*", "Aaa12*","7337ead11dd6981dd6448d27f24cc687bf5d27fae506ab3f4ee80f8ac101f7fb"), 0)

if __name__ == '__main__':
    unittest.main()
