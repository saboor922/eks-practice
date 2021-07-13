# Kubernetes Architecture

![Kubernetes Full Architecture Diagram](./full-kubernetes-model-architecture.png)

# Create an EKS cluster
Using following command from root:

    eksctl create cluster -f cluster.yaml

Eksctl Tool leverages aws cli and aws cloudformation stacks to create your cluster. It can be used to create clusters using managed EC2 instances or Fargate serverless executions

You should get an output that looks something like below:

    [ℹ]  eksctl version 0.31.0
    [ℹ]  using region eu-west-1
    [✔]  using existing VPC (vpc-45b4573c) and subnets (private:[subnet-1788164d subnet-96d28ff0 subnet-7a0d2132] public:[])
    [!]  custom VPC/subnets will be used; if resulting cluster doesn't function as expected, make sure to review the configuration of VPC/subnets
    [ℹ]  using Kubernetes version 1.18
    [ℹ]  creating EKS cluster "my-managed-eks-cluster" in "eu-west-1" region with managed nodes
    [ℹ]  2 nodegroups (managed-ng-1-workers, managed-ng-2-workers) were included (based on the include/exclude rules)
    [ℹ]  will create a CloudFormation stack for cluster itself and 0 nodegroup stack(s)
    [ℹ]  will create a CloudFormation stack for cluster itself and 2 managed nodegroup stack(s)
    [ℹ]  if you encounter any issues, check CloudFormation console or try 'eksctl utils describe-stacks --region=eu-west-1 --cluster=my-managed-eks-cluster'
    [ℹ]  Kubernetes API endpoint access will use default of {publicAccess=true, privateAccess=false} for cluster "my-managed-eks-cluster" in "eu-west-1"
    [ℹ]  2 sequential tasks: { create cluster control plane "my-managed-eks-cluster", 2 sequential sub-tasks: { update CloudWatch logging configuration, 2 parallel sub-tasks: { create managed nodegroup "managed-ng-1-workers", create managed nodegroup "managed-ng-2-workers" } } }
    [ℹ]  building cluster stack "eksctl-my-managed-eks-cluster-cluster"
    [ℹ]  deploying stack "eksctl-my-managed-eks-cluster-cluster"
    [✔]  configured CloudWatch logging for cluster "my-managed-eks-cluster" in "eu-west-1" (enabled types: api, audit, authenticator, controllerManager, scheduler & no types disabled)
    [ℹ]  building managed nodegroup stack "eksctl-my-managed-eks-cluster-nodegroup-managed-ng-2-workers"
    [ℹ]  building managed nodegroup stack "eksctl-my-managed-eks-cluster-nodegroup-managed-ng-2-workers"
    [ℹ]  deploying stack "eksctl-my-managed-eks-cluster-nodegroup-managed-ng-2-workers"
    [ℹ]  deploying stack "eksctl-my-managed-eks-cluster-nodegroup-managed-ng-1-workers"
    [ℹ]  waiting for the control plane availability...
    [✔]  saved kubeconfig as "C:\\Users\\suhaila/.kube/config"
    [ℹ]  no tasks
    [✔]  all EKS cluster resources for "my-managed-eks-cluster" have been created
    [ℹ]  nodegroup "managed-ng-1-workers" has 2 node(s)
    [ℹ]  node "ip-172-31-28-147.eu-west-1.compute.internal" is ready
    [ℹ]  node "ip-172-31-33-248.eu-west-1.compute.internal" is ready
    [ℹ]  waiting for at least 2 node(s) to become ready in "managed-ng-1-workers"
    [ℹ]  nodegroup "managed-ng-1-workers" has 2 node(s)
    [ℹ]  node "ip-172-31-28-147.eu-west-1.compute.internal" is ready
    [ℹ]  node "ip-172-31-33-248.eu-west-1.compute.internal" is ready
    [ℹ]  nodegroup "managed-ng-2-workers" has 2 node(s)
    [ℹ]  node "ip-172-31-20-172.eu-west-1.compute.internal" is ready
    [ℹ]  node "ip-172-31-34-142.eu-west-1.compute.internal" is ready
    [ℹ]  waiting for at least 2 node(s) to become ready in "managed-ng-2-workers"
    [ℹ]  nodegroup "managed-ng-2-workers" has 2 node(s)
    [ℹ]  node "ip-172-31-20-172.eu-west-1.compute.internal" is ready
    [ℹ]  node "ip-172-31-34-142.eu-west-1.compute.internal" is ready
    [ℹ]  kubectl command should work with "C:\\Users\\suhaila/.kube/config", try 'kubectl get nodes'
    [✔]  EKS cluster "my-managed-eks-cluster" in "eu-west-1" region is ready

