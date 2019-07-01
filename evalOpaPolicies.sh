#!/bin/bash
docker run -w /app \
	     -v $(pwd)/opa:/app openpolicyagent/opa eval \
       --data /app \
       --format=values \
       data.contino.rules
