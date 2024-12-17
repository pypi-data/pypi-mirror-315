import uuid


class Utils:
    @staticmethod
    def generate_id():
        return str(uuid.uuid4())
