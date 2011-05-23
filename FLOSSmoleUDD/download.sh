#!/bin/bash
TIME=$(date +%m-%d-%y_%H-%M)
wget --retry-connrefused http://udd.debian.org/udd.sql.gz
gunzip udd.sql.gz
mv udd.sql udd-$TIME.sql
echo udd-$TIME.sql
