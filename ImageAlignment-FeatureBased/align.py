#[learnOpencv]/learnopencv/ImageAlignment-FeatureBased/align.py
# KEYPOINTS --  keypoints, which are just the location of regions of interest. ( Source -- https://pyimagesearch.com/2020/08/31/image-alignment-and-registration-with-opencv/)


from __future__ import print_function
import cv2
import numpy as np


MAX_MATCHES = 500
GOOD_MATCH_PERCENT = 0.15


def alignImages(im1, im2):

  # Convert images to grayscale
  im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
  im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
  
  # Detect ORB features and compute descriptors.
  orb = cv2.ORB_create(MAX_MATCHES)
  keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
  keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
  
  # Match features. 
  #BLOG >># We use the hamming distance as a measure of similarity between two feature descriptors.
  matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)

  matches = matcher.match(descriptors1, descriptors2, None)

  print("---type(matches---",type(matches)) # TUPLE -- (< cv2.DMatch 0x7f87383db5b0>, < cv2.DMatch 0x7f87383db250>, < cv2.DMatch 0x7f87383db530>,
  #print("---len(matches)---",len(matches)) # 500 
  ls_matches = list(matches)
  #print("---len(ls_matches)---",len(ls_matches)) # 500 
  print("---ls_matches[:5]---",ls_matches[:5])
  print("-----     "*10)
  
  # Sort matches by score
  # set_matches_sorted = matches.sort(key=lambda x: x.distance, reverse=False)
  # print("---type(set_matches_sorted---",type(set_matches_sorted))
  ls_sorted = sorted(ls_matches,key=lambda x: x.distance, reverse=False)
  print("---type(ls_sorted---",type(ls_sorted))
  print("---ls_sorted[:5]---",ls_sorted[:5])
  print("-----     "*10)

  #matches.sort(key=lambda x: x.distance, reverse=False)

  # Remove not so good matches
  numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
  matches = matches[:numGoodMatches]

  # Draw top matches
  imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
  cv2.imwrite("matches.jpg", imMatches)
  
  # Extract location of good matches
  points1 = np.zeros((len(matches), 2), dtype=np.float32)
  points2 = np.zeros((len(matches), 2), dtype=np.float32)

  for i, match in enumerate(matches):
    points1[i, :] = keypoints1[match.queryIdx].pt
    points2[i, :] = keypoints2[match.trainIdx].pt
  
  # Find homography
  h, mask = cv2.findHomography(points1, points2, cv2.RANSAC) ## Random Sample Consensus (RANSAC) 

  # Use homography
  height, width, channels = im2.shape
  im1Reg = cv2.warpPerspective(im1, h, (width, height))
  
  return im1Reg, h


if __name__ == '__main__':
  
  # Read reference image
  refFilename = "form.jpg"
  print("Reading reference image : ", refFilename)
  imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)

  # Read image to be aligned
  imFilename = "scanned-form.jpg"
  print("Reading image to align : ", imFilename);  
  im = cv2.imread(imFilename, cv2.IMREAD_COLOR)
  
  print("Aligning images ...")
  # Registered image will be resotred in imReg. 
  # The estimated homography will be stored in h. 
  imReg, h = alignImages(im, imReference)
  
  # Write aligned image to disk. 
  outFilename = "aligned.jpg"
  print("Saving aligned image : ", outFilename); 
  cv2.imwrite(outFilename, imReg)

  # Print estimated homography
  print("Estimated homography : \n",  h)
  
