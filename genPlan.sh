#!/bin/bash

echo "Generating terraform plan file..."

DIR=$1

if [ -z "$DIR" ]
then
   DIR="."
fi

terraform plan -out $DIR/opa/plan/my.plan \
    && terraform show -json $DIR/opa/plan/my.plan > $DIR/opa/plan/my.plan.json \
    && python -m json.tool $DIR/opa/plan/my.plan.json > $DIR/opa/plan/plan.json \
    && rm $DIR/opa/plan/my.plan*
