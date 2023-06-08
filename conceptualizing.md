# Workflow

0. Create / Authenticate user, keep track on Amazon RDS (relational database service).
1. Develop a project on client rendered website.
2. Send project for build to RESTful API.
3. Project gets stored in Amazon CodeCommit.
4. Project gets included in a cookiecutter flask RESTful API template.
5. Project gets sent to surrogate orsa-builder
6. Docker image gets built.
7. Docker image gets pushed to Amazon ECR (elastic container registry).
    a. On image push, add registry to user database tracking users' images.
8. Usesr requests deployment.
9. Amazon ECS (elastic container service) pulls image from ECR and deploys it.
    a. On image deploy, add registry to user database tracking deployed services.
10. User may add or remove images and deployments from ECR and ECS.
11. Periodically remove unused services (if not on Fargate) and images.

# Implementation details.

## Docker build

orsa-deployer spawns a surrogate worker (lambda) to build the image. The image gets sent back to orsa-deployer and registered to ECR.
We might not need to put these workers behind a load balancer since the expected demand for image builds is fairly low.

## Amazon ECR

Images pushed to ECR are managed exclusively by orsa-deployer. This way users may not view what other images are available, besides the ones exposed on the website.

## Amazon ECS, Fargate, and EC2.

orsa-deployer is able to deploy a service to ECS from an image in ECR. The database should keep track of available images and deployed services, along with the users linked.

Services deployed through ECS can be deployed to Amazon EC2 instances or to Amazon Fargate. Preferably Fargate, as this allows for serverless compute and seamless integration with the load balancer.

Should users be able to choose between EC2 and Fargate? If so, consider how to configure a load balancer for the ec2 instances, though this seems unnecesary.

A container instance on fargate can be configured to never stop running (is this correct?)

CloudWatch should be used to monitor deployments.

## Tech Stack

Should the frontend be included in the multi-container application (docker-compose, services)???

### 1. Website

Because the orsa-deployer is a RESTful API written in flask, the frontend should be separate and work only as means to send requests to the API.
Frontend should be written in React and be CSR (client side rendered), hydrated through requests to the orsa-deployer.

Tools:
- Node
- React
- JS
- React components
- Bootstrap?
- Auth cookkies are sent with every request and can be set to expire from client side. [Article outline](https://medium.com/lightrail/getting-token-authentication-right-in-a-stateless-single-page-application-57d0c6474e3)


#### Logo

[Canva](https://www.canva.com/design/DAFlM9Si3Lg/9FI2O9j9VoLuPI-t84uh7g/edit?utm_content=DAFlM9Si3Lg&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

### 2. orsa-deployer and orsa-builder containers

RESTful APIs written in Flask. Available as containers, run on AWS Lambda, built as multi-container application with docker-compose. Should:

- authenticate the user but be stateless (authentication should be emitted server-side but handled client-side)
- access their repos on Amazon CodeCommit
- manage available images on ECR
- manage deployed services on ECS
- package user projects in cookiecutter template
- send to surrogate orsa-builder (spawn new function so that the build process does not lock or access private data through orsa-deployer)
- Trigger deployments to ECS / Fargate or ECS / EC2
- Keep track of role based access control [Aricle outline](https://developer.auth0.com/resources/code-samples/api/flask/basic-role-based-access-control)

Tools:
- Flask
- Python
- Auth0
- GitHub authentication api
- SQLAlchemy
- Docker
- Docker-compose
- Amazon RDS
- Amazon ECR
- Amazon ECS
- Amazon CodeCommit
- Amazon Fargate
- Amazon Lambda Functions
- Amazon EC2

### 3. State of the art and research

Despite the project being almost entirely software development driven, we should sell it as though it were research driven.

Reference research on:
- The difficulties in OR when selling software or consulting.
- Previous attempts at selling software directly.
- Current attempts at selling SaaS.
- Cloud architecture paradigms and design.
- Cloud architecture in the context of OR.
- Similar solutions (edge impulse, SageMaker, ...)

Pending: find research


# Azure alternatives

|     AWS    |      Azure      |
| ---------- | --------------- |
| RDS        | DB for MySQL    |
| ECR        | ACR             |
| ECS        | Container Apps  |
| CodeCommit | DevOps          |
| Lambda     | Azure Functions |
| EC2        | Azure VMs       |
