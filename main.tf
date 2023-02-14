terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 4.16"
    }
  }
}

locals {
    config = file("dwh.cfg")
}

provider "aws" {
  region = "${var.region_name}"
}

resource "aws_iam_role" "redshift_role" {
    name = "${var.iam_name}"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Principal = {
                    Service = "redshift.amazonaws.com"
                }
            }
        ]
    })
}

resource "aws_iam_policy_attachment" "redshift_role_attachment" {
    name = "redshift_role_attachment"
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
    roles = [aws_iam_role.redshift_role.name]
}

resource "aws_security_group" "redshift_security_group" {
    name = "redshift_security_group"
    description = "Authorise redshift cluster access"

    ingress {
        from_port = 5439
        to_port = 5439
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = [ "0.0.0.0/0" ]
    }
}

resource "aws_redshift_cluster" "dwh-cluster" {
    cluster_identifier = "${var.cluster_identifier}"
    database_name = "${var.db_name}"
    master_username = "${var.db_user}"
    master_password = "${var.db_password}"
    node_type = "dc2.large"
    number_of_nodes = 8
    vpc_security_group_ids = [aws_security_group.redshift_security_group.id]
    iam_roles = [aws_iam_role.redshift_role.arn]
    skip_final_snapshot = true
}