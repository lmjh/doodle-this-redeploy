from django.contrib.messages import get_messages


def get_message_array(request):
    """
    Retrieves all messages and adds them to an array to pass to the page
    context
    """

    # find message storage and create an empty array
    storage = get_messages(request)
    message_array = []

    # if there are messages in the storage
    if storage:
        for message in storage:
            # append a dict containing each message and its tag to the array
            message_dict = {
                'message': message.message,
                'tag': message.tags
                }
            message_array.append(message_dict)

    context = {
        'message_array': message_array
    }

    return context
