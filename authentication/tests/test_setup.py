#setting the setup method for test , we need to similar test , include testing data

#utilities for test
from rest_framework.test import APITestCase, APIClient
#reverse takes views name , and give the path
from django.urls import reverse
#faker helps to import dyanmic data instead of static one
from faker import Faker

class TestSetUp(APITestCase):
    #setup and tear down call for every test run were we define variable that access in every test case
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.fake=Faker()
        #creating user data for test
        self.user_data={
            'email':self.fake.email(),
            'username':self.fake.email().split('@')[0],
            'password':self.fake.password(),
        }
        # import pdb
        # pdb.set_trace()

        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()

