import ntpath
from logging import getLogger
from typing import Optional

from NEMO.models import User
from NEMO.utilities import EmailCategory, create_email_log
from NEMO.views.customization import get_media_file_contents
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import Context, Template, TemplateDoesNotExist
from django.template.loader import render_to_string

adapter_logger = getLogger(__name__)


class NEMOAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        """
        Checks whether the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse
        """
        return False

    def get_from_email(self):
        return getattr(settings, "SERVER_EMAIL", settings.DEFAULT_FROM_EMAIL)

    def add_message(self, request, *args, **kwargs):
        # Override this method to make it safe in case no request is passed
        if request:
            super().add_message(request, *args, **kwargs)

    def render_mail(self, template_prefix, email, context, headers=None):
        """
        Overridden to use render_from_media. this is the only change from original method
        """
        to = [email] if isinstance(email, str) else email
        subject = self.render_from_media("{0}_subject.txt".format(template_prefix), context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        from_email = self.get_from_email()

        bodies = {}
        for ext in ["html", "txt"]:
            try:
                template_name = "{0}_message.{1}".format(template_prefix, ext)
                bodies[ext] = self.render_from_media(
                    template_name,
                    context,
                    self.request,
                ).strip()
            except TemplateDoesNotExist:
                if ext == "txt" and not bodies:
                    # We need at least one body
                    raise
        if "txt" in bodies:
            msg = EmailMultiAlternatives(subject, bodies["txt"], from_email, to, headers=headers)
            if "html" in bodies:
                msg.attach_alternative(bodies["html"], "text/html")
        else:
            msg = EmailMessage(subject, bodies["html"], from_email, to, headers=headers)
            msg.content_subtype = "html"  # Main content is now text/html
        return msg

    def render_from_media(self, template_name, context, request=None):
        """Try to find the template in media folder. if it doesn't exists, keep original behavior"""
        file_name = ntpath.basename(template_name)
        email_contents = get_media_file_contents(file_name)
        if email_contents:
            return Template(email_contents).render(Context(context))
        else:
            # original behavior, look in template folder
            return render_to_string(template_name, context, request)

    def send_mail(self, template_prefix, email, context):
        # Overriding to use NEMO's email logger
        ctx = {
            "email": email,
            "current_site": get_current_site(self.request),
        }
        ctx.update(context)
        msg = self.render_mail(template_prefix, email, ctx)
        if msg.recipients():
            email_record = create_email_log(msg, EmailCategory.SYSTEM)
            try:
                msg.send()
            except Exception as e:
                email_record.ok = False
                raise
            finally:
                email_record.save()


class NEMOSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        return False

    def pre_social_login(self, request, sociallogin):
        if settings.AUTO_CONNECT_VERIFIED_EMAIL:
            provider = (
                sociallogin.account.provider
                if sociallogin and sociallogin.account and sociallogin.account.provider
                else "No Provider"
            )

            # social account already exists, so this is just a login
            if sociallogin.is_existing:
                adapter_logger.debug(f"{provider} social account already exists, sending to login")
                return

            # some social logins don't have an email address
            if not sociallogin.email_addresses:
                adapter_logger.debug(
                    f"{provider} does not provide email address, the user cannot be logged in securely"
                )
                return

            # find the first verified email that we get from this sociallogin
            verified_email: Optional[str] = None
            for email in sociallogin.email_addresses:
                if email.verified:
                    verified_email = email.email
                    break

            # if not found, take a look in extra data
            if not verified_email and sociallogin.account and sociallogin.account.extra_data:
                extra_data = sociallogin.account.extra_data
                if "email_verified" in extra_data and "email" in extra_data and bool(extra_data["email_verified"]):
                    verified_email = extra_data["email"]

            # if the provider emails are force-trusted, use the first one that was provided
            provider_configuration = getattr(settings, "SOCIALACCOUNT_PROVIDERS", {}).get(provider) if provider else {}
            if not verified_email and provider and provider_configuration:
                trust_emails = provider_configuration.get("trust_emails", False)
                if trust_emails:
                    verified_email = sociallogin.email_addresses[0].email if sociallogin.email_addresses else None

            # no verified emails found, nothing more to do
            if not verified_email:
                adapter_logger.debug(f"{provider} did not provide a verified email")
                return
            adapter_logger.debug(f"{verified_email} was provided as a verified email by {provider}")

            # check first if given email address already exists as a verified email on an active existing user's account
            verified_user: Optional[User] = None
            try:
                existing_email = EmailAddress.objects.get(
                    email__iexact=verified_email, verified=True, user__is_active=True
                )
                verified_user = existing_email.user
            except EmailAddress.DoesNotExist:
                # next check if there is a superuser with that email, if the setting is enabled
                if settings.TRUST_SUPERUSERS_EMAIL:
                    try:
                        superuser = User.objects.get(is_active=True, is_superuser=True, email__iexact=verified_email)
                        EmailAddress.objects.update_or_create(
                            user=superuser, email=verified_email, verified=False, defaults={"verified": True}
                        )
                        verified_user = superuser
                    except User.DoesNotExist:
                        pass

            # no user found with a verified email, nothing more to do
            if not verified_user:
                adapter_logger.debug(f"could not find a user with the verified email {verified_email}")
                return
            adapter_logger.debug(f"found user {verified_user} with the verified email {verified_email}")
            adapter_logger.debug(f"connecting and login in {verified_user}")

            # we found a user, connect this new social login
            sociallogin.connect(request, verified_user)

    def on_authentication_error(self, *args, exception=None, **kwargs):
        adapter_logger.exception(exception)
