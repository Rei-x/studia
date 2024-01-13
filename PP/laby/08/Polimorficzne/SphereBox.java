package Polimorficzne;

public class SphereBox extends Box {
  private double radius;

  public SphereBox(double radius) {
    this.radius = radius;
  }

  @Override
  public double getExternalVolume() {
    return Math.pow(radius * 2, 3);
  }

  @Override
  public double getInternalVolume() {
    return Math.pow(radius * Math.sqrt(3), 3);
  }

  @Override
  public String toString() {
    return "SphereBox {" +
        "radius=" + radius +
        '}';
  }
}