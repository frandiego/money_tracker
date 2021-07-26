ROJECT_ID:=bank-306009
SERVICE_NAME:=shinyrun
IMAGE:=gcr.io/${ROJECT_ID}/${SERVICE_NAME}
REGION:=europe-north1

build:
	docker image build -t ${IMAGE} .

local: build
	docker container run -p 8080:8080 ${IMAGE}

push:
	docker push ${IMAGE}

deploy:
	gcloud run deploy ${SERVICE_NAME} --image ${IMAGE} --region ${REGION} --platform managed --max-instances 1 --memory 1G

run: build push deploy