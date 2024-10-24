from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation_email(order):
    subject = f"Order Confirmation: #{order.order_number}"
    recipient = order.email
    message = f"""
    Dear {order.user_profile.user.get_full_name()},

    Thank you for your order. We've received your payment and processed your order # {order.order_number}.

    Order details:
    - Total: {order.grand_total}
    - Items: {', '.join(f"{item.product.name}: {item.quantity}"
                        for item in order.lineitems.all())}

    We'll send you a separate email with shipping details
    once we ship your order.

    Best regards,
    Daintree Team
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )
