from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.shortcuts import render
import markdown2

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title for the page")
    textarea = forms.CharField(widget=forms.Textarea)


def index(request):
    # Реалізація поля пошуку та переходу на сторінку статті чи виведення списку назв статтей, які збігаються з введеним текстом у пошуку
    if request.method == "POST":
        form = request.POST.get("q")
        if form:
            page_find = util.get_entry(form)
            if page_find:
                return HttpResponseRedirect(reverse("entry_page", args=[form]))
            else:
                entryList = util.list_entries()
                coincideList = []
                for entry in entryList:
                    if form.lower() in entry.lower():
                        coincideList.append(entry)
                return render(request, "encyclopedia/search_result.html", {
                    "entries": coincideList,
                    "title": form
                })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Реалізація переходу на сторінку статті
def entry_page(request, title):
    page_exist = util.get_entry(title)
    if page_exist:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "entry": markdown2.markdown(page_exist)
        })
    else:
        return HttpResponseRedirect(reverse("error_page", args=[title]))
    
# Реалізація сторінки з помилкою
def error_page(request, title):
    return render(request, "encyclopedia/error_page.html", {
        "error": title
    })

# Реалізація функції щодо створення нової сторінки
def new_page(request):
    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm()
    })

