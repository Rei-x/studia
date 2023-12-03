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

sealed trait FileOrDir[+FileSystem];

case class File[+FileSystem](name: String, data: FileSystem)
    extends FileOrDir[FileSystem]
case class Dir[+FileSystem](name: String, files: List[FileOrDir[FileSystem]])
    extends FileOrDir[FileSystem]

case class Disk[+FileSystem](
    name: String,
    files: List[FileOrDir[FileSystem]]
)

def path[FileSystem](
    disk: Disk[FileSystem],
    fileOrDir: String
): Option[String] = {
  def pathAux(
      filesOrDirs: List[FileOrDir[FileSystem]],
      fileOrDir: String,
      currentPath: String
  ): Option[String] = filesOrDirs match {
    case List() => None
    case head :: tail =>
      head match {
        case File(name, _) if (name == fileOrDir) =>
          Some(currentPath + "\\" + name)
        case Dir(name, _) if (name == fileOrDir) =>
          Some(currentPath + "\\" + name)
        case Dir(name, files) =>
          pathAux(files, fileOrDir, currentPath + "\\" + name)
        case _ => pathAux(tail, fileOrDir, currentPath)
      }
  }

  pathAux(disk.files, fileOrDir, disk.name + ":")
}
