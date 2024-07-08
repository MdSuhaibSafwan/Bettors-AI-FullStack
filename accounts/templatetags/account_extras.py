from django import template

register = template.Library()


@register.simple_tag
def is_user_applicable_for_subscription(user):
	eligible = user.is_eligible_for_next_subscription()
	print(eligible)
	return eligible
