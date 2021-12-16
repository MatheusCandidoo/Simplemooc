from django.db import models
from django.urls import reverse
from django.conf import settings
from simplemooc.core.mail import send_mail_template
from django.utils import timezone


class CourseManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(models.Q(
            name__icontains=query) |
            models.Q(description__icontains=query))


class Course(models.Model):

    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descrição Simples', blank=True)
    about = models.TextField('Sobre o Curso', blank=True)
    startDate = models.DateField('Data de Ínicio', null=True, blank=True)
    image = models.ImageField(
        'Imagem', upload_to='courses/images', null=True, blank=True)
    createdAt = models.DateTimeField('Criado em', auto_now_add=True)
    updatedAt = models.DateTimeField('Atualizado em', auto_now=True)

    objects = CourseManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course:details', kwargs={'slug': self.slug})

    def release_lessons(self):
        today = timezone.now().date()
        return self.lessons.filter(release_date_gte=today)

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name']



class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='Curso', related_name='lessons', on_delete=models.CASCADE)
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank=True)
    number = models.IntegerField('Número (ordem)', blank=True, default = 0)
    release_date = models.DateField('Data de Liberação', blank=True, null=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.name

    def is_available(self):
        if self.release_date:
            today = timezone.now.date()
            return self.release_date>=today
        return True

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']

class Material(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='Aula', related_name='materials',  on_delete=models.CASCADE)
    name = models.CharField('Nome', max_length=100)
    embed_media = models.TextField('Video embedded', blank=True)
    file = models.FileField(upload_to='lessons/materials', verbose_name='Materiais', blank=True, null=True) 

    def is_embedded(self):
        return bool(self.embed_media)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'



class Enrollment(models.Model):

    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Inscrito'),
        (2, 'Cancelado'),
        (3, 'Recusado'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='Usuário', related_name='enrollments', on_delete=models.DO_NOTHING)
    course = models.ForeignKey(
        Course, verbose_name='Curso', related_name='enrollments',  on_delete=models.DO_NOTHING)

    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICES, default=0, blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def active(self):
        self.status = 1
        self.save()

    def is_subscribe(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (
            ('user', 'course'),
        )

class Announcements(models.Model):
    course = models.ForeignKey(Course, verbose_name='Curso',related_name= 'announcements',on_delete=models.CASCADE)
    tittle = models.CharField('Título', max_length=100)
    content = models.TextField('Conteúdo')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.tittle

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']

class Comments(models.Model):
    announcements = models.ForeignKey(Announcements, verbose_name='Anúncio', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuario', related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField('Comentário')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    def __str__(self):
        return '{0}_{1}'.format(self.user,self.announcements.pk)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name = 'Comentários'

def post_save_announcement(instance, created, **kwargs):
    subject = "Novo anúncio no Curso {0}".format(instance.course)
    context = {'announcement': instance}
    template_name = 'courses/announcement_mail.html'
    enrollments = Enrollment.objects.filter(course=instance.course, status=1)
    emails=[]
    for enrollment in enrollments:
        emails.append(enrollment.user.email)
    send_mail_template(subject, template_name, context, emails)

models.signals.post_save.connect(post_save_announcement, sender=Announcements, dispatch_uid='post_save_announcement')