from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.shortcuts import render
import markdown2


from . import util


def index(request):
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

def entry_page(request, title):
    page_exist = util.get_entry(title)
    if page_exist:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "entry": markdown2.markdown(page_exist)
        })
    else:
        return render(request, "encyclopedia/title.html", {
            "title": title + " page not found"
        })

