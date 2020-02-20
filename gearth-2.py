import ee
from ee import batch

ee.Initialize()

collection = ee.ImageCollection('LANDSAT/LC8_L1T_TOA')

pointCoord = ee.Geometry.Point(34, -84)
pathrow = collection.filterBounds(pointCoord)
 
clouds = pathrow.filter(ee.Filter.lt('CLOUD_COVER', 5))

bands = clouds.select(['B4', 'B3', 'B2'])

def convertBit(image):
    return image.multiply(512).uint8()  

outputVideo = bands.map(convertBit)

print "about to build video"

out = batch.Export.video.toDrive(outputVideo, description='timelapse-1', dimensions = 720, framesPerSecond = 2, region=(
[-84.33036804199219,
34.10100227884199],
[-84.27165985107422,
34.10100227884199],
[-84.27165985107422,
34.150880214361884],
[-84.33036804199219,
34.150880214361884],
[-84.33036804199219,
34.10100227884199]
), maxFrames=10000)

process = batch.Task.start(out)

print "process sent to cloud"
