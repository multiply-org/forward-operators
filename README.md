# Forward Operators

This repository contains optical and microwave forward operator codes which are used within the MULTIPLY Platform.

In a first step the optical and microwave forward operators will be used within the MULTIPLY platform to retrieve biophysical parameters separately for each domain. In a second step the retrieval schemes of the optical and microwave forward operators will be brought together to accomplish a joint retrieval of specific biophysical parameters.

## Optical Forward Operator
The widely used PROSPECT & SAIL (PROSAIL) model was chosen as a RT-model for the optical domain of the MULTIPLY platform.

The python code for the optical forward operator is implemented in "optical_forward_model.py"

## Microwave Forward Operator
The Water Cloud Model (WCM), as a semi empirical RT-model, was chosen for the first implementation of a RT-model for the microwave domain of the MULTIPLY platform. WCMs can be used to estimate the backscatter of vegetated surfaces accounting separately for vegetation and underlying surface contributions. An advantage of WCMs compared to other RT-models is their low parametrization effort.

The python code for the microwave forward operator is implemented in "sar_forward_model.py"
