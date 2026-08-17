from django.db import models


from django.utils.translation import gettext_lazy as _


class Rashi(models.TextChoices):
    """
    Rashi choices for the NameEntry model.
    Different Rashi values are Dhanur, Kanya, Karka, Kumbha, Makara, Meena, Mesha, Mithuna, Simha, Tula, Vrishabha, Vrishchika, and NONE.
    """
    NONE = 'NONE', _('None')
    DHANUR = 'Dhanur', _('Dhanur')
    KANYA = 'Kanya', _('Kanya')
    KARKA = 'Karka', _('Karka')
    KUMBHA = 'Kumbha', _('Kumbha')
    MAKARA = 'Makara', _('Makara')
    MEENA = 'Meena', _('Meena')
    MESH = 'Mesha', _('Mesha')
    MITHUNA = 'Mithuna', _('Mithuna')
    SIMHA = 'Simha', _('Simha')
    TULA = 'Tula', _('Tula')
    VRISHABHA = 'Vrishabha', _('Vrishabha')
    VRISHCHIKA = 'Vrishchika', _('Vrishchika')

    @classmethod
    def get_name_prefix_map(cls):
        """Name prefix for different rashis."""
        return {
            cls.NONE: [],
            cls.KUMBHA: ['Go', 'Sa', 'Si', 'Su'],
        }


class NameEntry(models.Model):
    class Meta:
        verbose_name = 'Name Entry'
        verbose_name_plural = 'Name Entries'
        ordering = ['-uploaded_at', 'name']

    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True)
    sum = models.IntegerField(default=0)
    recursive_sum = models.IntegerField(default=0)
    source_file = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.sum = self.calculate_sum(self.name)
            self.recursive_sum = self.calculate_recursive_sum(self.sum)
        else:
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
        return self.name
