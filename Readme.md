In this repository, we will develop Container and Kubernetes artifacts, perform **DL training and DL Inference hosting in GKE: Google Kubernetes Engine.**

*Kubernetes*, is an open-source platform designed to automate the deployment, scaling, and operation of application containers. *Google Kubernetes Engine*[7] is a managed service provided by Google Cloud Platform (GCP) that allows you to deploy, manage, and scale containerized applications using Kubernetes. GKE gives you a Kubernetes environment on Google’s infrastructure, removing the need to install, manage, and operate your own Kubernetes clusters. Key aspects of GKE include:
Managed Kubernetes, Integration with Google Cloud, Scalability, Security, High Availability.

We would be using the code `mnist-rnn` from the `https://github.com/pytorch/examples/tree/main/mnist_rnn` repository.

![kubernetes workflow](https://github.com/srushti98/ml-kubernetes-mnist/blob/main/kubernetes_workflow.png)

We would first create a cluster, attach the PVC file and then run the necessary steps for training and testing the mnist-rnn code.

### PART A: Creation of cluster on GKE[7]
To begin with, we will need to create a kubernetes cluster on Google Kubernetes Engine.

The `kubectl` will be configured in the cloud shell by the following command.
`gcloud container clusters get-credentials <kubernetes-cluster-name>
--zone <zone> --project <project-name>`

Now we can successfully use `kubectl commands`.

For more GCP commands, refer official documentation.

### PART B: Creating and attaching PVC resource to the cluster[8]

1. To attach a PVC, we will need `pvc.yaml` which all specify all the configurations of our persistent storage. Create a `pvc.yaml` in the cloud cluster by `vim pvc.yaml`.
2. In our cloud shell, we will use command `kubectl apply -f pvc.yaml` to apply these configurations to our cluster.
3. We can check using the command,`kubectl get pvc` or `kubectl get pvc mnist-model-pvc` whether our pvc has been successfully bounded with our cluster or not.
4. Thus, our PVC is ready now and successfully bound, we can go ahead with training and inference steps.

### PART C: Training program in kubernetes[8]
For training we will have to create a dockerfile, push the docker image to docker registry, and then create a training.yaml and apply that configuration to the cluster.

1. Build the docker image by `docker build -t trainmnistrnn . --platform=linux/amd64`. (This will name my image as `trainmnistrnn`)
2. Then tag the image by `docker tag trainmnistrnn srush98/trainmnistrnn`
3. Then push the train image to the dockerhub registry by using the command `docker push srush98/trainmnistrnn`
4. Thus your train image is ready to be used by your kubernetes cluster. 
5. Now we will create `train.yaml` in the cloud shell by `vim train.yaml`.
6. Deploy the training job: `kubectl apply -f train.yaml`
7. To check whether training is successful we can see `kubectl get jobs` and `kubectl get
pods`

### PART D: Inferencing (trained program) in kubernetes[8][5][6]
I will be using the gradio library for user interaction. The gradio related code changes have been made in inference code.

1. Build the docker image by `docker build -t infermnistrnnfinal . --platform=linux/amd64`.
2. Then tag the image by `docker tag infermnistrnnfinal srush98/infermnistrnnfinal`.
3. Then push the inference image to the dockerhub registry by using the command
`docker push srushti98/infermnistrnnfinal`.
4. Now, similar to training, we will create `infer.yaml` on our cloud shell using `vim infer.yaml`.
5. Deploy the inference application: `kubectl apply -f infer.yaml`
6. To verify whether the deployment is successful or not we can check `kubectl get deployments` and `kubectl get pods`. The status running tells that the deployment is up and can be consumed by the service.
7. To describe a particular deployment we will use `kubectl describe deployment mnist-inference-deployment`.
8. Our deployment of inference code is successful now we can create our service to use our deployed app and expose it to users to use our inference code.

### PART E: Creating Service on Kubernetes[8]

1. Since our deployment is ready, we will now create a `service.yaml`.
2. Expose the Gradio app: `kubectl apply -f service.yaml`.
3. Verify the service is running properly by `kubectl get service`.
4. Describe the service using `kubectl describe service mnist-inference-service`.
5. Now we can see our service is up and running.
6. The external ip is the ip exposed to the end user for interacting with the application.
7. After this, we have to enable port forwarding, by going to services page in GCP console.
8. Click on `port forwarding`.
9. This will give a command which will enable the forwarding.
10. Once this is entered in the console, it will give a link for deployed app.
11. This will be the url where the app will be deployed and be accessed.
12. We can see the gradio interface[9], upload any image from mnist data and you will see the prediction on the screen as output.

![Screenshot](https://github.com/srushti98/ml-kubernetes-mnist/blob/main/app_screenshot.png)

### References:

[1] Docker official documentation: https://docs.docker.com/desktop/

[2] Blog of deploying an ML model on Docker.
https://towardsdatascience.com/build-and-run-a-docker-container-for-your-machine-learning-model-60209c2d7a7f

[3] MNIST code repo=>
https://github.com/pytorch/examples/tree/main/mnist_rnn

[4] Containzerization wikipedia=>
https://en.wikipedia.org/wiki/Containerization_(computing)

[5] Kubernetes Wikipedia => https://en.wikipedia.org/wiki/Kubernetes

[6] Kubernetes official documentation => https://kubernetes.io/docs/home/

[7] GKE official documentation => https://cloud.google.com/kubernetes-engine?hl=en

[8] Medium blog of deploying containers to kubernetes =>
https://tsai-liming.medium.com/part-3-deploying-your-data-science-containers-to-kubernetes-aaae769144ec

[9] Gradio documentation => https://www.gradio.app/docs/interface

[10] NYU Prof. Hao and Chung's Slides => https://cs.nyu.edu/courses/spring21/CSCI-GA.3033-085/