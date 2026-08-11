from django.db import models


class NameEntry(models.Model):
    name = models.CharField(max_length=255)
    initial = models.CharField(max_length=10, blank=True)
    full_name = models.CharField(max_length=270, blank=True)
    sum_without_initial = models.IntegerField(default=0)
    recursive_sum_without_initial = models.IntegerField(default=0)
    sum = models.IntegerField(default=0)
    recursive_sum = models.IntegerField(default=0)
    source_file = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at', 'name']

    def save(self, *args, **kwargs):
        if self.name and not self.initial:
            self.initial = self.name[:1].upper()
        if self.name:
            self.sum_without_initial = self.calculate_sum(self.name)
            self.recursive_sum_without_initial = self.calculate_recursive_sum(self.sum_without_initial)
            self.full_name = f"{self.name} {self.initial}" if self.initial else self.name
            self.sum = self.calculate_sum(self.full_name)
            self.recursive_sum = self.calculate_recursive_sum(self.sum)
        else:
            self.sum_without_initial = 0
            self.recursive_sum_without_initial = 0
            self.full_name = ''
            self.sum = 0
            self.recursive_sum = 0
        super().save(*args, **kwargs)

    @staticmethod
    def calculate_sum(text: str) -> int:
        values = {
            'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 8, 'g': 3, 'h': 5,
            'i': 1, 'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 7, 'p': 8,
            'q': 1, 'r': 2, 's': 3, 't': 4, 'u': 6, 'v': 6, 'w': 6, 'x': 5,
            'y': 1, 'z': 7,
        }
        total = 0
        for char in text.lower():
            total += values.get(char, 0)
        return total

    @staticmethod
    def calculate_recursive_sum(total: int) -> int:
        while total > 9:
            total = sum(int(digit) for digit in str(total))
        return total

    def __str__(self):
        return self.full_name
