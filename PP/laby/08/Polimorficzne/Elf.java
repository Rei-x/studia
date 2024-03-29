package Polimorficzne;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Elf {
  private List<List<Box>> boxesStacks = new ArrayList<>();

  public void arrangeBoxes(List<Box> boxes) {
    Collections.sort(boxes, Collections.reverseOrder());

    System.err.println(boxes);
    System.out.println("The biggest one: " + boxes.get(0));
    for (Box currentBox : boxes) {
      boolean isPlaced = false;

      for (List<Box> stack : boxesStacks) {
        if (currentBox.getExternalVolume() < stack.get(stack.size() - 1).getInternalVolume()) {
          stack.add(currentBox);

          System.out.println("Box: " + currentBox + ", added to stack: " + stack);
          isPlaced = true;
          break;
        }
      }

      if (!isPlaced) {
        List<Box> newStack = new ArrayList<>();
        newStack.add(currentBox);
        boxesStacks.add(newStack);
        System.out.println("New stack: " + newStack);
      }
    }
  }

  public List<List<Box>> getBoxesStacks() {
    return boxesStacks;
  }

  public double getTotalVolume() {
    double totalVolume = 0;
    for (List<Box> stack : boxesStacks) {
      totalVolume += stack.get(0).getExternalVolume();
    }
    return totalVolume;
  }
}