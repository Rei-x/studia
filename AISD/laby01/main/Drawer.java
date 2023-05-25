
public class Drawer {
  private static void drawLine(int n, char ch) {
    for (int i = 0; i < n; i++)
      System.out.print(ch);
  }

  private static void drawPiramidSmart(int n, int margin) {
    for (int i = 0; i < n; i++) {
      drawLine(margin + (n - i - 1), '.');
      drawLine(2 * i + 1, 'X');
      drawLine(margin + (n - i - 1), '.');
      System.out.println();
    }
  }

  public static void square(int n) {
    drawLine(n, 'X');
    System.out.println();
    for (int i = 0; i < n - 2; i++) {
      drawLine(1, 'X');
      drawLine(n - 2, '.');
      drawLine(1, 'X');
      System.out.println();
    }
    drawLine(n, 'X');
    System.out.println();
  }

  public static void drawPyramid(int n) {
    drawPiramidSmart(n, 0);
  }

  public static void drawChristmassTree(int n) {
    for (int i = 1; i < n + 1; i++) {
      drawPiramidSmart(i, n - i);
    }
  }

}