# Create a kubeconfig 
This is to fetch correct context to communicate with Kube Control Plane. This is done using the EKS update-kubeconfig command.

    aws eks --region eu-west-1 update-kubeconfig --name my-managed-eks-cluster

# Test your Kube Configuration 

Using Kubectl CLI:

    kubectl get svc

You should see a ClusterIP Type.

Ands, to see if our nodes were created properly:

    kubectl get nodes

You should see a total of 4 nodes as configured in the `cluster.yaml` file (from total of `DesiredCapacity` values).

    NAME                                          STATUS   ROLES    AGE   VERSION
    ip-172-31-20-172.eu-west-1.compute.internal   Ready    <none>   11m   v1.18.9-eks-d1db3c
    ip-172-31-28-147.eu-west-1.compute.internal   Ready    <none>   11m   v1.18.9-eks-d1db3c
    ip-172-31-33-248.eu-west-1.compute.internal   Ready    <none>   11m   v1.18.9-eks-d1db3c
    ip-172-31-34-142.eu-west-1.compute.internal   Ready    <none>   11m   v1.18.9-eks-d1db3c

# Updating/Upgrading an existing cluster
 Once you've made any changes to the eks cluster config file, you can update the cluster using:

    eksctl upgrade cluster -f cluster.yaml

 Validate the changes notified in the CLI by using the `approve` flag. This will make the necessary updates in your cluster

 Alternatively, if you are changing the cluster logging configuration, you can update the cluster loggin via CLI command:

    eksctl utils update-cluster-logging -f cluster.yaml --approve

Similarly, using the 'utils' ESK CLI commands, you can update certain portions of your cluster configuration without deleteing and re-creating the cluster again.

# Switching Kubernetes Contexts

Kubernetes contexts works similar to awsume command in the sense that it allows you to switch your current  kubernetes control plane via CLI commands.

These contexts are stored in the '~/.kube/config' file.

To get all kubernetes contexts use the following command:

    kubectl config get-contexts

This will return a list of contexts that kubernetes has stored in your config file.

To switch your current context to another one use the following CLI command:

    kubectl config use-context CONTEXT_NAME

The 'CONTEXT_NAME' is the Name returned from the previous command. 

# Managing Node Labels

EKS Managed Nodegroups supports attaching labels that are applied to the Kubernetes nodes in the nodegroup. This is specified via the labels field in eksctl during cluster or nodegroup creation. Having labels in your nodes or nodegroup 

To set new labels or updating existing labels on a nodegroup:

    eksctl set labels --cluster my-managed-eks-cluster --nodegroup managed-ng-1-workers --labels color=blue
    eksctl set labels --cluster my-managed-eks-cluster --nodegroup managed-ng-2-workers --labels color=green

To unset or remove labels from a nodegroup:

    eksctl unset labels --cluster my-managed-eks-cluster --nodegroup managed-ng-1-workers --labels color

To view all labels set on a nodegroup:

    eksctl get labels --cluster my-managed-eks-cluster --nodegroup managed-ng-1-workers

Alternatively, to view all labels for a node(s) in your cluster using 'kubectl' :

    kubectl get-nodes --show-labels

