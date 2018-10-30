# Forward Operators

This repository contains optical and microwave forward operator codes which are used within the MULTIPLY Platform.

In a first step the optical and microwave forward operators will be used within the MULTIPLY platform to retrieve biophysical parameters separately for each domain. In a second step the retrieval schemes of the optical and microwave forward operators will be brought together to accomplish a joint retrieval of specific biophysical parameters.

## Optical Forward Operator
The widely used PROSPECT & SAIL (PROSAIL) model was chosen as a RT-model for the optical domain of the MULTIPLY platform.

The python code for the optical forward operator is implemented in "optical_forward_model.py"

## Microwave Forward Operator
The Water Cloud Model (WCM), as a semi empirical RT-model, was chosen for the first implementation of a RT-model for the microwave domain of the MULTIPLY platform. WCMs can be used to estimate the backscatter of vegetated surfaces accounting separately for vegetation and underlying surface contributions. An advantage of WCMs compared to other RT-models is their low parametrization effort.

The python code for the microwave forward operator is implemented in "sar_forward_model.py"

# References

ATTEMA, E. P. W. & ULABY, F. T. 1978. Vegetation modeled as a water cloud. Radio Science, 13, 357- 364.
DABROWSKA-ZIELINSKA, K., INOUE, Y., KOWALIK, W. & GRUSZCZYNSKA, M. 2007. Inferring the effect
of plant and soil variables on C- and L-band SAR backscatter over agricultural fields, based on model analysis. Advances in Space Research, 39, 139-148.
KUMAR, K., HARI PRASAD, K. S. & ARORA, M. K. 2012. Estimation of water cloud model vegetation parameters using a genetic algorithm. Hydrological Sciences Journal, 57, 776-789.
KWEON, S.-K. & OH, Y. 2015. A modified water-cloud model with leaf angle parameters for microwave backscattering from agricultural fields. IEEE Transactions on Geoscience and Remote Sensing, 53, 2802-2809.
PREVOT, L., DECHAMBRE, M., TACONET, O., VIDAL-MADJAR, D., NORMAND, M. & GALLEJ, S. 1993.
Estimating the characteristics of vegetation canopies with airborne radar measurements.
International Journal of Remote Sensing, 14, 2803-2818.
