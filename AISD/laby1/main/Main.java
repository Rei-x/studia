import java.util.Scanner;

public class Main {

  static Scanner scan;

  /***
   * commands:
   * py size
   * draw a pyramid with size
   * ct size
   * draw a christmas tree with size
   * ld documentName
   * load document from standard input line by line. Last line consists of only
   * sequence "eod",
   * which means end of document
   * ha
   * halt program and finish execution
   * 
   * @param args
   */

  public static void main(String[] args) {
    System.out.println("START");
    scan = new Scanner(System.in);
    boolean halt = false;
    while (!halt) {
      String line = scan.nextLine();
      // empty line and comment line - read next line
      if (line.length() == 0 || line.charAt(0) == '#')
        continue;
      // copy line to output (it is easier to find a place of a mistake)
      System.out.println("!" + line);
      String word[] = line.split(" ");
      if (word[0].equalsIgnoreCase("py") && word.length == 2) {
        int value = Integer.parseInt(word[1]);
        Drawer.drawPyramid(value);
        continue;
      }
      if (word[0].equalsIgnoreCase("ct") && word.length == 2) {
        int value = Integer.parseInt(word[1]);
        Drawer.drawChristmassTree(value);
        continue;
      }
      if (word[0].equalsIgnoreCase("sqr") && word.length == 2) {
        int value = Integer.parseInt(word[1]);
        Drawer.square(value);
        continue;
      }
      // ld documentName
      if (word[0].equalsIgnoreCase("ld") && word.length == 2) {
        Document.loadDocument(word[1], scan);
        continue;
      }
      // ha
      if (word[0].equalsIgnoreCase("ha") && word.length == 1) {
        halt = true;
        continue;
      }
      System.out.println("Wrong command");
    }
    System.out.println("END OF EXECUTION");
    scan.close();

  }

}
