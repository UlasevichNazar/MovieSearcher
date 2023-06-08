from django.contrib.auth.models import BaseUserManager


class MyCustomManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email=None, username=None, password=None, free_mailing_list=None, paid_mailing_list=None,
                     **extra_fields):
        if not username:
            raise ValueError('Введите ваш Логин')

        if email:
            email = self.normalize_email(email)
        else:
            raise ValueError('Введите ваш email')
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        if free_mailing_list:
            user.free_mailing_list = free_mailing_list
        if paid_mailing_list:
            user.paid_mailing_list = paid_mailing_list

        user.save(using=self._db)
        return user

    def create_user(self, email=None, username=None, password=None, free_mailing_list=None, paid_mailing_list=None,
                    **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, username, password, free_mailing_list, paid_mailing_list, **extra_fields)

    def create_superuser(self, email=None, username=None, password=None, free_mailing_list=None, paid_mailing_list=None,
                         **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, username, password, free_mailing_list, paid_mailing_list, **extra_fields)
