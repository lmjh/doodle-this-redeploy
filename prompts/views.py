from django.http import JsonResponse

from .prompts import generate_prompt


def get_prompt(request):
    """
    A view to generate and return a random drawing prompt
    """
    if request.is_ajax and request.method == "GET":
        # generate a new drawing prompt
        prompt = generate_prompt()
        if prompt:
            # if a prompt is successfully generated, build a result string with
            # it and return
            result = "Draw " + prompt + "!"
            return JsonResponse({"prompt": result}, status=200)
        else:
            # if a prompt could not be generated, return an error
            return JsonResponse(
                {"error": "Unable to generate prompt."}, status=400
            )
