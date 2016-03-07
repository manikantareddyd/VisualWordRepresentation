# Visual Word Representation

##	Introduction
Bag of words model of language seems to be very good at matching documents by treating documents as just a bag of important keywords and then matching similar bags! So why not try this on images.

After all an image is just a collection of objects! Somehow if we are able to represent these images as a bag of visual words, we might be in luck.

##	Visual Word Representation
The main idea is to arrive at some descriptors called Visual Words. What should visual word look like. It must be a set of lookalike interest points. If we bring similar interest points together they might represent something

Now we need to cluster the interest points. Turns out a simple k means clustering is enough. We perform a hierarchical K-Means clustering to some predefined k and depth. The leaf nodes are then believed to be the Visual Words. Now we describe the Image only in terms of the Visual Words.

+	Get SIFT descriptors of Interest points.
+	Perform a Hierarchical K Means, retaining only the centroid for each node.
+	For any image get its SIFT descriptors and for evry descriptor make it travel down the tree, by using a distance measure between the SIFT descriptor and the Node representative.
+	Note the leaf to which it falls. By this way we get a histogram representation of the image in terms of Visual Words.
+	Note the Histogram.

## Implementation
We’ll be working on the UKY data set which contains about 10,000 images of groups of 4 images. There could be as many as 2000-3000 SIFT interest points in each image.

But we’ll be using only 500 feature points on only 1000 images at max to save on memory and computation.
Using these 500 SIFT descriptors for every image we performed a normal distance based measurement to find 4 closest neighbors of it using the Vocabulary tree.

As the test set and train set are the same, the best match is always the image itself (makes sense) We’ll assign a score of 0.25 if the match lies in one of the four images of the group to which the original image belonged to.

At max every image  gets a max score of 1 if all  the matches belong to the image group, the minimum it gets is 0.25 (A match with itself)

## Results

<img src="res/1.PNG">

<img src="res/2.PNG">

<img src="res/3.PNG">

As can be seen it appears that increasing the depth as well as the Number of branches increase the accuracy of match.

The accuracies are also very great (~0.98).

Using too many images tends to lower the accuracy as the number of available features is too diverse and finding a match becomes difficult.

Same is the case with too less features as the data tends to over fit over the given images.

The UKY data set can be downloaded from <a href = "http://vis.uky.edu/~stewe/ukbench/" target="_blank"> Here</a>
