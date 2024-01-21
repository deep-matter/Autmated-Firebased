import firebase
from Creditials import Creditials

class FirebaseConfig:
    def __init__(self, config):
        self.config = config
        self.app = None
        self.auth = None

    def initialize_app(self):
        """
        Initialize the Firebase app.
        """
        if not self.app:
            self.app = firebase.initialize_app(self.config)
            print("Firebase app initialized successfully.")

    def get_auth_instance(self):
        """
        Get the Firebase Authentication instance.

        Returns:
        - auth: Firebase Authentication instance.
        """
        if not self.auth:
            self.auth = self.app.auth()
            print("Firebase Authentication instance obtained.")
        return self.auth

if __name__ == "__main__":

    firebase_config = FirebaseConfig(Credentials)

    firebase_config.initialize_app()

    auth_instance = firebase_config.get_auth_instance()

