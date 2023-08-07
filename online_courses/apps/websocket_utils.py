from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def push_lecture_notification(lecture_uuid, data):
    channel_layer = get_channel_layer()

    group_name = f'lecture_notifications_{lecture_uuid}'

    async_to_sync(channel_layer.group_send)(
        group_name,
        data
    )

