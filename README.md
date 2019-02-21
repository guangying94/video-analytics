# video-analytics

This is a sample code that leverage on Azure Cognitive Services - Custom Vision to run real time video analytics.

## Setup Procedure
1. Install Python / Anaconda
2. Install the necessary packages (OpenCV, numpy, json, http etc)
3. Train the model in [Custom Vision](https://customvision.ai) in compact mode
4. Export container image and run in docker
5. Modify the python script to docker endpoint