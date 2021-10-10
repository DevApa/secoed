from datetime import datetime

import requests
from django.views.generic import TemplateView

from eva.models import Courses
from secoed.settings import TOKEN_MOODLE, API_BASE


def get_all_courses():
    params = {
        "wstoken": TOKEN_MOODLE,
        "wsfunction": "core_course_get_courses",
        "moodlewsrestformat": "json",
    }
    response = requests.get(API_BASE, params)

    if response.ok:
        return response.json()
    else:
        return 0


class CursosEva(TemplateView):
    model = Courses
    template_name = 'evaluaciones/cursos-eva.html'

    def get_courses(self):
        data = {}
        courses = Courses.objects.all()
        if courses.count() > 0:
            return courses
        else:
            data = get_all_courses()
            if data is not None:

                for c in data:
                    if c['shortname'] == 'Pedagogía' or c['shortname'] == 'Didáctica' or c['shortname'] == 'TICs':
                        cours = Courses()
                        cours.idMoodle = c['id']
                        cours.sortName = c['shortname']
                        cours.fullName = c['fullname']
                        cours.categoryName = c['shortname']
                        date = datetime.fromtimestamp(c['startdate'])
                        cours.startDate = date
                        if c['shortname'] == 'Pedagogía':
                            cours.image = 'images/eva/pedagogia.jpg'
                        elif c['shortname'] == 'Didáctica':
                            cours.image = 'images/eva/didactica.jpg'
                        else:
                            cours.image = 'images/eva/tics.png'
                        cours.save()

                courses = Courses.objects.all()
            return courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Cursos Disponibles'
        context['courses'] = self.get_courses()
        context['tics'] = 'images/eva/tics.png'
        context['pedagogia'] = 'images/eva/pedagogia.jpg'
        context['didactica'] = 'images/eva/didactica.jpg'
        return context
