package Niepolimorficzne;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Box implements Comparable<Box> {
  private BoxType type;

  private List<Double> dimensions;

  public Box(BoxType type, Double[] dimensions) {
    this.type = type;
    this.dimensions = new ArrayList<Double>(Arrays.asList(dimensions));
  }

  public double getExternalVolume() {
    switch (type) {
      case Cuboid:
        return dimensions.get(0) * dimensions.get(1) * dimensions.get(2);
      case Cylinder:
        return Math.pow(dimensions.get(0) * 2, 2) * dimensions.get(1);
      case Sphere:
        return Math.pow(dimensions.get(0) * 2, 3);
      default:
        throw new IllegalArgumentException("Unknown box type");
    }
  };

  public double getInternalVolume() {
    switch (type) {
      case Cuboid:
        return dimensions.get(0) * dimensions.get(1) * dimensions.get(2);
      case Cylinder:
        return Math.pow(dimensions.get(0) * Math.sqrt(2), 2) * dimensions.get(1);
      case Sphere:
        return Math.pow(dimensions.get(0) * Math.sqrt(3), 3);
      default:
        throw new IllegalArgumentException("Unknown box type");
    }
  }

  public int compareTo(Box other) {
    return Double.compare(this.getExternalVolume(), other.getExternalVolume());
  }

  @Override
  public String toString() {
    return "Box [type=" + type + ", dimensions=" + dimensions + "]";
  }

}
