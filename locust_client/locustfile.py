import time
from locust import task
from locust_plugins.users.socketio import SocketIOUser
import websocket


class WsUser(SocketIOUser):
    @task
    def ping_task(self):
        self.ws_resp = None
        self.ws_message = None
        self.connect("ws://localhost:1500")
        self.send("ping")
        while not self.ws_resp:
            time.sleep(0.1)
        self.sleep_with_heartbeat(10)

    def send(self, body, name=None, context={}, opcode=websocket.ABNF.OPCODE_TEXT):
        if not name:
            if body == "2":
                name = "2 heartbeat"
            else:
                name = ""
        self.environment.events.request.fire(
            request_type="WSS",
            name=name,
            response_time=None,
            response_length=len(body),
            exception=None,
            context={**self.context(), **context},
        )
        self.ws.send(body, opcode)

    def on_message(self, message):
        print(message)
        self.ws_resp = message

    if __name__ == "__main__":
        host = "127.0.0.1"
