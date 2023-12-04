sealed trait tree3[+A];

case object Empty extends tree3[Nothing]

case class Node[+A](
    element: A,
    leftTree: tree3[A],
    middleTree: tree3[A],
    rightTree: tree3[A]
) extends tree3[A]

def map3[A, B](tree: tree3[A])(f: A => B): tree3[B] = tree match {
  case Empty => Empty
  case Node(element, leftTree, middleTree, rightTree) =>
    Node(f(element), map3(leftTree)(f), map3(middleTree)(f), map3(rightTree)(f))
}

sealed trait FileSystemEntity[+FileData];

case class File[+FileData](name: String, data: FileData)
    extends FileSystemEntity[FileData]
case class Dir[+FileData](name: String, files: List[FileSystemEntity[FileData]])
    extends FileSystemEntity[FileData]

case class Disk[+FileData](
    name: Char,
    files: List[FileSystemEntity[FileData]]
)

def path[FileData](
    disk: Disk[FileData],
    fileSystemEntityName: String
): Option[String] = {
  def pathAux(
      fileSystemEntities: List[FileSystemEntity[FileData]],
      path: String,
      depth: Int
  ): Option[(String, Int)] = {
    if (
      fileSystemEntities.exists(x => {
        x match {
          case Dir(name, _) if (name == fileSystemEntityName)  => true
          case File(name, _) if (name == fileSystemEntityName) => true
          case _                                               => false
        }
      })
    ) {
      Some((path, depth))
    } else {
      fileSystemEntities.foldLeft(None: Option[(String, Int)])(
        (currentBestResult, fileSystemEntity) =>
          fileSystemEntity match {
            case Dir(dirName, dirFiles) =>
              currentBestResult match {
                case Some((_, currentDepth)) =>
                  val newResult =
                    if (currentDepth <= depth)
                      None
                    else
                      fileSystemEntity match {
                        case Dir(name, fileSystemEntities) =>
                          pathAux(fileSystemEntities, path + name, depth)
                        case File(name, data) => None
                      }

                  newResult match {
                    case Some((_, newDepth)) if (newDepth < currentDepth) =>
                      newResult
                    case _ => currentBestResult
                  }
                case _ =>
                  pathAux(dirFiles, path + "\\" + dirName, depth + 1)
              }
            case _ => currentBestResult
          }
      )
    }
  }

  pathAux(disk.files, disk.name + ":", 0).map(_._1) match
    case None        => None
    case Some(value) => Some(value + "\\" + fileSystemEntityName)

}

def insert[FileData](
    disk: Disk[FileData],
    fileSystemEntity: FileSystemEntity[FileData],
    path: String
): Disk[FileData] = {
  def insertAux(
      fileSystemEntities: List[FileSystemEntity[FileData]],
      path: String
  ): List[FileSystemEntity[FileData]] = {
    val pathParts = path.split("\\\\").toList
    val pathPartsLength = pathParts.length
    val pathPart = pathParts.head
    val pathPartTail = pathParts.tail

    fileSystemEntities match {
      case List() =>
        pathPart match {
          case "" => List(fileSystemEntity)
          case _ =>
            List(Dir(pathPart, insertAux(List(), pathPartTail.mkString("\\"))))
        }
      case head :: tail =>
        head match {
          case Dir(name, files) if (name == pathPart) =>
            if (pathPartsLength == 1) {
              Dir(name, fileSystemEntity :: files) :: tail
            } else {
              Dir(name, insertAux(files, pathPartTail.mkString("\\"))) :: tail
            }
          case _ => head :: insertAux(tail, path)
        }
    }

  }

  Disk(disk.name, insertAux(disk.files, path))
}
