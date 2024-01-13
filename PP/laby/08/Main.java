import java.util.Arrays;
import java.util.List;

import Niepolimorficzne.BoxType;
import Polimorficzne.CuboidBox;
import Polimorficzne.CylinderBox;
import Polimorficzne.SphereBox;

public class Main {
  public static void main(String[] args) {
    polimorfia();
    niepolimorfia();
  }

  private static void polimorfia() {
    System.out.println("-------------Polimorfia-------------");
    List<Polimorficzne.Box> allBoxes = Arrays.asList(
        new CuboidBox(10, 5, 2),
        new CuboidBox(10, 5, 2),
        new CuboidBox(10, 5, 2),
        new CylinderBox(2, 10),
        new SphereBox(6),
        new CuboidBox(4, 4, 12));

    Polimorficzne.Elf elf = new Polimorficzne.Elf();
    elf.arrangeBoxes(allBoxes);
    List<List<Polimorficzne.Box>> boxesStacks = elf.getBoxesStacks();

    for (int i = 0; i < boxesStacks.size(); i++) {
      System.out.println("Stack " + (i + 1) + ": " + boxesStacks.get(i));
    }

    double totalVolume = elf.getTotalVolume();
    System.out.println("Total external volume: " + totalVolume);
    System.out.println("-------------Koniec polimorfii-------------");
  }

  private static void niepolimorfia() {
    System.out.println("-------------Niepolimorfia-------------");
    List<Niepolimorficzne.Box> allBoxes = Arrays.asList(
        new Niepolimorficzne.Box(BoxType.Cuboid, new Double[] { 10.0, 5.0, 2.0 }),
        new Niepolimorficzne.Box(BoxType.Cuboid, new Double[] { 10.0, 5.0, 2.0 }),
        new Niepolimorficzne.Box(BoxType.Cuboid, new Double[] { 10.0, 5.0, 2.0 }),
        new Niepolimorficzne.Box(BoxType.Cylinder, new Double[] { 2.0, 10.0 }),
        new Niepolimorficzne.Box(BoxType.Sphere, new Double[] { 6.0 }),
        new Niepolimorficzne.Box(BoxType.Cuboid, new Double[] { 4.0, 4.0, 12.0 }));

    Niepolimorficzne.Elf elf = new Niepolimorficzne.Elf();
    elf.arrangeBoxes(allBoxes);
    List<List<Niepolimorficzne.Box>> boxesStacks = elf.getBoxesStacks();

    for (int i = 0; i < boxesStacks.size(); i++) {
      System.out.println("Stack " + (i + 1) + ": " + boxesStacks.get(i));
    }

    double totalVolume = elf.getTotalVolume();
    System.out.println("Total external volume: " + totalVolume);
    System.out.println("-------------Koniec niepolimorfii-------------");
  }
}