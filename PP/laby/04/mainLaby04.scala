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
    name: String,
    files: List[FileSystemEntity[FileData]]
)

def path[FileData](
    disk: Disk[FileData],
    fileSystemEntityName: String
): Option[String] = {
  def pathAux(
      fileSystemEntities: List[FileSystemEntity[FileData]],
      currentPath: String
  ): Option[String] = fileSystemEntities match {
    case List() => None
    case head :: tail =>
      head match {
        case File(name, _) if (name == fileSystemEntityName) =>
          Some(currentPath + "\\" + name)
        case Dir(name, _) if (name == fileSystemEntityName) =>
          Some(currentPath + "\\" + name)
        case Dir(name, files) =>
          pathAux(files, currentPath + "\\" + name)
        case _ => pathAux(tail, currentPath)
      }
  }

  pathAux(disk.files, disk.name + ":")
}
