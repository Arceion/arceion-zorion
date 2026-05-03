import re

from django.core.exceptions import ValidationError


__all__ = ['StrongPasswordValidator']


class StrongPasswordValidator:
	"""
	Password strength validator for enforcing strong password requirements.
	
	Configurable requirements:
	- Minimum length
	- Uppercase letters required
	- Lowercase letters required
	- Digits required
	- Special characters required
	
	USAGE EXAMPLE:
	==============
	from arceion.zorion.auth import StrongPasswordValidator
	
	validator = StrongPasswordValidator()
	try:
	    validator.validate(password)
	except ValidationError as e:
	    return Return.badRequest({'errors': e.messages})
	"""
	
	MIN_LENGTH = 12
	REQUIRE_UPPERCASE = True
	REQUIRE_LOWERCASE = True
	REQUIRE_DIGIT = True
	REQUIRE_SPECIAL = True
	
	def validate(self, password, user=None):
		"""
		Validate password against configured requirements.
		
		Args:
		    password: The password string to validate
		    user: Optional user object (for context, currently unused)
		
		Raises:
		    ValidationError: If password doesn't meet requirements
		"""
		errors = []
		
		# Check minimum length
		if len(password) < self.MIN_LENGTH:
			errors.append(f'Password must be at least {self.MIN_LENGTH} characters.')
		
		# Check for uppercase letters
		if self.REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
			errors.append('Password must contain at least one uppercase letter.')
		
		# Check for lowercase letters
		if self.REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
			errors.append('Password must contain at least one lowercase letter.')
		
		# Check for digits
		if self.REQUIRE_DIGIT and not re.search(r'\d', password):
			errors.append('Password must contain at least one digit.')
		
		# Check for special characters
		if self.REQUIRE_SPECIAL and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
			errors.append('Password must contain at least one special character (!@#$%^&*...).')
		
		if errors:
			raise ValidationError(errors)
	
	def get_help_text(self):
		"""Get human-readable help text describing the requirements."""
		requirements = []
		
		if self.MIN_LENGTH:
			requirements.append(f'{self.MIN_LENGTH}+ characters')
		
		if self.REQUIRE_UPPERCASE:
			requirements.append('uppercase letter')
		
		if self.REQUIRE_LOWERCASE:
			requirements.append('lowercase letter')
		
		if self.REQUIRE_DIGIT:
			requirements.append('digit')
		
		if self.REQUIRE_SPECIAL:
			requirements.append('special character')
		
		return f'Password must contain: {", ".join(requirements)}.'
