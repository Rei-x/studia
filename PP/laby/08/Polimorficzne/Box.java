package Polimorficzne;

public abstract class Box implements Comparable<Box> {

  public abstract double getExternalVolume();

  public abstract double getInternalVolume();

  @Override
  public int compareTo(Box other) {
    return Double.compare(this.getExternalVolume(), other.getExternalVolume());
  }

  @Override
  public abstract String toString(); // Abstrakcyjna metoda do nadpisania w klasach potomnych
}