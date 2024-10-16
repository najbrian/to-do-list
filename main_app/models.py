from django.db import models
from django.contrib.auth.models import User

class ToDoItem(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(null=True, blank=True, max_length=100)
    notes = models.CharField(null=True, blank=True, max_length=100)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

class ToDoList(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_todo_lists')
    sharedWithUser = models.ForeignKey(User, on_delete=models.PROTECT, related_name='shared_todo_lists')
    todo_item = models.ForeignKey(ToDoItem, on_delete=models.CASCADE, related_name='todo_items')
    title = models.CharField(max_length=100)
    notes = models.CharField(null=True, blank=True, max_length=100)
    
    def save(self, *args, **kwargs):
        if self.pk:
            original = ToDoList.objects.get(pk=self.pk)
            if self.created_by != original.created_by:
                raise ValueError("Only the user who created the to-do list can update it.")
        super(ToDoList, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("You cannot delete this to-do list.")


