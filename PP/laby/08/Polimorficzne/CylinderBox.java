package Polimorficzne;

public class CylinderBox extends Box {
  private double radius;
  private double height;

  public CylinderBox(double radius, double height) {
    this.radius = radius;
    this.height = height;
  }

  @Override
  public double getExternalVolume() {
    return (radius * 2) * (radius * 2) * height;
  }

  @Override
  public double getInternalVolume() {
    return Math.pow(radius * Math.sqrt(2), 2) * height;
  }

  @Override
  public String toString() {
    return "CylinderBox {" +
        "radius=" + radius +
        ", height=" + height +
        '}';
  }
}