Alternatively, to set label to a particular node in your cluster 'kubectl' :

    kubectl label nodes <node-name> <label-key>=<label-value>

# Optional: Deploying the Kubernetes Dashboard

The Dashboard UI is not deployed by default. To deploy it, run the following command:

    kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0/aio/deploy/recommended.yaml

# Optional: Accessing the Dashboard UI
To protect your cluster data, Dashboard deploys with a minimal RBAC configuration by default. Currently, Dashboard only supports logging in with a Bearer Token. 

## Fetching Bearer Token
A Bearer Token is necessary to authenticate login to the Kubernetes Dashboard.

This can be fetched using the following CLI Command:

    aws eks get-token --cluster-name my-managed-eks-cluster

You should get an output that looks like something below:

    {"kind": "ExecCredential", "apiVersion": "client.authentication.k8s.io/v1alpha1", "spec": {}, "status": {"expirationTimestamp": "2020-11-17T20:59:03Z", "token": "k8s-aws-v1.aHR0cHM6Ly9zdHMuYW1hem9uYXdzLmNvbS8_QWN0aW9uPUdldENhbGxlcklkZW50aXR5JlZlcnNpb249MjAxMS0wNi0xNSZYLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFTSUFRVUdUSjVSR0NFWUpYQkdJJTJGMjAyMDExMTclMkZ1cy1lYXN0LTElMkZzdHMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDIwMTExN1QyMDQ1MDNaJlgtQW16LUV4cGlyZXM9NjAmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JTNCeC1rOHMtYXdzLWlkJlgtQW16LVNlY3VyaXR5LVRva2VuPUZ3b0daWEl2WVhkekVNMyUyRiUyRiUyRiUyRiUyRiUyRiUyRiUyRiUyRiUyRndFYURIJTJGNmJqMTRQdGNWR2xkMkVTSzVBVklTc3J0ckVKdHVtanlORXFFTzdxck1DNmU3RDl4QW5NdiUyRkJCbjVhbE1ZWTIlMkZRNFJ4ZGs2d1BmMGlUJTJCcnF5M2FUdzJJYzJGS2UzUWxaaVRFakZmVmJLNTZLVE5PayUyRm9QcDhUYjZnSGxxUCUyRlZWU3BBdkRzalolMkYlMkZLS1BLRFNrcGJlS1RFakxqV1BIS2wzWUxYTDg0eTBtcUszRm5xRGJkam41U1p3NmxUQkJyTklNVXFBN0Ewb1JOTHRyMU9RcXRqV2k0RE5CUUpMTUwlMkZyRklRUTA5OFcxcVh5QVMyUzladkloYVFwa2ZkdGROOVlJNk1ZTEVnejJLTXJZMFAwRk1pMnVMTU8zMExVMk5tTDVTeUElMkJLU0JDcjElMkYlMkJwblolMkZrWGs0Wk9FeDdPcFhtd2x2TXMzNWpENUdlbUV0Qno0JTNEJlgtQW16LVNpZ25hdHVyZT03ODc2YjBiYjE2N2UwN2Q5YWRkYzEyNjQ3YzkwZTFkNzI3OGFiNmRlZTZkOWNiNzg3ZjcwMDcyYjZjZjYzMGYx"}}

Copy and keep hold of the `token` value.

## Command line proxy
You can access Dashboard using the kubectl command-line tool by running the following command:

    kubectl proxy

Kubectl will make Dashboard available at http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/.

**__The UI can only be accessed from the machine where the command is executed.__**

Use the bearer token obtained in the previous step to authenticate yourself to the Kubernetes Web UI Dashboard

## Cleanup

TO delete the kubernetes Web UI dashboard created, use the following CLI command:

    kubectl delete -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0/aio/deploy/recommended.yaml

