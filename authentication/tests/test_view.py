from .test_setup import TestSetUp
from authentication.models import User

#testing view

class TestView(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        #sessions for check make request and see can get response from app
        res=self.client.post(self.register_url)
        #running assertion ie checkig
        # import pdb
        # pdb.set_trace()
        self.assertEqual(res.status_code, 400)



    def test_user_can_register_correctly(self):
        res = self.client.post(
            self.register_url, self.user_data, format="json")
        #checking username and email are equal
        self.assertEqual(res.data['email'], self.user_data['email'])
        self.assertEqual(res.data['username'], self.user_data['username'])
        self.assertEqual(res.status_code, 201)

    def test_user_cannot_with_unverified_email(self):
        self.client.post(
            self.register_url, self.user_data, format="json")
        #request to login
        res=self.client.post(self.login_url, self.user_data, format="json")
        # import pdb
        # pdb.set_trace()
        self.assertEqual(res.status_code, 401)

    def test_user_can_login_after_verification(self):
        #response contain data use in register
        response=self.client.post(
            self.register_url, self.user_data, format="json")
        #getting email
        email= response.data['email']
        user=User.objects.get(email=email)
        user.is_verified= True
        user.save()
        res=self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)

        


        