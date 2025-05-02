import unittest
from unittest.mock import patch
from app import App

class TestApp(unittest.TestCase):
   def test_password_first(self):
      testApp = App()
      with patch('builtins.input', side_effect=['Te$t123!']):
         result = testApp.passwordCheck('Te$t123!')
         self.assertEqual(result,'Te$t123!' )

   def test_password_multiple(self):
      testApp = App()
      with patch('builtins.input', side_effect=['W3akP$', 'Bukayo Saka 7!', 'W3akPa55w0rd#']):
         result = testApp.passwordCheck('WeakPassword')
         self.assertEqual(result,'W3akPa55w0rd#')
   
   def test_password_none_multiple(self):
      testApp = App()
      with patch('builtins.input', side_effect=['', 'A$$umptions555']):
         result = testApp.passwordCheck('')
         self.assertEqual(result,'A$$umptions555')
   
   def test_password_hasher_verify_pass(self):
      testApp = App()
      testPswd = "L3gendary#"
      testPswdHash = testApp.hashPassword(testPswd)
      self.assertTrue(testApp.hasher.verify(testPswdHash,testPswd))

   def test_password_hasher_verify_fail(self):
      testApp = App()
      testPswd = "L3gendary#"
      testPswdHash = testApp.hashPassword(testPswd)

      with self.assertRaises(Exception) as context:
         testApp.hasher.verify(testPswdHash,"D1ffTe$tPswd")
      
      self.assertTrue('The password does not match the supplied hash' in str(context.exception))

   def test_encryption_decryption_pass(self):
      testApp = App()
      testKey = testApp.genEncryptionKey()
      testPassword = 'Te5tP$wd'
      testHeader = 'Twitter'
      
      test_encryption = testApp.encryptPassword(testPassword,testKey,testHeader)
      test_password_data = test_encryption.split(b'EUREKA')
      test_decryption = testApp.decryptPassword(test_password_data[0],test_password_data[1],test_password_data[2],testKey, testHeader)
      
      self.assertEqual(test_decryption,testPassword)
   
   def test_encryption_decryption_header_fail(self):
      testApp = App()
      testKey = testApp.genEncryptionKey()
      testPassword = 'Te5tP$wd'
      testHeader = 'Twitter'
      
      test_encryption = testApp.encryptPassword(testPassword,testKey,testHeader)
      test_password_data = test_encryption.split(b'EUREKA')
      
      with self.assertRaises(Exception) as context:
         testApp.decryptPassword(test_password_data[0],test_password_data[1],test_password_data[2],testKey, "Instagram")
      
      self.assertTrue('MAC check failed' in str(context.exception))
      
   def test_encryption_decryption_different_key(self):
      testApp = App()
      testKey = testApp.genEncryptionKey()
      testPassword = 'Te5tP$wd'
      testHeader = 'Twitter'
         
      test_encryption = testApp.encryptPassword(testPassword,testKey,testHeader)
      test_password_data = test_encryption.split(b'EUREKA')
      
      diffKey = testApp.genEncryptionKey()
      with self.assertRaises(Exception) as context:
         testApp.decryptPassword(test_password_data[0],test_password_data[1],test_password_data[2],diffKey, "Instagram")
         
      self.assertTrue('MAC check failed' in str(context.exception))

if __name__ == '__main__':
    unittest.main()