package Polimorficzne;

public class ConeBox extends Box {
  private double height;
  private double radius;

  public ConeBox(double height, double radius) {
    this.height = height;
    this.radius = radius;
  }

  @Override
  public double getExternalVolume() {
    return height * Math.pow(2 * radius, 2);
  }

  @Override
  public double getInternalVolume() {
    return (8.0 / 27.0) * height * Math.pow(radius, 2);
  }

  public double getHeight() {
    return height;
  }

  public void setHeight(double height) {
    this.height = height;
  }

  public double getRadius() {
    return radius;
  }

  public void setRadius(double radius) {
    this.radius = radius;
  }

  @Override
  public String toString() {
    return "ConeBox [height=" + height + ", radius=" + radius + "]";
  }

}
