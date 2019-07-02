#!/bin/sh

TFE_WORKSPACE_TOKEN=$1

cat > .terraformrc <<EOF
credentials "tfe-poc.apac.squadzero.io" {
  token = "${TFE_WORKSPACE_TOKEN}"
}
EOF
