trait Figure {
  def area: Double
}

class Rectangle(private var _width: Double, private var _height: Double)
    extends Figure {
  require(_width > 0 && _height > 0, "Width and height must be positive values")

  def this(side: Double) = this(side, side)
  def area = _width * _height

  def height = _height
  def height_=(h: Double) = {
    require(h > 0, "Height must be a positive value")
    _height = h
  }

  def width = _width
  def width_=(w: Double) = {
    require(w > 0, "Width must be a positive value")
    _width = w
  }

}

class Splitter(val minThreshold: Double) {
  require(minThreshold >= 0, "Lower threshold must be a non-negative value")

  protected var smallFigures: List[Figure] = Nil
  protected var largeFigures: List[Figure] = Nil

  def apply(figure: Figure): Unit = {
    if (figure.area <= minThreshold) {
      smallFigures = figure :: smallFigures
    } else {
      largeFigures = figure :: largeFigures
    }
  }

  def printSmallFigures(): Unit = {
    println("Small figures:")
    smallFigures.foreach(f => println(f.area))
  }

  def printLargeFigures(): Unit = {
    println("Large figures:")
    largeFigures.foreach(f => println(f.area))
  }
}

class FineSplitter(minThreshold: Double, maxThreshold: Double)
    extends Splitter(minThreshold) {
  require(maxThreshold >= 0, "Upper threshold must be a non-negative value")
  require(
    minThreshold <= maxThreshold,
    "Lower threshold must be less than or equal to upper threshold"
  )

  private var mediumFigures: List[Figure] = Nil

  override def apply(figure: Figure): Unit = {
    if (figure.area < maxThreshold && figure.area > minThreshold) {
      mediumFigures = figure :: mediumFigures
    }
    super.apply(figure)
  }

  def printMediumFigures(): Unit = {
    println("Medium figures:")
    mediumFigures.foreach(f => println(f.area))
  }
}
