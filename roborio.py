from networktables import NetworkTables
import time
while True:
     NetworkTables.initialize(server = '10.37.34.2')#roboRIO-3734-frc.local')
     print(NetworkTables.isConnected())
     sd = NetworkTables.getTable("Vision")
     sd.putNumber("distance",12)#doesn't show up in table
     sd.putString("orientation","right")
     NetworkTables.shutdown()
     time.sleep(1)