You should see an output similar to:

    namespace "kubernetes-dashboard" deleted
    serviceaccount "kubernetes-dashboard" deleted
    service "kubernetes-dashboard" deleted
    secret "kubernetes-dashboard-certs" deleted
    secret "kubernetes-dashboard-csrf" deleted
    secret "kubernetes-dashboard-key-holder" deleted
    configmap "kubernetes-dashboard-settings" deleted
    role.rbac.authorization.k8s.io "kubernetes-dashboard" deleted
    clusterrole.rbac.authorization.k8s.io "kubernetes-dashboard" deleted
    rolebinding.rbac.authorization.k8s.io "kubernetes-dashboard" deleted
    clusterrolebinding.rbac.authorization.k8s.io "kubernetes-dashboard" deleted
    deployment.apps "kubernetes-dashboard" deleted
    service "dashboard-metrics-scraper" deleted
    deployment.apps "dashboard-metrics-scraper" deleted

# Deploy your Application into K8s cluster nodes
Now, to deploy the flask docker application services, create a `deployment.yaml` file containing the Kubernetes Deployment Object configurations.

## Deploy your stateless application containers
Once created for each app, use the following Kubectl CLI command to deploy your stateless applications:

    kubectl apply -f hello_docker_flask/kubernetes/deployment.yaml
    kubectl apply -f kcom_docker_flask/kubernetes/deployment.yaml

You should see an ouput like below:

    deployment.apps/helloworld-app-deployment created
    deployment.apps/kcom-app-deployment created

## Describe your kubernetes deployments

To describe the status of your deployments:

    kubectl describe deployment helloworld-app-deployment

You should get an output like:

    Name:                   helloworld-app-deployment
    Namespace:              default
    CreationTimestamp:      Tue, 17 Nov 2020 21:19:12 +0000
    Labels:                 app=helloworld
    Annotations:            deployment.kubernetes.io/revision: 1
    Selector:               app=helloworld
    Replicas:               3 desired | 3 updated | 3 total | 0 available | 3 unavailable
    StrategyType:           RollingUpdate
    MinReadySeconds:        0
    RollingUpdateStrategy:  25% max unavailable, 25% max surge
    Pod Template:
    Labels:  app=helloworld
    Containers:
    helloworld-flask-container:
        Image:      saboor922/my_docker_flask:latest
        Port:       8081/TCP
        Host Port:  0/TCP
        Limits:
        cpu:     300m
        memory:  256Mi
        Requests:
        cpu:        100m
        memory:     128Mi
        Environment:  <none>
        Mounts:       <none>
    Volumes:        <none>
    Conditions:
    Type           Status  Reason
    ----           ------  ------
    Available      False   MinimumReplicasUnavailable
    Progressing    True    ReplicaSetUpdated
    OldReplicaSets:  <none>
    NewReplicaSet:   helloworld-app-deployment-7b5cff4c6f (3/3 replicas created)
    Events:
    Type    Reason             Age    From                   Message
    ----    ------             ----   ----                   -------
    Normal  ScalingReplicaSet  2m15s  deployment-controller  Scaled up replica set helloworld-app-deployment-7b5cff4c6f to 3

## List Pods created by deployment label

     kubectl get pods -l app=helloworld

The output should be something like:

    NAME                                         READY   STATUS             RESTARTS   AGE
    helloworld-app-deployment-7b5cff4c6f-ctkpj   1/1     Running            0          4m13s
    helloworld-app-deployment-7b5cff4c6f-ngqtw   1/1     Running            0          4m13s
    helloworld-app-deployment-7b5cff4c6f-x2nhp   1/1     Running            0          4m13s

## Deleting a Deployment

Enter the following Kubectl CLI command:

    kubectl delete deployment helloworld-app-deployment
    kubectl delete deployment kcom-app-deployment

# Create your Kubernetes Services to access your Applications Deployed

