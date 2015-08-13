# -*- coding: utf-8 -*-

# django
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.views.generic.edit import FormView

# forms
from analys_users.forms import UsersForm

# utils
from analys_users.utils import check_users


class UsersView(FormView):
    """
        Представление /user_check/
    """
    template_name = 'analys_users/users.html'
    form_class = UsersForm
    success_url = '/res/'

    def form_valid(self, form):
        res = check_users(
            self.request.POST['id_user_1'], self.request.POST['id_user_2']
        )
        self.request.session['res'] = res
        return redirect(self.get_success_url(), res=True)


def res_view(request):
    """
        Представление /res/
    """
    res = request.session.get('res')
    return render_to_response(
        'analys_users/res.html', {'res': res}
    )
