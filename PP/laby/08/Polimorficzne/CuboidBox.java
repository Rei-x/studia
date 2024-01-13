package Polimorficzne;

public class CuboidBox extends Box {
  private double length;
  private double width;
  private double height;

  public CuboidBox(double length, double width, double height) {
    this.length = length;
    this.width = width;
    this.height = height;
  }

  @Override
  public double getExternalVolume() {
    return length * width * height;
  }

  @Override
  public double getInternalVolume() {
    return getExternalVolume();
  }

  @Override
  public String toString() {
    return "CuboidBox {" +
        "length=" + length +
        ", width=" + width +
        ", height=" + height +
        '}';
  }
}
