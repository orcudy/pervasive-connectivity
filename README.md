###Pervasive Connectivity: Classifying Supporters and Opponents of Governmental Surveillance Programs

####Abstract
In this paper, I investigate people's support of governmental surveillance programs using the Pervasive Connectivity dataset provided by the Pew Research Center. The dataset was obtained via phone interview from August 7, 2013 to September 16, 2013 and consists of a sample of 1,801 adults residing in the United States. The dataset was analyzed using principal component analysis using Numpy, a scientific computing library written in the Python programming language. Principal component analysis did not yield data separation; therefore, I was unable to reach any significant conclusion about people's support of governmental surveillance programs.

####File Structure
**data**
* *CSV.csv*: Pervasive Connectivity dataset  
* *Iris.csv*: Fisher's Iris dataset

**images**
* *graph*: all principal component analysis comparison graphs 
* *pc*: tables containing first two eigenvectors of correlation matrix  
* *src_images*: screenshots of source code  

**src**
* *connect.py*: main routine for Pervasive Connectivity analysis  
* *iris.py*: main routine for Iris analysis  
* *keys.py*: lookup table for data categorization  
* *csvutils.py*: library for manipulating csv data  
* *linalg.py*: library for logging results of linear algebra computation  
* *utils.py*: library for general utilities  
