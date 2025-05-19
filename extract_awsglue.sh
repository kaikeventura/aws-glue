#!/bin/bash

set -e

echo "📦 Subindo container do AWS Glue..."
docker run -d --name glue-env amazon/aws-glue-libs:glue_libs_4.0.0_image_01 tail -f /dev/null

echo "📁 Extraindo awsglue do PyGlue.zip dentro do container..."
docker exec glue-env unzip -q /home/glue_user/aws-glue-libs/PyGlue.zip -d /tmp/awsglue

echo "📥 Copiando awsglue para o projeto local..."
docker cp glue-env:/tmp/awsglue/awsglue ./awsglue

echo "🧹 Limpando container..."
docker rm -f glue-env

echo "✅ awsglue disponível localmente em ./awsglue/"