You will need to define a `service.yaml` file for each of your flask applications to define the Kubernetes Services that will expose the Applications deployed. The Kubernetes control plane would need some form of a pod selector to integrate our Services to the right Application Containers. In our case, we will be using the __label selector__ of `app: helloworld` OR `app: kcom` to tie these up properly.

Moreover, we will need to deploy these services of type LoadBalancer to create a public facing External IP for our services.

Once done, use the following Kubectl CLI command to create these services:

    kubectl apply -f hello_docker_flask/kubernetes/service.yaml
    kubectl apply -f kcom_docker_flask/kubernetes/service.yaml

## Get a list of Kubernetes Services Running

    kubectl get service

You should get an output like:

    NAME                     TYPE           CLUSTER-IP       EXTERNAL-IP                                                               PORT(S)          AGE
    helloworld-app-service   LoadBalancer   10.100.81.1      a3aaf8f9c71b94d3e9b05d3ad5f37800-427139808.eu-west-1.elb.amazonaws.com    8081:30081/TCP   9m57s
    kcom-app-service         LoadBalancer   10.100.109.207   aa5884e9f488e40b0a4b4fcf29c8ea50-1862341514.eu-west-1.elb.amazonaws.com   8082:30082/TCP   9m46s
    kubernetes               ClusterIP      10.100.0.1       <none>                                                                    443/TCP          142m



# Access your Exposed Services

Now use the `EXTERNAL_IP` along with the `PORT` (Not the NodePort) in a browser to access your service.

Example:

    curl https://a3aaf8f9c71b94d3e9b05d3ad5f37800-427139808.eu-west-1.elb.amazonaws.com:8081 -k


Output:

    * Trying 52.48.18.188...
    * TCP_NODELAY set
    * Connected to a3aaf8f9c71b94d3e9b05d3ad5f37800-427139808.eu-west-1.elb.amazonaws.com (52.48.18.188) port 8081 (#0)
    > GET / HTTP/1.1
    > Host: a3aaf8f9c71b94d3e9b05d3ad5f37800-427139808.eu-west-1.elb.amazonaws.com:8081
    > User-Agent: curl/7.55.1
    > Accept: */*
    >
    * HTTP 1.0, assume close after body
    < HTTP/1.0 200 OK
    < Content-Type: text/html; charset=utf-8
    < Content-Length: 34
    < Server: Werkzeug/1.0.1 Python/3.8.6
    < Date: Tue, 17 Nov 2020 22:42:39 GMT
    <
    This is my Flask App in Kubernetes* Closing connection 0

# EKS Cluster Cleanup

Once your deployment and services have been deleted, you can delete your cluster using the following eksctl command:

    eksctl delete cluster --name=my-managed-eks-cluster

You should see an output like:

    [ℹ]  eksctl version 0.31.0
    [ℹ]  using region eu-west-1
    [ℹ]  deleting EKS cluster "my-managed-eks-cluster"
    [ℹ]  deleted 0 Fargate profile(s)
    [✔]  kubeconfig has been updated
    [ℹ]  cleaning up AWS load balancers created by Kubernetes objects of Kind Service or Ingress
    [ℹ]  2 sequential tasks: { 2 parallel sub-tasks: { delete nodegroup "managed-ng-2-workers", delete nodegroup "managed-ng-1-workers" }, delete cluster control plane "my-managed-eks-cluster" [async] }
    [ℹ]  will delete stack "eksctl-my-managed-eks-cluster-nodegroup-managed-ng-1-workers"
    [ℹ]  waiting for stack "eksctl-my-managed-eks-cluster-nodegroup-managed-ng-1-workers" to get deleted
    [ℹ]  will delete stack "eksctl-my-managed-eks-cluster-nodegroup-managed-ng-2-workers"
    [ℹ]  waiting for stack "eksctl-my-managed-eks-cluster-nodegroup-managed-ng-2-workers" to get deleted
    [ℹ]  will delete stack "eksctl-my-managed-eks-cluster-cluster"
    [✔]  all cluster resources were deleted
