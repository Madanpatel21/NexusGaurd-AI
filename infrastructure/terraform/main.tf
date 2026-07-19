terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_eks_cluster" "nexusguard" {
  name     = "nexusguard-cluster"
  role_arn = aws_iam_role.cluster.arn
  # ...
}
