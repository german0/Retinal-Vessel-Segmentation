# Retinal Vessel Segmentation
The retinal vascular condition is a reliable biomarker of several ophthalmologic and cardiovascular diseases, so automatic vessel segmentation may be crucial to diagnose and monitor them.
With that in mind, employing computer vision methodologies, we were able to segment retinal vessels from the background.

Following the steps of a research Ricci and Perfetti named "Retinal Blood Vessel Segmentation Using LineOperators and Support Vector Classification" we where able to achieve the desired results through pattern recognition and pixel-wise classification, classifying pixels as "vessel" or "non-vessel".

Furthermore, we compared the results attained with the results attained by employing a SVM (support vector machine). We concluded, as expected, that the SVM achieves better performances in termns of vessel detection accuracy with improvements in feature extraction and pixel-classification.

<p float="left">
  <img src="/DRIVE/01_test.tif" width="400" />
  <img src="/DRIVE/output_ricci/01_testbinary_manual.tif" width="400" />
</p>


**Software**

*Python*

*OpenCV*


**References**

https://ieeexplore.ieee.org/document/4336179
 
