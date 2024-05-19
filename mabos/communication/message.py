from datetime import datetime
# The Message class in mabos/agents/message.py represents a message object
# that can be sent between agents using the communication mechanisms
# defined in mabos/communication.py, such as send_message() and receive_message().
# The Message class encapsulates the necessary information for agent communication,
# including the sender, recipient, and content of the message.
class Message:
    def __init__(self, sender, recipient, content):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.timestamp = datetime.now()
        self.conversation_id = None
        self.reply_to = None
        self.language = 'english'
        self.ontology = None
        self.protocol = None

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}: {self.content}"
# The MessageSerializer class in mabos/communication/message_serializer.py
# is responsible for serializing and deserializing Message objects to and from
# a string format, respectively. This allows for the Message object to be
# easily serialized and deserialized for transmission over a network or
# stored in a database.

