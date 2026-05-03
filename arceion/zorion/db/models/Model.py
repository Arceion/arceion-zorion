from django.db import models
from django.utils import timezone

from .Manager import Manager, SoftManager
from .query import QuerySet

__all__ = ['Model']


class Model(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted_at = models.DateTimeField(null=True, blank=True)

	objects = SoftManager()
	all_objects = Manager()

	class Meta:
		abstract = True

	def __repr__(self):
		return f'<{self.__class__.__name__}: {self.__str__()}>'

	def __str__(self):
		return f'{self.pk}'

	def delete(self, *, using=None, keep_parents=False, _depth=0):
		"""
		Soft delete: Mark record as deleted instead of removing it.
		Handles cascading soft deletes with recursion depth protection.
		
		Args:
			using: Database alias
			keep_parents: Unused (kept for Django API compatibility)
			_depth: Internal recursion depth tracker (prevents infinite loops)
		"""
		# Prevent infinite recursion with circular foreign keys
		MAX_RECURSION_DEPTH = 50
		if _depth > MAX_RECURSION_DEPTH:
			raise RuntimeError(
				f'Soft delete recursion depth exceeded: {MAX_RECURSION_DEPTH}. '
				'Possible circular foreign key relationships.'
			)
		
		# Mark as deleting to prevent cycles if same object is referenced multiple times
		if not hasattr(self, '_is_deleting'):
			self._is_deleting = True
		else:
			# Already being deleted in this chain, skip to prevent cycles
			return
		
		try:
			# Mark record as deleted
			self.deleted_at = timezone.now()
			self.save(using=using)

			# Handle cascading soft deletes for related objects
			for related in self._meta.related_objects:
				if related.on_delete == models.CASCADE:
					accessor_name = related.get_accessor_name()
					related_manager = getattr(self, accessor_name)
					# Get all related objects as QuerySet
					related_objects = related_manager.all()
					# Delete each related object (with increased depth)
					for rel_obj in related_objects:
						rel_obj.delete(using=using, _depth=_depth + 1)
		finally:
			# Clean up deletion marker
			if hasattr(self, '_is_deleting'):
				delattr(self, '_is_deleting')

	def hard_delete(self):
		# Perform hard delete
		super().delete()
