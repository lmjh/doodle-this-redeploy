from django.shortcuts import render
from django.urls import reverse

from accounts.forms import DrawingForm
from accounts.models import Drawing
from prompts.prompts import generate_prompt


def sketchbook(request):
    """A view to display the sketchbook page"""

    # create a dictionary to store urls for javascript functions
    # this dictionary will be output to the template as JSON using the
    # json_script filter, then accessed in javascript with JSON.parse()
    urls = {
        "save_drawing": reverse("save_drawing"),
        "get_drawing": reverse("get_drawing"),
        "get_prompt": reverse("get_prompt"),
    }

    # also create a dictionary to store drawing titles
    titles = {}

    form = None
    saved_drawings = None

    # if user is authenticated
    if request.user.is_authenticated:
        # attach the form to save the current user's drawing into the database
        form = DrawingForm()
        account = request.user.useraccount

        # create an array to store user's saved drawings
        saved_drawings = []

        # search the database for saved drawings and add to array
        for save_slot in range(1, 4):
            # this query resolves to 'None' if no matching record is found
            drawing = Drawing.objects.filter(
                user_account=account, save_slot=save_slot
            ).first()
            saved_drawings.append(drawing)

        # iterate through saved_drawings array
        for count, drawing in enumerate(saved_drawings):
            # set title to the title of the drawing if one is present, or an
            # empty string if no drawing found or drawing doesn't have a title
            if drawing:
                title = drawing.title or ""
            else:
                title = ""
            # save the titles to the titles dictionary
            titles[f"title_{count + 1}"] = title

    # generate a drawing prompt to display on page load
    prompt = generate_prompt()
    if prompt:
        # if a prompt is successfully generated, build a string with it
        prompt = "Draw " + prompt + "!"
    else:
        # if a prompt could not be generated, pass an empty string to template
        prompt = ""

    template = "sketchbook/sketchbook.html"

    context = {
        "form": form,
        "saved_drawings": saved_drawings,
        "urls": urls,
        "titles": titles,
        "prompt": prompt,
    }

    return render(request, template, context)
