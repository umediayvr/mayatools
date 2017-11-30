import qbs
import qbs.File
import qbs.TextFile
import qbs.FileInfo
import "installExtra/mainGroup.qbs" as MainGroup

Project {
  id: main
  property string name: "maya"
  property string releaseType
  property int mayaMajorVersion

  Probe {
    id: info
    property string fileName: "info.json"
    property var data
    configure: {
      // making sure the info file exists
      if (!File.exists(fileName)){
        throw new Error("Cannot find: " + fileName)
      }

      // parsing info contents
      data = JSON.parse(new TextFile(fileName).readAll())
      return data
    }
  }

  Application {
    name: "defaultMaya2018"
    MainGroup {
      name: main.name
      version: info.data.version
      mayaMajorVersion: 2018
      releaseType: main.releaseType

      condition: (main.mayaMajorVersion === undefined || main.mayaMajorVersion == mayaMajorVersion)
    }
  }

  Application {
    name: "defaultMaya2017"
    MainGroup {
      name: main.name
      version: info.data.version
      mayaMajorVersion: 2017
      releaseType: main.releaseType

      condition: (main.mayaMajorVersion === undefined || main.mayaMajorVersion == mayaMajorVersion)
    }
  }
}
