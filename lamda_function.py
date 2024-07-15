import os
import logging
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
channel_secret = os.getenv('LINE_CHANNEL_SECRET')

configuration = Configuration(access_token=channel_access_token)
api_client = ApiClient(configuration) 
line_bot_api = MessagingApi(api_client)
handler = WebhookHandler(channel_secret)

def lambda_handler(event, context):

    signature = event["headers"]["x-line-signature"]
    body = event["body"]
    
    @handler.add(MessageEvent, message=TextMessageContent)
    def handle_message(event):
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        message = "Invalid signature. Please check your channel access token/channel secret."
        logger.error(message)
        return {'statusCode': 400,'body': message}
    
    return {'statusCode': 200, 'body': "OK"}
