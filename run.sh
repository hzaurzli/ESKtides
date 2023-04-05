#!/bin/bash
source /root/miniconda3/bin/activate R;
echo "Path：$1";
Rscript /home/ESKtides/property.R $1;
conda deactivate;

