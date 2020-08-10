import cas_server.models as models
from django.contrib.auth import get_user_model

from config import celery_app

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task()
def cas_clean_sessions():
    """Cleans CAS user sessions."""
    models.User.clean_deleted_sessions()
    models.UserAttributes.clean_old_entries()
    models.NewVersionWarning.send_mails()


@celery_app.task()
def cas_clean_tickets():
    """Cleans CAS service, proxy, and proxy granting tickets."""
    models.User.clean_old_entries()
    for ticket_class in [
        models.ServiceTicket,
        models.ProxyTicket,
        models.ProxyGrantingTicket,
    ]:
        ticket_class.clean_old_entries()


@celery_app.task()
def cas_clean_federate():
    """Cleans CAS federate sessions."""
    models.FederatedUser.clean_old_entries()
    models.FederateSLO.clean_deleted_sessions()
