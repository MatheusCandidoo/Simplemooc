from typing import ContextManager
from django.shortcuts import render, get_object_or_404, redirect
from .models import Announcements, Course, Enrollment, Lesson, Material
from .forms import CommentForm, ContactCourse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import enrollment_required


def courses(request):
    courses = Course.objects.all()
    template_name = 'courses/index.html'
    context = {'courses': courses}
    return render(request, template_name, context)


def details(request, slug):

    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            form.send_mail(course)
            context['isValid'] = True
            form = ContactCourse()
    else:
        form = ContactCourse()

    context['course'] = course
    context['form'] = form
    template_name = 'courses/details.html'

    return render(request, template_name, context)


@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course)
    if created:
        enrollment.active()
        messages.success(
            request, 'Você foi inscrito no curso {0} com sucesso!'.format(course.name))
    else:
        messages.info(
            request, 'Você já se inscreveu para o curso {0}'.format(course.name))
    return redirect('accounts:dashboard')


@login_required
@enrollment_required
def announcements(request, slug):
    context = {}
    course = request.course
    template_name = 'courses/announcements.html'
    context['course'] = course
    context['announcements'] = course.announcements.all()
    context['enrollments'] = Enrollment.objects.filter(user=request.user)
    return render(request, template_name, context)


@login_required
def undo_enrollment(request, slug):
    context = {}
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course=course)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'A sua incrição no curso {0} foi cancelada'.format(course))
        return redirect('accounts:dashboard')

    context['course'] = course
    template_name = 'courses/undo_enrollment.html'
    return render(request, template_name, context)


@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    context = {}
    course = request.course
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False);
        comment.user = request.user
        comment.announcements = announcement
        comment.save()
        form = CommentForm()

    template_name = 'courses/show_announcements.html'
    context['course'] = course
    context['announcement'] = announcement
    context['form'] = form

    return render(request, template_name, context)

@login_required
@enrollment_required
def show_lessons(request, slug):
    course = request.course
    if request.user.is_staff:
        lessons = course.lessons.all()
    else:
        lessons = course.release_lessons()
    template_name = 'courses/lessons.html'
    context = {'course':course,
                'lessons':lessons}
    return render(request,template_name, context)

@login_required
@enrollment_required
def show_lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(Lesson, pk=pk, course=course)
    template_name = 'courses/lesson.html'
    context = {'course':course,
                'lesson': lesson}
    return render(request, template_name, context)

@login_required
@enrollment_required
def show_material(request, slug, pk):
    course = request.course
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Esta material não está disponível!')
        return redirect('course:lesson', slug=course.slug, pk=lesson.pk)
    if not material.is_embedded():
        return redirect(material.file.url)
    template_name = 'courses/material.html'
    context = {'course':course,
            'lesson':lesson,
            'material':material,}
    return render(request, template_name, context)
    
