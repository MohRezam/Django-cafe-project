from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password, address=None, national_id=None):
        if not phone_number:
            raise ValueError("User must have a phone number")
        
        if not email:
            raise ValueError("User must have an email")
        
        if not full_name:
            raise ValueError("User must have a full name")

        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            full_name=full_name,
            address=address,
            national_id=national_id,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email, full_name, password, address=None, national_id=None):
        user = self.create_user(
            phone_number=phone_number,
            email=email,
            full_name=full_name,
            password=password,
            address=address,
            national_id=national_id,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
# class UserManager(BaseUserManager):
#     def create_user(self, email, phone_number, full_name, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')
#         if not phone_number:
#             raise ValueError('Users must have a phone number')
#         if not full_name:
#             raise ValueError('Users must have a full name')

#         user = self.model(
#             email=self.normalize_email(email),
#             phone_number=phone_number,
#             full_name=full_name,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, phone_number, full_name, password=None):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             phone_number=phone_number,
#             full_name=full_name,
#             password=password,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user    
            
