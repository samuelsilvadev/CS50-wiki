from django.shortcuts import render, redirect
import markdown2

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
        "entry": markdown2.markdown(util.get_entry(title)),
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


def _save_entry(request, skip_duplicated_title_check=False):
    title = request.POST['title']
    content = request.POST['content']

    if not skip_duplicated_title_check and _does_title_already_exists(title):
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
    title = request.POST.get('title', '')
    content = request.POST.get('content', '')

    try:
        if request.method == 'POST':
            was_successful, failed_reason = _save_entry(request)

            if was_successful:
                return redirect('get_by_title', title)
            else:
                return render(request, "encyclopedia/new.html", {
                    "error": failed_reason or "Failed to save, please try again.",
                    "title": title,
                    "content": content
                })
        else:
            return render(request, "encyclopedia/new.html")
    except:
        return render(request, "encyclopedia/new.html", {
            "error": "Failed to save, please try again.",
            "title": title,
            "content": content
        })


def edit(request):

    if request.method == 'POST':
        return edit_save(request)
    if request.method == 'GET':
        return edit_get(request)


def edit_get(request):
    title = request.GET.get('q', '')
    markdown = util.get_entry(title)

    if markdown is None:
        return render(request, "encyclopedia/404.html", {
            "title": title
        })

    return render(request, "encyclopedia/edit.html", {
        "content": markdown,
        "title": title
    })


def edit_save(request):
    title = request.POST.get('title', '')
    content = request.POST.get('content', '')

    does_title_exists = util.get_entry(title) is not None

    if not does_title_exists:
        return render(request, "encyclopedia/edit.html", {
            "error": "The title you sent does not exists, please do not tamper with the form.",
            "title": title,
            "content": content
        })

    was_successful, failed_reason = _save_entry(
        request, skip_duplicated_title_check=True)

    if was_successful:
        return redirect('get_by_title', title)
    else:
        return render(request, "encyclopedia/edit.html", {
            "error": failed_reason or "Failed to save, please try again.",
            "title": title,
            "content": content
        })
