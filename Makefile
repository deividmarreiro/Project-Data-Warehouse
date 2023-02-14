setup:
	terraform plan -out=terraform.tfplan && terraform apply terraform.tfplan && python3 setup.py
destroy:
	terraform destroy