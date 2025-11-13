from django.db.models.signals import post_save,pre_save
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User,Group
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail


@receiver(post_save,sender=User)
def user_account_activation(sender,instance,created,**kwargs):
    
    if created:
        user=instance
        user.is_active=False
        user.save()
        token=default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}auth/activate/{user.id}/{token}"

        subject = "Account Confirmation"
        message = f"Hello {user.username},\n\nPlease click the link below to activate your account:\n{activation_url}\n\nThank you!"

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")

@receiver(post_save,sender=User)
def assign_role(sender,instance,created,**kwargs):
    if created:
        user_group,create=Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)
        instance.save()

