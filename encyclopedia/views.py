from django.shortcuts import render, redirect

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


def search_by_title(request):
    search_term = request.GET.get('q', '')
    all_entries = util.list_entries()
    filtered_entries = []
    entry_found = None

    for entry in all_entries:
        if search_term.lower() == entry.lower():
            entry_found = entry
            break

        if search_term.lower() in entry.lower():
            filtered_entries.append(entry)

    if entry_found is not None or len(filtered_entries) == 0:
        """
            Using the redirect has two advantages:
                - changes the URL to where the entry is at,
                - avoids duplicating the logic to find the entry
        """
        return redirect('get_by_title', title=entry_found)

    return render(request, "encyclopedia/index.html", {
        "entries": filtered_entries
    })


def _does_title_already_exists(title):
    return util.get_entry(title) is not None


def _create_entry(request):
    title = request.POST['title']
    content = request.POST['content']

    if (_does_title_already_exists(title)):
        return (False, "Title already exists.")

    has_title = title != "" and title is not None
    has_content = content != "" and content is not None

    if not has_title:
        return (False, "Title is mandatory")

    if not has_content:
        return (False, "Content is mandatory")

    try:
        util.save_entry(title, content)

        return (True, "")
    except:
        return (False, "Something went wrong with the saving process.")


def new(request):
    try:
        if request.method == 'POST':
            was_successful, failed_reason = _create_entry(request)

            if was_successful:
                title = request.POST['title']

                return redirect('get_by_title', title)
            else:
                return render(request, "encyclopedia/new.html", {
                    "error": failed_reason or "Failed to save, please try again."
                })
        else:
            return render(request, "encyclopedia/new.html")
    except:
        return render(request, "encyclopedia/new.html", {
            "error": "Failed to save, please try again."
        })
