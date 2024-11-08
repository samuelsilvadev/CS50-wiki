from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def get_by_title(request, title):
    markdown = util.get_entry(title)

    if markdown is None:
        return render(request, "encyclopedia/404.html", {
            "title": title
        })

    return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(title),
        "title": title
    })
