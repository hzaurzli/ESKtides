#!/bin/bash
source /root/miniconda3/bin/activate python3;
echo "Path: $1";
/home/SCRATCH-1D_1.1/bin/run_SCRATCH-1D_predictors.sh $1 /home/ESKtides/static/structure/test.out 2;
conda deactivate;
