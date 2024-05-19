# mabos/communication/message_serializer.py
import json
from mabos.communication.message import Message

class MessageSerializer:


    def serialize(self, message):
        # Serialize the message object into a format suitable for transmission
        serialized_message = {
            'sender': message.sender,
            'recipient': message.recipient,
            'content': message.content,
            'timestamp': message.timestamp
        }
        return json.dumps(serialized_message)

    def deserialize(self, serialized_message):
        # Deserialize the serialized message back into a message object
        if isinstance(serialized_message, str):
            # Assuming the serialized message is in JSON format
            message_data = json.loads(serialized_message)
            message = Message(
                sender=message_data['sender'],
                recipient=message_data['recipient'],
                content=message_data['content'],
                timestamp=message_data['timestamp']
            )
            return message
        else:
            raise ValueError("Invalid serialized message format")
    