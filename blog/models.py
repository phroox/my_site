from django.conf import settings
from django.db import models
from django.utils import timezone
#from django.db.models.functions import Now

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )
# Modelo de dados para postagens de blog
class Post(models.Model):
    class Status(models.TextChoices): #classe de enumeração Status subclassificando models.TextChoices
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey( #define um relacionamento muitos para um com o modelo de usuário padrão, o que significa que cada postagem é escrita por um usuário e um usuário pode escrever qualquer número de postagens
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # especifica o comportamento a adotar quando o objeto referenciado for excluído. Isso não é específico do Django; é um padrão SQL. Usando CASCADE, você especifica que quando o usuário referenciado for excluído, o banco de dados também excluirá todas as postagens de blog relacionadas. 
        related_name='blog_posts' # para especificar o nome do relacionamento reverso, de Usuário para Postagem. Isso nos permitirá acessar objetos relacionados facilmente a partir de um objeto de usuário usando a notação user.blog_posts. 
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now) #publish = models.DateTimeField(db_default=Now()) #Django 5
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status, 
        default = Status.DRAFT  #Usamos DRAFT como opção padrão para este campo.        
    )
    objects = models.Manager() #The default manager
    published = PublishedManager() # Our custom manager.

class Meta:
    ordering = ['-publish'] # Ordem decrescente
    indexes = [
        models.Index(fields=['-publish']), # definir um índice de banco de dados para o campo de publicação. permite definir índices de banco de dados para o seu modelo, que podem compreender um ou vários campos, em ordem crescente ou decrescente
    ]

def __str__(self):
    return self.title

