from django.shortcuts import render
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    page_exist = util.get_entry(title)
    if page_exist:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "entrie": markdown2.markdown(page_exist)
        })
    else:
        return render(request, "encyclopedia/title.html", {
            "title": title + " page not found"
        })