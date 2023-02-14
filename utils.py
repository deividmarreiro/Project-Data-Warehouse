import boto3
import configparser

config = configparser.ConfigParser()
config.read('dwh.cfg')

options = {
    "aws_access_key_id": config.get("AWS", "AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key":config.get("AWS", "AWS_SECRET_ACCESS_KEY"),
    "region_name":config.get("AWS", "REGION_NAME")
}

iam = boto3.client("iam", **options)

redshift = boto3.client("redshift", **options)

def set_iam_role():
    if not config.has_section("IAM_ROLE"):
        config.add_section("IAM_ROLE")
    
    config["IAM_ROLE"]["ARN"] = iam.get_role(RoleName="redshift_role")["Role"]["Arn"]
    
    print("Setting IAM_ROLE...")
    with open("dwh.cfg", "w") as file:
        config.write(file)

def set_db_host():
    response = redshift.describe_clusters(ClusterIdentifier=config.get("CLUSTER", "CLUSTER_IDENTIFIER"))
    cluster = response["Clusters"][0]
    endpoint = cluster["Endpoint"]["Address"]
    
    config["DB"]["HOST"] = endpoint
    
    print("Setting DB_HOST...")
    with open("dwh.cfg", "w") as file:
        config.write(file)