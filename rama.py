import os
import sys
import subprocess
import argparse
import shutil
import pathlib
import http.server
import socketserver
import threading
import signal

# Global variables for image storage
IMAGE_REGISTRY = "/var/rama_registry"
CONTAINER_STORAGE = "/var/containers"
NETWORKS = "/var/rama_networks"
VOLUMES = "/var/rama_volumes"
PROCESS_TRACKER = "/var/rama_pids"  # File to track running container PIDs

# Setup Registry
def setup_registry():
    os.makedirs(IMAGE_REGISTRY, exist_ok=True)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", 5000), handler)
    print("Rama Registry started on port 5000")
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

# Push Image
def push_image(image_name, registry_url):
    image_path = os.path.join(IMAGE_REGISTRY, image_name)
    if os.path.exists(image_path):
        print(f"Pushing {image_name} to {registry_url}...")
        subprocess.run(["scp", "-r", image_path, f"{registry_url}/{image_name}"])
        print("Push successful!")
    else:
        print("Image not found!")

# Pull Image
def pull_image(image_name, registry_url):
    print(f"Pulling {image_name} from {registry_url}...")
    subprocess.run(["scp", "-r", f"{registry_url}/{image_name}", IMAGE_REGISTRY])
    print("Pull successful!")

# Run Container
def run_container(image_name, container_name):
    container_path = os.path.join(CONTAINER_STORAGE, container_name)
    image_path = os.path.join(IMAGE_REGISTRY, image_name)
    if os.path.exists(image_path):
        os.makedirs(container_path, exist_ok=True)
        process = subprocess.Popen(["python3", "-m", "http.server"], cwd=container_path)
        with open(PROCESS_TRACKER, "a") as f:
            f.write(f"{container_name}:{process.pid}\n")
        print(f"Container {container_name} started from {image_name} with PID {process.pid}")
    else:
        print("Image not found!")

# List Running Containers
def list_containers():
    if os.path.exists(PROCESS_TRACKER):
        with open(PROCESS_TRACKER, "r") as f:
            containers = f.readlines()
        print("Running containers:")
        for container in containers:
            print(container.strip())
    else:
        print("No running containers found.")

# Stop Container
def stop_container(container_name):
    if os.path.exists(PROCESS_TRACKER):
        with open(PROCESS_TRACKER, "r") as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            name, pid = line.strip().split(":")
            if name == container_name:
                print(f"Stopping container {container_name} with PID {pid}")
                os.kill(int(pid), signal.SIGTERM)
            else:
                new_lines.append(line)
        with open(PROCESS_TRACKER, "w") as f:
            f.writelines(new_lines)
    else:
        print("Container not found!")

# Remove Container
def remove_container(container_name):
    stop_container(container_name)
    container_path = os.path.join(CONTAINER_STORAGE, container_name)
    if os.path.exists(container_path):
        shutil.rmtree(container_path)
        print(f"Container {container_name} removed")
    else:
        print("Container storage not found")

# Networking Support
def create_network(network_name):
    network_path = os.path.join(NETWORKS, network_name)
    os.makedirs(network_path, exist_ok=True)
    print(f"Network {network_name} created")

def list_networks():
    networks = os.listdir(NETWORKS)
    print("Available networks:", networks)

# Volume Management
def create_volume(volume_name):
    volume_path = os.path.join(VOLUMES, volume_name)
    os.makedirs(volume_path, exist_ok=True)
    print(f"Volume {volume_name} created")

def list_volumes():
    volumes = os.listdir(VOLUMES)
    print("Available volumes:", volumes)

# CLI Management
def main():
    parser = argparse.ArgumentParser(description="Rama Container Tool")
    subparsers = parser.add_subparsers(dest="action")
    
    push_parser = subparsers.add_parser("push", help="Push an image to a registry")
    push_parser.add_argument("--image", required=True, help="Image name")
    push_parser.add_argument("--registry", required=True, help="Registry URL")
    
    pull_parser = subparsers.add_parser("pull", help="Pull an image from a registry")
    pull_parser.add_argument("--image", required=True, help="Image name")
    pull_parser.add_argument("--registry", required=True, help="Registry URL")
    
    build_parser = subparsers.add_parser("build", help="Build an image from Ramafile")
    build_parser.add_argument("--image", required=True, help="Image name")
    build_parser.add_argument("--file", required=True, help="Path to Ramafile")
    
    run_parser = subparsers.add_parser("run", help="Run a container from an image")
    run_parser.add_argument("--image", required=True, help="Image name")
    run_parser.add_argument("--name", required=True, help="Container name")
    
    ps_parser = subparsers.add_parser("ps", help="List running containers")
    
    stop_parser = subparsers.add_parser("stop", help="Stop a running container")
    stop_parser.add_argument("--name", required=True, help="Container name")
    
    rm_parser = subparsers.add_parser("rm", help="Remove a container")
    rm_parser.add_argument("--name", required=True, help="Container name")
    
    network_parser = subparsers.add_parser("network", help="Manage networks")
    network_parser.add_argument("--create", help="Create a network")
    
    volume_parser = subparsers.add_parser("volume", help="Manage volumes")
    volume_parser.add_argument("--create", help="Create a volume")
    
    args = parser.parse_args()
    
    if args.action == "push":
        push_image(args.image, args.registry)
    elif args.action == "pull":
        pull_image(args.image, args.registry)
    elif args.action == "build":
        print("Building images is not implemented yet.")  # Placeholder for build functionality
    elif args.action == "run":
        run_container(args.image, args.name)
    elif args.action == "ps":
        list_containers()
    elif args.action == "stop":
        stop_container(args.name)
    elif args.action == "rm":
        remove_container(args.name)
    elif args.action == "network":
        create_network(args.create)
    elif args.action == "volume":
        create_volume(args.create)
    else:
        parser.print_help()

if __name__ == "__main__":
    setup_registry()
    main()
