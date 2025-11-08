import json
from channels.generic.websocket import AsyncWebsocketConsumer


class CallConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time video call functionality.
    Manages user connections, call signaling, and ICE candidate exchange.
    """

    async def connect(self):
        """
        Handles initial WebSocket connection.
        Accepts the connection and sends a confirmation message to the client.
        """
        await self.accept()
        await self.send(
            text_data=json.dumps(
                {"type": "connection", "data": {"message": "Connected"}}
            )
        )

    async def disconnect(self, close_code):
        """
        Handles WebSocket disconnection.
        Removes the user from their associated channel group.
        """
        await self.channel_layer.group_discard(self.my_name, self.channel_name)

    async def receive(self, text_data):
        """
        Processes incoming WebSocket messages from clients.
        Handles different types of events: login, call initiation, call answering, and ICE candidates.
        """
        text_data_json = json.loads(text_data)
        eventType = text_data_json["type"]

        if eventType == "login":
            # Handle user login: Add user to their personal channel group
            name = text_data_json["data"]["name"]
            self.my_name = name
            await self.channel_layer.group_add(self.my_name, self.channel_name)

        if eventType == "call":
            # Handle outgoing call: Notify the callee about the incoming call
            name = text_data_json["data"]["name"]
            print(self.my_name, "is calling", name)
            await self.channel_layer.group_send(
                name,
                {
                    "type": "call_received",
                    "data": {
                        "caller": self.my_name,
                        "rtcMessage": text_data_json["data"]["rtcMessage"],
                    },
                },
            )

        if eventType == "answer_call":
            # Handle call answer: Forward answer to the original caller
            caller = text_data_json["data"]["caller"]
            await self.channel_layer.group_send(
                caller,
                {
                    "type": "call_answered",
                    "data": {"rtcMessage": text_data_json["data"]["rtcMessage"]},
                },
            )

        if eventType == "ICEcandidate":
            # Handle ICE candidate exchange between peers
            user = text_data_json["data"]["user"]
            await self.channel_layer.group_send(
                user,
                {
                    "type": "ICEcandidate",
                    "data": {"rtcMessage": text_data_json["data"]["rtcMessage"]},
                },
            )

    async def call_received(self, event):
        """
        Notifies a user about an incoming call.
        """
        print("Call received by", self.my_name)
        await self.send(
            text_data=json.dumps({"type": "call_received", "data": event["data"]})
        )

    async def call_answered(self, event):
        """
        Notifies the caller that their call has been answered.
        """
        print(self.my_name, "'s call answered")
        await self.send(
            text_data=json.dumps({"type": "call_answered", "data": event["data"]})
        )

    async def ICEcandidate(self, event):
        """
        Forwards ICE candidates between peers for WebRTC connection establishment.
        """
        await self.send(
            text_data=json.dumps({"type": "ICEcandidate", "data": event["data"]})
        )
