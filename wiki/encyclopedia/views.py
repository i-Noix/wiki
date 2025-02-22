from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.shortcuts import render
import markdown2
import random

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(
        label="Title for the page", 
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style': 'width: 25%;'
    }))
    textarea = forms.CharField(label="Page Content", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'style': 'height: 90vh; width: 80%;'
    }))

class EditPageForm(forms.Form):
    textarea = forms.CharField(label="Page Content", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'style': 'height: 90vh; width: 80%;'
    }))


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
    # Сценарій у випадку, коли користувач натискає edit_this_page
    if request.method == "POST":
        return HttpResponseRedirect(reverse("edit_page", args=[title]))
   
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
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]
        if util.get_entry(title):
            return render(request, "encyclopedia/new_page.html", {
                "form": form,
                "error": title
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry_page", args=[title]))
    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm()
    })

# Реалізація функції щодо редагування сторінки
def edit_page(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["textarea"]
            util.save_entry(title, new_content)
            return HttpResponseRedirect(reverse("entry_page", args=[title]))

    edit_entry = util.get_entry(title)
    form = EditPageForm(initial={'textarea': edit_entry})
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": edit_entry,
        "form": form
    })

# Реалізація функції рандомної сторінки
def random_page(request):
    entrys = util.list_entries()
    print(entrys)
    return HttpResponseRedirect(reverse("entry_page", args=[random.choice(entrys)]))

