# Rama-

🚀 Rama - Lightweight Container Runtime



Rama is a lightweight, high-performance container runtime designed for modern cloud applications. It enables developers to build, ship, and run applications seamlessly across different environments—without using Docker. 🚀

🔹 Features
✅ Custom Ramafile - Define your containerized applications.
✅ Self-Hosted Registry - Push & Pull images from your own registry or cloud providers.
✅ Networking & Volumes - Create custom networks & persistent storage for containers.
✅ Kubernetes Support - Easily deploy Rama containers in Kubernetes clusters.
✅ Multi-Platform Support - Runs on Linux, macOS, and Windows.

📌 Prerequisites
Before installing Rama, ensure you have:
🔹 Linux/macOS/Windows system
🔹 Python 3.7+ installed
🔹 cURL or Wget for installation

📥 Installation
🔹 Quick Install (Linux/macOS)
bash
Copy
Edit
curl -sSL https://raw.githubusercontent.com/rahu1yadav/Rama-/main/install.sh | bash
🔹 Windows Install
powershell
Copy
Edit
irm https://raw.githubusercontent.com/rahu1yadav/Rama-/main/install.ps1 | iex
Once installed, check the version:

bash
Copy
Edit
rama --version
🛠️ Getting Started
1️⃣ Build an Image
First, create a Ramafile:

dockerfile
Copy
Edit
FROM ubuntu:latest  
RUN apt-get update && apt-get install -y python3  
CMD ["python3", "-m", "http.server"]
Now, build the image:

bash
Copy
Edit
rama build -t myapp .
2️⃣ Run a Container
bash
Copy
Edit
rama run -d --name my-container myapp
3️⃣ List Running Containers
bash
Copy
Edit
rama ps
4️⃣ Stop & Remove a Container
bash
Copy
Edit
rama stop my-container
rama rm my-container
📦 Image Management
Push Image to Registry
bash
Copy
Edit
rama push myapp registry.example.com/myapp
Pull Image from Registry
bash
Copy
Edit
rama pull registry.example.com/myapp
🚀 Kubernetes Deployment
To deploy Rama containers in Kubernetes, create a YAML file:

yaml
Copy
Edit
apiVersion: v1
kind: Pod
metadata:
  name: my-rama-container
spec:
  containers:
    - name: myapp
      image: registry.example.com/myapp
      ports:
        - containerPort: 8080
Apply it with:

bash
Copy
Edit
kubectl apply -f myapp.yaml
🛠️ Advanced Features
1️⃣ Self-Hosted Registry
Set up a Rama Registry to store images:

bash
Copy
Edit
rama registry start
rama push myapp my-registry.local/myapp
2️⃣ Networking
Create a custom network:

bash
Copy
Edit
rama network create my-network
Run a container in the network:

bash
Copy
Edit
rama run --network my-network -d --name webapp myapp
3️⃣ Volumes
Create a persistent volume:

bash
Copy
Edit
rama volume create my-volume
Run a container with the volume:

bash
Copy
Edit
rama run -d --name db-container --volume my-volume:/data my-database
🔧 CLI Commands
Command	Description
rama build -t <image-name> .	Build an image from Ramafile
rama run -d --name <container-name> <image-name>	Run a container
rama ps	List running containers
rama stop <container-name>	Stop a running container
rama rm <container-name>	Remove a stopped container
rama push <image-name> <registry-url>	Push an image to registry
rama pull <registry-url>/<image-name>	Pull an image from registry
rama network create <network-name>	Create a network
rama volume create <volume-name>	Create a volume
📢 Contributing
We welcome contributions! 🎉 Fork the repo, create a branch, and submit a PR.

bash
Copy
Edit
git clone https://github.com/rahu1yadav/Rama-.git
cd Rama-
git checkout -b feature-new
git commit -m "Added new feature"
git push origin feature-new
📄 License
Rama is open-source and licensed under the MIT License.

