generate: install-generator  ## Generate the SDK from our public openapi spec
	node_modules/.bin/openapi-generator-cli generate -i schema.yaml \
		-g python \
		-o glhub_sdk/generated \
		--additional-properties=packageName=hubaxle_api_client



install-generator: ## Install api code generator
	npm install