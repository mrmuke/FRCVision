from networktables import NetworkTables
while True:

     NetworkTables.initialize(server = 'roborio-3734-frc.local')
     print(NetworkTables.isConnected())
     sd = NetworkTables.getTable("SmartDashboard")
     sd.putNumber("someNumber",1234)#doesn't show up in table
     NetworkTables.shutdown()
