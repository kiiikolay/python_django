from django.contrib.auth.models import User
import os
from django.db import models
from django.conf import settings
from django.utils.deconstruct import deconstructible
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.core.files import File


@deconstructible
class ProfileAvatarDirectoryPath:
    def __call__(self, instance, filename):
        return "profiles/profiles_{pk}/avatar/{filename}".format(
            pk=instance.pk,
            filename=filename,
        )

profile_avatar_directory_path = ProfileAvatarDirectoryPath()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=profile_avatar_directory_path)

    _avatar_pending = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._avatar_pending = None
        self.old_avatar = None

    def save(self, *args, **kwargs):
        is_new = not self.pk
        if is_new:
            super().save(*args, **kwargs)

        if self.avatar and self._avatar_pending is None:
            self._avatar_pending = self.avatar
            self.avatar = None

        if self._avatar_pending:
            file_path = profile_avatar_directory_path(self, os.path.basename(self._avatar_pending.name))

            if isinstance(self._avatar_pending, File):
                file_content = self._avatar_pending.read()
            elif isinstance(self._avatar_pending, str) and default_storage.exists(self._avatar_pending):
                file_content = default_storage.open(self._avatar_pending, 'rb').read()
            else:
                self._avatar_pending = None
                return

            if isinstance(self._avatar_pending, File):
                new_file_path = default_storage.save(file_path, self._avatar_pending)
            else:
                new_file_path = default_storage.save(file_path, default_storage.open(self._avatar_pending, 'rb'))

            self.avatar = new_file_path
            self._avatar_pending = None

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Profile(pk={self.pk}, name={self.user.username!r})"
