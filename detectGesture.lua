scriptId = 'com.besthack.gesturedetect'
scriptTitle = "Gesture Detect"
scriptDetailsUrl = "" -- We don't have this until it's submitted to the Myo Market

startTime = myo.getTimeMilliseconds()
currentTime = 0

BUFFER_SIZE = 8

xGryoBuffer = {}
xGyroIndex = 1

for i=1,BUFFER_SIZE do
  xGryoBuffer[i] = 0
end

xAccelBuffer = {}
xAccelIndex = 1

timeOfLastVibrate = -1

for i=1,BUFFER_SIZE do
  xAccelBuffer[i] = 0
end

function onPeriodic()
  updateBuffers()
  updateTime()

  if isPointUp() then
    if timeOfLastVibrate == -1 or currentTime - timeOfLastVibrate > 1000 then
      timeOfLastVibrate = currentTime
      myo.vibrate("short")
    end
    
    myo.debug("Point Up")
  end

  if currentTime - startTime > 250 then 
    startTime = currentTime
    printValues()
  end
end

function isPointUp()
  if getAverage(xGryoBuffer) > 75 and getAverage(xAccelBuffer) < -0.75 then
    return true
  end

  return false
end

function updateBuffers()
  xGyro, yGyro, zGyro = myo.getGyro()
  xGryoBuffer[xGyroIndex] = xGyro
  xGyroIndex = xGyroIndex + 1

  if xGyroIndex > BUFFER_SIZE then
    xGyroIndex = 1
  end

  xAccel, yAccel, zAccel = myo.getAccel()
  xAccelBuffer[xAccelIndex] = xAccel
  xAccelIndex = xAccelIndex + 1

  if xAccelIndex > BUFFER_SIZE then
    xAccelIndex = 1
  end
end

function updateTime()
  currentTime = myo.getTimeMilliseconds()
end

function printValues()
  xGyro, yGyro, zGyro = myo.getGyro()
  xAccel, yAccel, zAccel = myo.getOrientationWorld()

  spaces = 16 - string.len(xGyro .. "")
  space1 = ""

  for i=1, spaces do 
    space1 = space1 .. " "
  end

  spaces = 16 - string.len(yGyro .. "")
  space2 = ""

  for i=1, spaces do 
    space2 = space2 .. " "
  end

  spaces = 16 - string.len(zGyro .. "")
  space3 = ""

  for i=1, spaces do 
    space3 = space3 .. " "
  end

  spaces = 16 - string.len(xAccel .. "")
  space4 = ""

  for i=1, spaces do 
    space4 = space4 .. " "
  end

  spaces = 16 - string.len(yAccel .. "")
  space5 = ""

  for i=1, spaces do 
    space5 = space5 .. " "
  end

  spaces = 16 - string.len(zAccel .. "")
  space6 = ""

  for i=1, spaces do 
    space6 = space6 .. " "
  end

  myo.debug(xGyro .. space1 .. ", " .. yGyro .. space2 .. ", " .. zGyro .. space3 .. ", " .. xAccel .. space4 .. ", " .. yAccel .. space5 .. ", " .. zAccel)
end

function getAverage(buffer)
  average = 0

  for i=1,BUFFER_SIZE do
    average = average + buffer[i]
  end

  return average / BUFFER_SIZE
end



function onForegroundWindowChange(app, title)
    myo.debug("onForegroundWindowChange: " .. app .. ", " .. title)
    return true
end

function activeAppName()
    return "Output Everything"
end

function onActiveChange(isActive)
    myo.debug("onActiveChange")
end