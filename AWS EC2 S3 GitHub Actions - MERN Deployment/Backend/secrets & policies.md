# 🔐 Configurations and Secrets

Ensure the following secrets and configurations are added to your GitHub Actions or environment variables.

### GitHub Secrets

| Secret Key             | Description                                                   |
|------------------------|---------------------------------------------------------------|
| `AWS_ACCESS_KEY_ID`    | Your AWS access key                                           |
| `AWS_SECRET_ACCESS_KEY`| Your AWS secret key                                           |
| `AWS_REGION`           | AWS region (e.g., `us-east-1`)                                |
| `ECR_REPOSITORY`       | ECR repository name (e.g., `node-backend`)                    |
| `ECR_REGISTRY`         | ECR registry (e.g., `123456789012.dkr.ecr.us-east-1.amazonaws.com`) |
| `IMAGE_TAG`            | Docker image tag (e.g., `latest`)                            |
| `EC2_HOST`             | EC2 instance public IP or DNS                                 |
| `EC2_USER`             | EC2 SSH username (e.g., `ec2-user`)                           |
| `EC2_SSH_KEY`          | Base64-encoded EC2 private SSH key                            |
| `HOST_URL`             | SonarQube server URL                                          |
| `PROJECT_KEY`          | SonarQube project key                                         |
| `SONAR_TOKEN`          | SonarQube authentication token                                |

---


# Required IAM User Permissions

- `AmazonEC2FullAccess`  
  _Access to manage EC2 instances._

- `AmazonEC2ContainerRegistryFullAccess`  
  _Manage and push images to ECR._

- `SecretsManagerReadWrite`  
  _Read/write access to AWS Secrets Manager._

- `CloudWatchLogsFullAccess` _(Optional)_  
  _Enable logging and monitoring._

# Required IAM Role Policies (for EC2 Role)

- `AmazonEC2ContainerRegistryPowerUser`  
- `AmazonElasticContainerRegistryPublicReadOnly`  
- `SecretsManagerReadWrite` 

