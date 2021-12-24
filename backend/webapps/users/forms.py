from typing import List 
from typing import Optional 

from fastapi import Request

class UserCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.firstname: Optional[str] = None
        self.lastname: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.email = form.get("email")
        self.firstname = form.get("firstname")
        self.lastname = form.get("lastname")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not len(self.username) > 3:
            self.errors.append("Username should be > 3 characters long")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.firstname or not len(self.firstname) > 3:
            self.errors.append("Firstname should br gt 3 characters long")
        if not self.lastname or not len(self.lastname) > 3:
            self.errors.append("Lastname should br gt 3 characters long")
        if not self.password or not len(self.password) >= 7:
            self.errors.append("Password must be > 7 characters")
        if not self.errors:
            return True
        return False