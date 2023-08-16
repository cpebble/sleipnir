from .dutil import DockerEventParser
import time
from pprint import pprint

def callback(ev):
    print("#"*10)
    pprint(ev)

def handle_docker_event(event):
    if event["Action"] == "kill":
        atts = event['Actor']['Attributes']
        print(f"Container {atts['name']} killed")
    if event["Action"] == "start":
        atts = event['Actor']['Attributes']
        print(f"Container {atts['name']} started")

if __name__ == "__main__":
    dep = DockerEventParser()
    print("A")
    dep.start_parsing(handle_docker_event)
    print("B")
    time.sleep(20)
    print("C")
    dep.stop_parsing()


